import os
import json
import redis
from hashlib import md5


db = redis.from_url(os.environ.get("REDIS_URL"))


def get_empty_user():
    return dict(wanted=[], collection=[])


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
    transaction_id = md5(json.dumps(transaction)).hexdigest
    db.set('transaction:{}'.format(transaction_id), json.dumps(transaction))
    for i in xrange(0, len(transaction), 2):
        user_id = transaction[i]
        card_to_get_id = transaction[i + 1]
        card_to_put_id = transaction[i - 1]
        add_user_transaction(
            get_user(user_id), card_to_put_id, card_to_get_id, transaction_id
        )


def add_user_transaction(user, put, get, transaction_id):
    user['wanted'].remove(get)
    user['collection'].remove(put)
    card_to_put = get_card(put)
    card_to_put['owners'].remove(user['id'])
    set_card(card_to_put)
    card_to_get = get_card(get)
    card_to_get['whished'].remove(user['id'])
    set_card(card_to_get)
    user['transactions'].append(dict(put=put, get=get, id=transaction_id))
    set_user(user)
