from flask import Flask, request, jsonify, redirect, Response, json
import os
import pprint
import requests
from slack_utils import SlackHelper

app = Flask(__name__)
slack = SlackHelper(os.environ["BOT_USER_ACCESS_TOKEN"])


def get_repo_info():
    """ Grabs all the authors and their number of commits to the repo
        returns {'author_name': int no_of_commits}
    """
    request_url = 'https://api.github.com/repos/denamwangi/CupCake/commits'
    response = json.loads(requests.get(request_url).content)

    committers = {}
    for each_commit in response:
        # import ipdb; ipdb.set_trace()
        author = each_commit['author']['login']
        committers[author] = committers.get(author, 0) + 1

    return committers


@app.route("/")
def show_index():
    # pprint.pprint(slack_client.api_call("channels.list"))
    return "click <a href='/test-message'>here</a> to send a test message"


@app.route("/github", methods=['POST'])
def process_github_webhook():
    # github sends us the issue, sender, repo, and action
    valid_actions = ['opened', 'closed']
    if request.method != 'POST':
        return Response('noooopes\n', status=405)

    try:
        data = json.loads(request.data)
    except Exception:
        return Response('ayooo this is not json\n', status=400)
    pprint.pprint("Github webhook come thruuuu:", data)
    action = data.get('action', None)
    sender = data.get('sender', None)

    text = "Sup' {} just {} an issue in this repo".format(
        sender['login'], action)
    slack.post_message(text)

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
