from flask import Flask, request, jsonify, redirect, Response, json
from slackclient import SlackClient
import os
import re
import pprint
import requests

app = Flask(__name__)

# TODO probably factor all slack setup stuff out into it's own file/class(?)
slack_token = os.environ["BOT_USER_ACCESS_TOKEN"]
slack_client = SlackClient(slack_token)


def get_user_info(user_id):
    return slack_client.api_call(
        "users.info",
        user=user_id,
        token=slack_token
    )

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

def post_to_slack(text):
    """ Convenience method to make it easier to post to slack. Might generalize even more e.g. pass in channel
        printing so we can see the output - this can be taken out once everything's working
    """
    pprint.pprint(
        slack_client.api_call("chat.postMessage",
                              channel="CC32SU9DE",
                              text=text, username="cupcake"))

def oxfordize(strings):
    """Given a list of strings, formats them correctly given the length of the
    list. For example:
        oxfordize(['A'])  =>  'A'
        oxfordize(['A', 'B'])  =>  'A and B'
        oxfordize(['A', 'B', 'C'])  =>  'A, B, and C'
    """

    if len(strings) == 0:
        return ''
    elif len(strings) == 1:
        return strings[0]
    elif len(strings) == 2:
        return '%s and %s' % (strings[0], strings[1])
    else:
        return '%s, and %s' % (', '.join(strings[:-1]), strings[-1])


@app.route("/")
def show_index():
    # pprint.pprint(slack_client.api_call("channels.list"))

    return "click <a href='/test-message'>here</a> to send a test message"


@app.route("/test-message")
def send_test_message():
    test = "Hello from actual cupcake! :tada:"
    post_to_slack(test)
    return redirect("/")


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
    post_to_slack(text)

    return Response(status=201, headers=(
        ('Access-Control-Allow-Origin', '*'),
    ))


@app.route("/slash-test", methods=["POST"])
def handle_slash_command():
    requesting_user_id = request.form.get('user_id')
    command_text = request.form.get('text')
    mentioned_users = re.findall(r"<@U\S*>", command_text)

    # TODO enforce the 'for'ness with a try and return error message if it didn't work
    reason = command_text.split(" for ")[-1]

    # requesting_user_info = get_user_info(requesting_user_id)

    response_body = {
        "text": "<@{user_id}> gave a cupcake to {users} for {reason}".format(
            user_id=requesting_user_id,
            users=oxfordize(mentioned_users),
            reason=reason),
        "response_type": "in_channel",
        "attachments": [{
            "text": "Thanks for giving cupcakes!"
        }],
    }

    return jsonify(response_body)


if __name__ == "__main__":
    app.run(debug=True)
