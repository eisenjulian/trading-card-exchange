import utils
import texts
import database as db

def run(messaging_event):
    sender = messaging_event['sender_data']
    sender.update(db.get_user(sender['id']))
    messages = process(messaging_event)
    db.set_user(sender)
    return messages

def process(messaging_event):
    message = messaging_event['message']
    postback = messaging_event['postback']
    sender = messaging_event['sender_data']

    t = texts.get_texts(sender)

    message_text = message and message['text'] or None
    postback_payload = postback and postback['payload'] or None

    if postback_payload == '/start':
        return [{'text': t('welcome')}]
    elif 'text' in message:
        message_text = message['text']  # the message's text
        return [{'text': t('roger')}]
    elif 'attachments' in message:
        for attachment in message['attachments']:
            if attachment['type'] == 'image':
                return [{'text': utils.get_image_text(attachment['payload']['url'])}]