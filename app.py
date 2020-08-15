from flask import Flask, render_template, request, session
from bot import Bot


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
    app.run(debug=True)
