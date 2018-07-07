import utils
import texts
import database as db
import re

def get_entities_deprecated(message, name):
    nlp = message and  'nlp' in message and message['nlp'] or None
    return nlp and 'entities' in nlp and name in nlp['entities'] and nlp['entities'][name]

def get_entities(message, name):
    try:
        return message['nlp']['entities'][name]
    except KeyError:
        return []

def get_intent(message, postback):
    if postback:
        return postback['payload'][1:].split()[0]
    intent = get_entities(message, 'intent')[0]
    return intent and intent['value'] or None

def get_card_ids(message):
    if 'attachments' in message:
        for attachment in message['attachments']:
            if attachment['type'] == 'image':
                return [utils.get_stickers_from_image(attachment['payload']['url'])]
    return list(set(
        [str(ent['value']) for ent in get_entities(message, 'number')] +
        [s for s in message.get('text').split() if s.isdigit()] +
        utils.get_stickers_from_text([message.get('text')][0])
    ))

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
    def pill(intent):
        return {'content_type': 'text', 'title': t(intent), 'payload': intent}

    def menu():
        return {
            'text': t('menu'),
            'quick_replies': [pill('/trades'), pill('/stickers'), pill('/wishlist')]
        }


    if 'last_action' in sender:
        del sender['last_action']
    message_text = message.get('text')
    intent = get_intent(message, postback)

    if intent == 'start':
        return [{'text': t('welcome')}]
    elif intent == 'hi':
        return [{'text': t('hi')}, menu()]
    elif intent == 'menu':
        return [menu()]
    elif intent == 'trades':
        return [menu()]
    elif intent == 'add_sticker':
        cards = get_card_ids(message)
        if cards:
            db.add_wanted(sender, cards)
            return [{'text': t('wanted_changed')}]
        sender['last_action'] = 'ask_sticker'
        return [{'text': t('ask_sticker')}]
    elif intent == 'add_wishlist':
        cards = get_card_ids(message)
        if cards:
            db.add_collection(sender, cards)
            return [{'text': t('collection_changed')}]
        sender['last_action'] = 'ask_wishlist'
        return [{'text': t('ask_wishlist')}]
    elif intent == 'stickers':
        if sender.get('collection'):
            return [{'text': t('no_stickers'), 'quick_replies': [pill('/add_sticker')]}]
        else:
            return [{'text': t('no_stickers'), 'quick_replies': [pill('/add_sticker')]}]
            
    elif intent == 'wishlist':
        if sender.get('wanted'):
            return [{'text': t('no_wishlist'), 'quick_replies': [pill('/add_wishlist')]}]
        else:
            return [{'text': t('no_wishlist'), 'quick_replies': [pill('/add_wishlist')]}]
        # TODO: Render stickers
        # return db.db.hgetall(db.get_wanted_key(sender['id'])).keys() or [{'text': t('no_wishlist')}]

    if sender.get('last_action') == 'ask_sticker':
        cards = get_card_ids(message)
        if cards:
            db.add_collection(sender, cards)
            return [{'text': t('collection_changed')}]
        sender['last_action'] = 'ask_sticker'
        return [{'text': t('ask_sticker')}]

    if sender.get('last_action') == 'ask_wishlist':
        cards = get_card_ids(message)
        if cards:
            db.add_wanted(sender, cards)
            return [{'text': t('wanted_changed')}]
        sender['last_action'] = 'ask_wishlist'
        return [{'text': t('ask_wishlist')}]


    if message_text:
        return [{'text': t('roger')}]
