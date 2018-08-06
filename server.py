from flask import Flask

app = Flask(__name__)


@app.route("/")
def show_index():
    return "it worked!!!"


if __name__ == "__main__":
    app.run(debug=True)
