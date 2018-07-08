import database as db
import utils

IMAGE_URL = 'https://storage.googleapis.com/trading-card-exchange/figus/'

def pill(t, intent):
    return {'content_type': 'text', 'title': t(intent), 'payload': intent}

def button(t, intent):
    return {'type': 'postback', 'title': t(intent), 'payload': intent}    

def menu(t):
    return {
        'text': t('menu'),
        'quick_replies': [pill(t, '/trades'), pill(t, '/stickers'), pill(t, '/wishlist')]
    }

def show_collection(t, collection):
    return [{
        "attachment":{
            "type":"template",
            "payload":{
                "image_aspect_ratio": "square",
                "template_type":"generic",
                "elements": [
                    {
                        "image_url": IMAGE_URL + card['id'] + '.jpg',
                        "title": card.get('name', card['id']),
                        "subtitle": card.get('team', card['id']),
                        "buttons": [button(t, '/remove_from_collection')]
                    } for card in [utils.cards.get(card_id) for card_id in collection] if card
                ]
            }
        }
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
                        "buttons": [button(t, '/remove_from_wanted')]
                    } for card in [utils.cards.get(card_id) for card_id in wanted] if card
                ]
            }
        }
    }]