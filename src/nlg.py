import database as db
import utils
import json

IMAGE_URL = 'https://storage.googleapis.com/trading-card-exchange/figus/'

def pill(t, intent, entities={}):
    return {'content_type': 'text', 'title': t(intent), 'payload': intent + ' ' + json.dumps(entities)}

def button(t, intent, entities={}):
    return {'type': 'postback', 'title': t(intent), 'payload': intent + ' ' + json.dumps(entities)}

def menu(t):
    return {
        'text': t('menu'),
        'quick_replies': [pill(t, '/trades'), pill(t, '/stickers'), pill(t, '/wishlist')]
    }

def show_trade(t, trades):
    return []


def show_collection(t, collection):
    return [{
        "attachment": {
            "type":"template",
            "payload": {
                "image_aspect_ratio": "square",
                "template_type":"generic",
                "elements": [
                    {
                        "image_url": IMAGE_URL + card['id'] + '.jpg',
                        "title": card.get('name', card['id']),
                        "subtitle": card.get('team', card['id']),
                        "buttons": [button(t, '/remove_from_collection', {'id': card['id']})]
                    } for card in [utils.cards.get(card_id) for card_id in collection] if card
                ]
            }
        },
        "quick_replies": [pill(t, '/add_sticker')]
    }]

def show_wanted(t, wanted):
    return [{
        "attachment":{
            "type": "template",
            "payload":{
                "image_aspect_ratio": "square",
                "template_type":"generic",
                "elements": [
                    {
                        "image_url": IMAGE_URL + card['id'] + '.jpg',
                        "title": card.get('name', card['id']),
                        "subtitle": card.get('team', card['id']),
                        "buttons": [button(t, '/remove_from_wanted', {'id': card['id']})]
                    } for card in [utils.cards.get(card_id) for card_id in wanted] if card
                ]
            }
        },
        "quick_replies": [pill(t, '/add_wishlist')]
    }]