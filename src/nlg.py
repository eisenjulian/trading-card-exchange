import database as db

def pill(t, intent):
    return {'content_type': 'text', 'title': t(intent), 'payload': intent}

def button(t, intent):
    return {'type': 'postback', 'title': t(intent), 'payload': intent}    

def menu(t):
    return {
        'text': t('menu'),
        'quick_replies': [pill('/trades'), pill('/stickers'), pill('/wishlist')]
    }

def show_collection(t, collection):
    return [{
        "attachment":{
            "type":"template",
            "payload":{
                "template_type":"generic",
                "elements": [
                    {
                        "title": card.get('name', card['id']),
                        "subtitle": card.get('desc', card['id']),
                        "buttons": [button(t, '/remove_from_collection')]
                    } for card in [db.get_card(card_id) for card_id in collection]
                ]
            }
        }
    }]

def show_wanted(t, wanted):
    return [{
        "attachment":{
            "type":"template",
            "payload":{
                "template_type":"generic",
                "elements": [
                    {
                        "title": card.get('name', card['id']),
                        "subtitle": card.get('desc', card['id']),
                        "buttons": [button(t, '/remove_from_wanted')]
                    } for card in [db.get_card(card_id) for card_id in wanted]
                ]
            }
        }
    }]