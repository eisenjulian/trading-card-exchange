import utils
import json
from itertools import islice

IMAGE_URL = 'https://storage.googleapis.com/trading-card-exchange/cartoon/'

def pill(t, intent, entities={}):
    payload = {'intent': intent}
    payload.update(entities)
    return {'content_type': 'text', 'title': t(intent), 'payload': json.dumps(payload)}

def button(t, intent, entities={}):
    payload = {'intent': intent}
    payload.update(entities)
    return {'type': 'postback', 'title': t(intent), 'payload': json.dumps(payload)}

def menu(t):
    return {
        'text': t('menu'),
        'quick_replies': [pill(t, 'trades'), pill(t, 'stickers'), pill(t, 'wishlist')]
    }

def cta(t):
    return {
        'text': t('cta'),
        'quick_replies': [pill(t, 'trades'), pill(t, 'stickers'), pill(t, 'wishlist')]
    }

def show_collection(t, collection):
    if not collection:
        return [{'text': t('no_stickers'), 'quick_replies': [pill(t, 'add_sticker')]}]
    return [{
        "attachment": {
            "type": "template",
            "payload": {
                "image_aspect_ratio": "square",
                "template_type": "generic",
                "elements": [
                    {
                        "image_url": IMAGE_URL + card['id'] + '.jpg',
                        "title": card.get('name', card['id']),
                        "subtitle": card.get('team', card['id']),
                        "buttons": [button(t, 'remove_sticker', {'number': card['id']})]
                    } for card in [utils.cards.get(card_id) for card_id in collection[-10:]] if card
                ]
            }
        },
        "quick_replies": [pill(t, 'add_sticker')]
    }]

def show_wanted(t, wanted):
    if not wanted:
        return [{'text': t('no_wishlist'), 'quick_replies': [pill(t, 'add_wishlist')]}]
    return [{
        "attachment": {
            "type": "template",
            "payload": {
                "image_aspect_ratio": "square",
                "template_type": "generic",
                "elements": [
                    {
                        "image_url": IMAGE_URL + card['id'] + '.jpg',
                        "title": card.get('name', card['id']),
                        "subtitle": card.get('team', card['id']),
                        "buttons": [button(t, 'remove_wishlist', {'number': card['id']})]
                    } for card in [utils.cards.get(card_id) for card_id in wanted[-10:]] if card
                ]
            }
        },
        "quick_replies": [pill(t, 'add_wishlist')]
    }]

def show_trades(t, trades):
    if not trades:
        return [{'text': t('no_trades'), 'quick_replies': [pill(t, 'add_wishlist'), pill(t, 'add_sticker')]}]
    return [{
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": t(
                            'trade',
                            card_get=card_get.get('name', card_get['id']),
                            card_put=card_put.get('name', card_put['id'])
                        ),
                        "buttons": [
                            button(t, 'cancel_transaction', {'id': transaction_id}),
                            button(t, 'finish_transaction', {'id': transaction_id}),
                            button(t, 'talk', {'id': transaction_id})
                        ]
                    }
                    for card_get, card_put in [
                        (utils.cards.get(transaction['get']), utils.cards.get(transaction['put']))
                        for transaction_id, transaction in islice(10, trades.iteritems())
                    ] if card_get and card_put
                ]
            }
        }
    }]
