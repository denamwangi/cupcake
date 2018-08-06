from flask import Flask
from slackclient import SlackClient
import os

app = Flask(__name__)
slack_client = SlackClient(os.environ["SLACK_TEST_TOKEN"])


@app.route("/")
def show_index():
    print slack_client.api_call("api.test")
    return "it worked!!!"


if __name__ == "__main__":
    app.run(debug=True)
