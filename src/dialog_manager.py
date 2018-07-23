# -*- coding: UTF-8 -*-
import re
import utils
import texts
import database as db
import nlg
import matching
import json
from src.connectors import messenger_sender

def get_entities(message, postback, name):
    try:
        if postback:
            return [{
                'value': json.loads(postback['payload'])[name],
                'confidence': 1.0
            }]
        if 'quick_reply' in message:
            return [{
                'value': json.loads(message['quick_reply']['payload'])[name],
                'confidence': 1.0
            }]
        return message['nlp']['entities'][name]
    except (KeyError, IndexError, TypeError):
        return []


def get_intent(message, postback):
    intents = get_entities(message, postback, 'intent')
    return intents and intents[0]['confidence'] > 0.8 and intents[0]['value'] or None


def get_card_ids(message, postback):
    if 'attachments' in message:
        for attachment in message['attachments']:
            if attachment['type'] == 'image':
                return utils.get_stickers_from_image(attachment['payload']['url'])
    return list(set(
        [str(ent['value']) for ent in get_entities(message, postback, 'number')] +
        [s for s in message.get('text', '').split() if s.isdigit()] +
        utils.get_stickers_from_text([message.get('text')])
    ))


def find_match(t, sender):
    cycle = matching.compute_match(sender['id'])
    if cycle:
        db.add_transaction(sender, cycle)
        return nlg.new_trade(t)
    return []

def get_emoji(user_id):
    emojis = [u'🐶', u'🐱', u'🐭', u'🐹', u'🐰', u'🦊', u'🐻', u'🐼', u'🐨', u'🐯', u'🦁', u'🐮', u'🐷', u'🐸', u'🐵', u'🐔', u'🐧', u'🐦', u'🐤', u'🦆', u'🦅', u'🦉', u'🦇', u'🐺', u'🐗', u'🐴', u'🦄', u'🐝', u'🦋', u'🐌', u'🐞', u'🐢', u'🐍', u'🦎', u'🐙', u'🐠', u'🐬', u'🐳', u'🐊', u'🦓', u'🦏']
    return emojis[hash(user_id) % len(emojis)]

def send_batch_messages(messages):
    # this should enqueue this messages to be send by another process
    messenger_sender.send_batch_messages(messages)

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
    cards = get_card_ids(message, postback)

    if intent == 'start':
        return [{
            'text': t('welcome'),
            'quick_replies': [nlg.pill(t, 'add_sticker'), nlg.pill(t, 'add_wishlist')]
        }]

    elif intent == 'menu':
        return [nlg.menu(t)]

    elif intent == 'trades':
        return nlg.show_trades(t, sender.get('transactions'))

    elif intent == 'stickers':
        return nlg.show_collection(t, sender.get('collection'))

    elif intent == 'wishlist':
        return nlg.show_wanted(t, sender.get('wanted'))

    elif intent == 'add_sticker' or last_action == 'ask_sticker':
        if cards:
            db.add_collection(sender, cards)
            return [{'text': t('collection_changed')}] +\
                    nlg.show_collection(t, sender.get('collection')) +\
                    find_match(t, sender)
        sender['last_action'] = 'ask_sticker'
        return [{'text': t('ask_sticker')}]
    elif intent == 'add_wishlist' or last_action == 'ask_wishlist':
        if cards:
            db.add_wanted(sender, cards)
            return [{'text': t('wanted_changed')}] +\
                    nlg.show_wanted(t, sender.get('wanted')) +\
                    find_match(t, sender)
        sender['last_action'] = 'ask_wishlist'
        return [{'text': t('ask_wishlist')}]

    elif intent == 'talk' or intent == 'reply':
        transaction_id = get_entities(message, postback, 'id')[0]['value']
        sender['last_action'] = 'ask_message ' + transaction_id
        return [{'text': t('ask_message')}]

    elif intent == 'cancel_transaction':
        transaction_id = get_entities(message, postback, 'id')[0]['value']
        transaction = db.get_transaction(transaction_id)
        if 'finished' in transaction:
            # Not cancelable
            return [t('transaction_finished'), nlg.cta(t)]
        transaction['canceled'] = True
        db.set_transaction(transaction_id, transaction)
        db.add_one_wanted(sender, sender['transactions'][transaction_id]['get'])
        db.add_one_collection(sender, sender['transactions'][transaction_id]['put'])
        del sender['transactions'][transaction_id]
        sender['past_transactions'].append(transaction_id)
        return [t('transaction_canceled'), nlg.cta(t)]

    elif intent == 'finish_transaction':
        transaction_id = get_entities(message, postback, 'id')[0]['value']
        transaction = db.get_transaction(transaction_id)
        if 'canceled' in transaction:
            # Not finalizable
            return [t('transaction_canceled'), nlg.cta(t)]
        transaction['finished'] = True
        db.set_transaction(transaction_id, transaction)
        del sender['transactions'][transaction_id]
        sender['past_transactions'].append(transaction_id)
        return [t('transaction_finished'), nlg.cta(t)]

    elif intent == 'remove_sticker' or last_action == 'remove_sticker':
        if cards:
            db.remove_collection(sender, cards)
            return [{'text': t('collection_changed')}] +\
                    nlg.show_collection(t, sender.get('collection'))
        sender['last_action'] = 'remove_sticker'
        return [{'text': t('ask_sticker')}]

    elif intent == 'remove_wishlist' or last_action == 'remove_wishlist':
        if cards:
            db.remove_wanted(sender, cards)
            return [{'text': t('wanted_changed')}] +\
                    nlg.show_wanted(t, sender.get('wanted'))
        sender['last_action'] = 'remove_wishlist'
        return [{'text': t('ask_wishlist')}]

    elif 'ask_message' in (last_action or ''):
        transaction_id = last_action.split()[1]
        transaction = db.get_transaction(transaction_id)
        users = [user for user in transaction['cycle'] if user != sender['id'] and db.is_user(user)]
        batch_messages = {user: [
            {'text': get_emoji(sender['id']) + ' ' + t('message_received')},
            {'text': message['text'], 'quick_replies': [
                nlg.pill(t, 'reply', {'id': transaction_id})
            ]}
        ] for user in users}
        send_batch_messages(batch_messages)
        return [{'text': t('message_sent')}, nlg.cta(t)]

    elif intent == 'hi':
        return [{'text': t('hi')}, nlg.menu(t)]

    if message_text:
        return [{'text': t('roger')}]
