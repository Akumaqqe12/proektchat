from flask import Flask, Response , request
from flask_cors import CORS
from uuid import uuid4
import json
import time 
import datetime
timestamp = time.time()


tokens = {}
messages = []
msg = {}
users = {}

def delete_user(name):
    users.remove(name)

app = Flask(__name__)
CORS(app)


def generate_token():
    token = str(uuid4())
    return token


@app.route("/")
def main():
    return "commands: /auth, /logout, /send, /getall"


@app.route("/auth")
def auth(): 
    username = request.args.get('name')
    if username is None:
        return "НАПИШИ ЧТО-ТО, НЕ БУДЬ ДЕБИЛОМ"
    if username in users:
        return "Уже есть такой ишак, второго такого не надо"
    else:
        token = generate_token()
        print(f"Твоя монета, держи: {token}")
        print (username,token)
        users[username] = token
        tokens[username] = token
        return f"{username}, {token}"


@app.route("/logout")
def logout():
    username_to_logout = request.args.get('name')
    if username_to_logout is None:
        return "Ну нельзя так понимаешь, нельзя"
    if username_to_logout in users:
        del users[username_to_logout]
        return f"Ишак известный как {username_to_logout} покинул нас"
    else:
        return f"Ишак с ником {username_to_logout} не был обнаружен"


@app.route("/send")
def send():
    username = request.args.get('name')
    message = request.args.get('message')
    if message is None:
        return "Че дурак, писать разучился?"
    if username not in users:
        return "Нету такого, что ты мне рассказываешь"
    if username not in tokens:
        return "С монетой траблы, прости"
    else:
        timestamp = datetime.datetime.now().isoformat()
        msg_data = {"username": username, "message": message, "timestamp": timestamp}
        messages.append(msg_data)
        print(username, message)
        return f"{username}, {message}"


@app.route("/getall")
def getall():
    username = request.args.get('name')
    if username not in users:
        return Response("А ну пшел отсюда",content_type='text/plain; charset=utf-8')

    user_messages = [{"username": msg["username"], "message": msg["message"], "timestamp": msg["timestamp"]} for msg in messages]
    response_data = json.dumps(user_messages, ensure_ascii=False)
    return Response(response_data, content_type='application/json; charset=utf-8')


if __name__ == "__main__":
    print('ЛЕСГОУ')
    app.run(debug=True)