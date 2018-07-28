import requests
import traceback
import os
from src import dialog_manager
from src.utils import log
import messenger_sender

profile_cache = {}

def get_profile_data(user_id):
    if not user_id in profile_cache:
        url = "https://graph.facebook.com/v3.0/{user_id}?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token={token}".format(user_id=user_id, token=os.environ["PAGE_ACCESS_TOKEN"])
        r = requests.get(url)
        if r.status_code != 200:
            log('Problems getting profile data')
            log(r.status_code)
            log(r.text)
            return {'id': user_id}
        else:
            profile_cache[user_id] = r.json()
    return profile_cache[user_id]

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
                # someone sent us a message or clicked/tapped "postback" button
                if messaging_event.get("message") or messaging_event.get("postback"): 
                    try:
                        messaging_event['sender_data'] = get_profile_data(messaging_event['sender']['id'])
                        messages = dialog_manager.run(messaging_event)
                        messenger_sender.send_messages(messaging_event['sender'], messages)
                        # if batch_messages:
                        #     send_batch_messages(batch_messages)
                    except Exception:
                        log(traceback.format_exc())

    return "ok", 200