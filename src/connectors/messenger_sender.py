import time
import json
import requests
import os
from src.utils import log

def send_messages(recipient, messages):
    log(u"sending message to {recipient}: {text}".format(recipient=recipient['id'], text=json.dumps(messages)))
    params = {"access_token": os.environ["PAGE_ACCESS_TOKEN"]}
    headers = {"Content-Type": "application/json"}
    for message in messages:
        data = json.dumps({
            "recipient": recipient,
            "sender_action": "typing_on"
        })
        r = requests.post("https://graph.facebook.com/v3.0/me/messages", params=params, headers=headers, data=data)
        time.sleep(1)
        if r.status_code != 200:
            log(r.status_code)
            log(r.text)

        data = json.dumps({
            "recipient": recipient,
            "message": message
        })
        r = requests.post("https://graph.facebook.com/v3.0/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            log(r.status_code)
            log(r.text)
