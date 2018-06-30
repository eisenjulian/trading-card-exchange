import utils
import database as db

def run(messaging_event):
    sender = messaging_event['sender_data']
    sender.update(db.get_user(sender['id']))
    messages = process(messaging_event)
    db.set_user(sender)
    return messages

def process(messaging_event):
    message = messaging_event['message']
    if 'text' in message:
        message_text = message['text']  # the message's text
        return [{'text': 'roger that! ' + messaging_event['sender_data']['first_name']}]
    elif 'attachments' in message:
        for attachment in message['attachments']:
            if attachment['type'] == 'image':
                return [{'text': utils.get_image_text(attachment['payload']['url'])}]