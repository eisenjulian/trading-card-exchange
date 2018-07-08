import os
import json
import redis
from hashlib import md5


db = redis.from_url(os.environ.get("REDIS_URL"))


def get_empty_user():
    return dict(wanted=[], collection=[], transactions=[])


def get_empty_card(id):
    return dict(id=id, whished=[], owners=[])


def get_users():
    return [key.split(':')[1] for key in db.keys('user:*')]


def get_cards():
    return [key.split(':')[1] for key in db.keys('card:*')]


def get_user(id):
    user = get_empty_user()
    user.update(json.loads(db.get('user:' + id) or '{}'))
    return user


def set_user(user):
    db.set('user:' + user['id'], json.dumps(user))


def get_card(id):
    card = get_empty_card(id)
    card.update(json.loads(db.get('card:' + id) or '{}'))
    return card


def set_card(card):
    db.set('card:' + card['id'], json.dumps(card))


def is_user(id):
    return int(id) > 1000


def add_wanted(user, wanted):
    for card in wanted:
        add_one_wanted(user, card)


def add_one_wanted(user, card_id):
    user['wanted'].append(card_id)
    card = get_card(card_id)
    card['whished'].append(user['id'])
    set_card(card)


def add_collection(user, collection):
    for card in collection:
        add_one_collection(user, card)


def add_one_collection(user, card_id):
    user['collection'].append(card_id)
    card = get_card(card_id)
    card['owners'].append(user['id'])
    set_card(card)


def add_transaction(transaction):
    transaction_id = md5(json.dumps(transaction)).hexdigest()
    db.set('transaction:{}'.format(transaction_id), json.dumps(transaction))
    offset = -1 if is_user(transaction[0]) else 0
    for i in xrange(offset, len(transaction), 2):
        user_id = transaction[i - 1]
        card_to_get_id = transaction[i]
        card_to_put_id = transaction[i - 2]
        add_user_transaction(
            get_user(user_id), card_to_put_id, card_to_get_id, transaction_id
        )

def get_transaction(id):
    return {'cycle': json.loads(db.get('transaction:' + id))}


def remove_if_exists(data, value):
    if value in data:
        data.remove(value)


def add_user_transaction(user, put, get, transaction_id):
    remove_if_exists(user['wanted'], get)
    remove_if_exists(user['collection'], put)
    card_to_put = get_card(put)
    remove_if_exists(card_to_put['owners'], user['id'])
    set_card(card_to_put)
    card_to_get = get_card(get)
    remove_if_exists(card_to_get['whished'], user['id'])
    set_card(card_to_get)
    user['transactions'].append(dict(put=put, get=get, id=transaction_id))
    set_user(user)
