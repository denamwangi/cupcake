from flask import Flask, request, jsonify, redirect, Response, json
import os
import pprint
import requests
from slack_utils import SlackHelper
import github_utils as gh

app = Flask(__name__)
slack = SlackHelper(os.environ["BOT_USER_ACCESS_TOKEN"])

# TODO[DENA]: add check for 1st and 100th commit, and 100th review
def check_milestone(event_type, sender):
    if event_type == 'pull_request_review':
        reviews = gh.get_repo_reviews()
        user_review_count = reviews.get(sender, None)
        print "*****This user {} has {} prs reviewed yaaayyyy!".format(sender, user_review_count)
        if user_review_count == 1:
            text = "Yasss! Congrats to {} for reviewing their first PR!!!!".format(
                    sender)
            slack.post_message(text)


@app.route("/")
def show_index():
    # pprint.pprint(slack_client.api_call("channels.list"))
    return "click <a href='/test-message'>here</a> to send a test message"


@app.route("/github", methods=['POST'])
def process_github_webhook():
    # github sends us the event, sender, repo, and action. The type of event is in the header.
    # TODO: Switch this to a dict with keys being actions specific to the event
    valid_actions = ['submitted', 'opened', 'closed']
    valid_events = ['pull_request_review', 'commits']

    if request.method != 'POST':
        return Response('noooopes\n', status=405)
    event_type = request.headers.get('X-Github-Event')
    try:
        data = json.loads(request.data)
    except Exception:
        return Response('ayooo this is not json\n', status=400)

    action = data.get('action', None)
    sender = data.get('sender', {}).get('login', None)
    print "********Github webhook come thruuuu:"
    print "event type", event_type
    print "action",  action
    print "sender",  sender

    if event_type in valid_events:
        check_milestone(event_type, sender)

    return Response(status=201, headers=(
        ('Access-Control-Allow-Origin', '*'),
    ))


@app.route("/test-message")
def send_test_message():
    slack.post_message("Hello from the cupcake app! :tada:")
    return redirect("/")


@app.route("/slash-cupcake", methods=["POST"])
def handle_slash_command():
    """Respond to a /cupcake command"""

    requesting_user_id = request.form.get('user_id')
    command = request.form.get('text')
    response_url = request.form.get('response_url')

    # TODO this will prob be necessary once we start storing data
    # user_info = slack.get_user_info(requesting_user_id))

    return slack.process_slash_command(requesting_user_id,
                                       command,
                                       response_url)


if __name__ == "__main__":
    app.run(debug=True)
