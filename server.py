from flask import Flask, request, jsonify, redirect, Response, json
import os
import pprint
import requests
from slack_utils import SlackHelper

app = Flask(__name__)
slack = SlackHelper(os.environ["BOT_USER_ACCESS_TOKEN"])


def get_repo_commits():
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


def get_repo_reviews():
    """ Grabs all the reviewers and the number of reviews to the repo
        returns {'reviewer_name': int no_of_reviews}
    """
    request_url = 'https://api.github.com/repos/denamwangi/skills_flask/pulls?state=all'
    response = json.loads(requests.get(request_url).content)

    repo_reviewers = {}
    for each_pr in response:
        # grab the pr id, pass that to the reviews function, which asks 
        # for all the reviews for that pr and grabs all the authors of the reviews
        # import ipdb; ipdb.set_trace()
        id = each_pr.get('number')
        reviewers = get_pr_reviews(id)
        for reviewer in reviewers:
            repo_reviewers[reviewer] = repo_reviewers.get(reviewer, 0) + 1

    return 'repo_reviewers'

def get_pr_reviews(id):
    """ Grabs all the reviews for this pr. Returns a set of all reviewers
    """

    request_url = 'https://api.github.com/repos/denamwangi/skills_flask/pulls/{}/reviews'.format(id)

    response = json.loads(requests.get(request_url).content)
    pr_reviewers = set()
    for each_review in response:
        reviewer = each_review['user']['login']
        pr_reviewers.add(reviewer)
    return pr_reviewers


@app.route("/")
def show_index():
    # pprint.pprint(slack_client.api_call("channels.list"))
    return "click <a href='/test-message'>here</a> to send a test message"


@app.route("/github", methods=['POST'])
def process_github_webhook():
    # github sends us the event, sender, repo, and action. The type of event is in the header.
    valid_actions = ['submitted', 'opened', 'closed']
    valid_events = ['pull_request_review', 'commits']
    if request.method != 'POST':
        return Response('noooopes\n', status=405)
    event_type = request.headers.get('X-Github-Event')
    try:
        data = json.loads(request.data)
    except Exception:
        return Response('ayooo this is not json\n', status=400)
    print "********Github webhook come thruuuu:", data

    # TODO[Dena]: add a check to see if this is the first/nth commit or review
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
