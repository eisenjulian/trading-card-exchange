import utils
import texts
import database as db

def first_entity(message, name):
    nlp = message and  'nlp' in message and message['nlp'] or None
    return nlp and name in nlp and nlp[name][0] or None

def get_intent(message, postback):
    if postback:
        return postback['payload'][1:].split()[0]
    intent = first_entity(message, 'intent')
    return intent and intent['value'] or None


def run(messaging_event):
    sender = messaging_event['sender_data']
    sender.update(db.get_user(sender['id']))
    messages = process(messaging_event)
    db.set_user(sender)
    return messages

def process(messaging_event):
    message = messaging_event['message'] if 'message' in messaging_event else {}
    postback = messaging_event['postback'] if 'postback' in messaging_event else None
    sender = messaging_event['sender_data']

    t = texts.get_texts(sender)
    menu = {
        'text': t('menu'), 
        'quick_replies': [
            {'title': t('/trades'), 'type': 'postback', 'payload': '/trades'},
            {'title': t('/stickers'), 'type': 'postback', 'payload': '/stickers'},
            {'title': t('/wishlist'), 'type': 'postback', 'payload': '/wishlist'}
        ]
    }

    message_text = message and message['text'] if 'text' in message else None
    intent = get_intent(message, postback)

    if intent == 'start':
        return [{'text': t('welcome')}]
    elif intent  == 'hi':
        return [{'text': t('hi')}, menu]
    elif intent  == 'menu':
        return [menu]
    elif intent  == 'trades':
        return [menu]
    elif intent  == 'stickers':
        return [menu]
    elif intent  == 'wishlist':
        return [menu]


    elif message_text:
        return [{'text': t('roger')}]
    elif 'attachments' in message:
        for attachment in message['attachments']:
            if attachment['type'] == 'image':
                return [{'text': utils.get_image_text(attachment['payload']['url'])}]