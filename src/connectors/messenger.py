from .. import dialog_manager
import time
import json
import requests
from ..utils import log

# when the endpoint is registered as a webhook, it must echo back
# the 'hub.challenge' value it receives in the query arguments
def verify(request):
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

def webhook(request):
	# endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):  # someone sent us a message
                    messages = dialog_manager.run(messaging_event)
                    send_messages(messages['sender'], messages)
                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

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
        time.sleep(2)
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
