from flask import Flask, render_template, request, session
from bot import Bot
import os


app = Flask(__name__)
bot = Bot()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return bot.Handle(session, userText)


if __name__ == "__main__":
    app.secret_key = "test"
    print(os.environ["DEBUG"])
    if "DEBUG" not in os.environ:
        app.run()
    else :
        app.run(debug=(os.environ["DEBUG"] == "true"))
