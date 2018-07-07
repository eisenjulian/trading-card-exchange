import re
import utils
import texts
import database as db
import nlg
import matching


def get_entities(message, name):
    try:
        return message['nlp']['entities'][name]
    except KeyError:
        return []


def get_intent(message, postback):
    if postback:
        return postback['payload'][1:].split()[0]
    intent = get_entities(message, 'intent')[0]
    return intent and intent['confidence'] > 0.8 and intent['value'] or None


def get_card_ids(message):
    if 'attachments' in message:
        for attachment in message['attachments']:
            if attachment['type'] == 'image':
                return utils.get_stickers_from_image(attachment['payload']['url'])
    return list(set(
        [str(ent['value']) for ent in get_entities(message, 'number')] +
        [s for s in message.get('text').split() if s.isdigit()] +
        utils.get_stickers_from_text([message.get('text')])
    ))


def run_match_and_answer(t, user_id, answer):
    transaction = matching.compute_match(user_id)
    print transaction
    response = [answer]
    if transaction:
        response.append({'text': t('new_transaction')})
        db.add_transaction(transaction)
    return response


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

    last_action = sender.get('last_action')
    if last_action:
        del sender['last_action']
    message_text = message.get('text')
    intent = get_intent(message, postback)

    if intent == 'start':
        return [{'text': t('welcome')}]
    elif intent == 'hi':
        return [{'text': t('hi')}, nlg.menu(t)]
    elif intent == 'menu':
        return [nlg.menu(t)]
    elif intent == 'trades':
        return [nlg.menu(t)]
    elif intent == 'add_sticker':
        cards = get_card_ids(message)
        if cards:
            db.add_collection(sender, cards)
            return run_match_and_answer(t, sender['id'], {'text': t('collection_changed')})
        sender['last_action'] = '/ask_sticker'
        return [{'text': t('/ask_sticker')}]
    elif intent == 'add_wishlist':
        cards = get_card_ids(message)
        if cards:
            db.add_wanted(sender, cards)
            return run_match_and_answer(t, sender['id'], {'text': t('wanted_changed')})
        sender['last_action'] = '/ask_wishlist'
        return [{'text': t('/ask_wishlist')}]
    elif intent == 'stickers':
        if sender.get('collection'):
            return nlg.show_collection(t, sender.get('collection'))
        else:
            return [{'text': t('no_stickers'), 'quick_replies': [nlg.pill(t, '/add_sticker')]}]

    elif intent == 'wishlist':
        if sender.get('wanted'):
            return nlg.show_wanted(t, sender.get('wanted'))
        else:
            return [{'text': t('no_wishlist'), 'quick_replies': [nlg.pill(t, '/add_wishlist')]}]

    if last_action == '/ask_sticker':
        cards = get_card_ids(message)
        if cards:
            db.add_collection(sender, cards)
            return run_match_and_answer(t, sender['id'], {'text': t('collection_changed')})
        sender['last_action'] = '/ask_sticker'
        return [{'text': t('/ask_sticker')}]

    if last_action == '/ask_wishlist':
        cards = get_card_ids(message)
        if cards:
            db.add_wanted(sender, cards)
            return run_match_and_answer(t, sender['id'], {'text': t('wanted_changed')})
        sender['last_action'] = '/ask_wishlist'
        return [{'text': t('/ask_wishlist')}]

    if message_text:
        return [{'text': t('roger')}]
