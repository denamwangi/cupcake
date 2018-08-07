from flask import Flask, request, jsonify
from slackclient import SlackClient
import os
import pprint

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


@app.route("/")
def show_index():
    # pprint.pprint(slack_client.api_call("channels.list"))

    # printing so we can see the output - this can be taken out once everything's working
    pprint.pprint(slack_client.api_call("chat.postMessage", channel="CC32SU9DE",
                                        text="Hello from actual cupcake! :tada:", username="cupcake"))
    return "it worked!!!"


@app.route("/slash-test", methods=["POST"])
def handle_slash_command():
    # import pdb
    # pdb.set_trace()
    command_text = request.form.get('text')
    slack_uid = request.form.get('user_id')
    # # TODO ^ change the name of this variable - it's the requesting user

    user_info = get_user_info(slack_uid)

    response_body = {"text": "you entered " + command_text}

    return jsonify(response_body)


if __name__ == "__main__":
    app.run(debug=True)
