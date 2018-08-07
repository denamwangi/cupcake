from flask import Flask
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


if __name__ == "__main__":
    app.run(debug=True)
