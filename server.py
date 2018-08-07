from flask import Flask, request, json, Response
from slackclient import SlackClient
import os
import pprint

app = Flask(__name__)
slack_client = SlackClient(os.environ["BOT_USER_ACCESS_TOKEN"])


@app.route("/")
def show_index():
    # pprint.pprint(slack_client.api_call("channels.list"))

    # printing so we can see the output - this can be taken out once everything's working
    pprint.pprint(slack_client.api_call("chat.postMessage", channel="CC32SU9DE",
                                        text="Hello from actual cupcake! :tada:", username="cupcake"))
    return "it worked!!!"


@app.route("/github", methods=['POST'])
def process_github_webhook():
    # github sends us the issue, sender, repo, and action
    valid_actions = ['opened', 'closed']
    if request.method != 'POST':
        return Response('noooopes\n', status=405)

    start = datetime.utcnow()

    try:
        data = json.loads(request.data)
    except Exception:
        return Response('ayooo this is not json\n', status=400)

    action = data.get('action', None)
    sender = data.get('sender', None)

    print "HI HI {} just {} an issue in this repo".format(sender['login'], action)

    return Response(status=201, headers=(
        ('Access-Control-Allow-Origin', '*'),
    ))



if __name__ == "__main__":
    app.run(debug=True)
