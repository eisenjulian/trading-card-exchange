import os
import sys
import time
import json
import unidecode
from datetime import datetime

import requests
from flask import Flask, request

app = Flask(__name__)

with open('cards.json') as f:
    cards = json.load(f)
    
def clean(string):
    return unidecode.unidecode(string).translate(None, '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~').lower().strip()

def find_card(lines):
    clean_lines = [clean(line) for line in lines]
    best_match = 'Nothing found!'
    score = 0
    for team, players in cards.iteritems():
        for player in players:
            for line in clean_lines:
                clean_player = clean(' '.join(player.split()[1:]))
                if len(line) > 4 and line in clean_player and len(line) > score:
                    log('Found match ' + line + ' in  '+ player) 
                    score = len(line)
                    best_match = team + ' ' + player
    return best_match
        

def get_image_text(url):
    image_data = requests.get(url)
    if image_data.status_code / 100 != 2:
        log('Problems getting image at URL ' + url + ' response: ' + image_data.text)
        return 'Nothing found'
    data = json.dumps({
        "requests": [{
            "image": {"content": image_data.content.encode('base64')},
            "features": [{"type": "TEXT_DETECTION"}]
        }]
    })
    response = requests.post('https://vision.googleapis.com/v1/images:annotate?fields=responses%2FfullTextAnnotation%2Ftext&key=' + os.environ['VISION_API_KEY'], data=data)
    log(response.text)
    if response.status_code / 100 != 2:
        log('Error calling Cloud Vision API: ' + response.text + ' for URL: ' + url)
        return 'Nothing found'
    lines = ('\n'.join(
        line['fullTextAnnotation']['text'] for line in response.json()['responses'] if 'fullTextAnnotation' in line
    )).split('\n')
    print lines
    return find_card(lines)

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message = messaging_event["message"]
                    if 'text' in message:
                        message_text = message["text"]  # the message's text
                        send_messages(sender_id, [{"text": "roger that!"}])
                    elif 'attachments' in message:
                        for attachment in message['attachments']:
                            if attachment['type'] == 'image':
                                send_messages(
                                    sender_id, 
                                    [{"text": get_image_text(attachment['payload']['url'])}]
                                )

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_messages(recipient_id, messages):
    log(u"sending message to {recipient}: {text}".format(recipient=recipient_id, text=json.dumps(messages)))
    params = {"access_token": os.environ["PAGE_ACCESS_TOKEN"]}
    headers = {"Content-Type": "application/json"}
    for message in messages:
        data = json.dumps({
            "recipient": {"id": recipient_id},
            "sender_action": "typing_on"
        })
        r = requests.post("https://graph.facebook.com/v3.0/me/messages", params=params, headers=headers, data=data)
        time.sleep(2)
        if r.status_code != 200:
            log(r.status_code)
            log(r.text)

        data = json.dumps({
            "recipient": {"id": recipient_id},
            "message": message
        })
        r = requests.post("https://graph.facebook.com/v3.0/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            log(r.status_code)
            log(r.text)


def log(msg):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg)
        print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
