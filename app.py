from src.connectors import messenger

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def messenger_verify():
    return messenger.verify(request)

@app.route('/', methods=['POST'])
def messenger_webhook():
    return messenger.webhook(request)

if __name__ == '__main__':
    app.run(debug=True)
