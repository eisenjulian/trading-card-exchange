import os
import json
import redis
from hashlib import md5


db = redis.from_url(os.environ.get("REDIS_URL"))


def get_empty_user():
    return dict(
        wanted=[], collection=[], transactions={}, past_transactions=[]
    )


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
    return int(id) > 10000


def add_wanted(user, wanted):
    for card in wanted:
        add_one_wanted(user, card)


def add_one_wanted(user, card_id):
    user['wanted'].append(card_id)
    set_user(user)
    card = get_card(card_id)
    card['whished'].append(user['id'])
    set_card(card)


def remove_wanted(user, wanted):
    for card in wanted:
        remove_one_wanted(user, card)


def remove_one_wanted(user, card_id):
    remove_if_exists(user['wanted'], card_id)
    set_user(user)
    card = get_card(card_id)
    remove_if_exists(card['whished'], user['id'])
    set_card(card)


def add_collection(user, collection):
    for card in collection:
        add_one_collection(user, card)


def add_one_collection(user, card_id):
    user['collection'].append(card_id)
    set_user(user)
    card = get_card(card_id)
    card['owners'].append(user['id'])
    set_card(card)


def remove_collection(user, collection):
    for card in collection:
        remove_one_collection(user, card)


def remove_one_collection(user, card_id):
    remove_if_exists(user['collection'], card_id)
    set_user(user)
    card = get_card(card_id)
    remove_if_exists(card['whished'], user['id'])
    set_card(card)


def get_repr(cycle):
    """This representation of cycles should be unique"""
    m_id = min(cycle)
    idx = cycle.index(m_id)
    return str(cycle[idx:] + cycle[:idx])


def add_transaction(t, user, cycle):
    print cycle
    transaction = dict(cycle=cycle)
    transaction_id = md5(get_repr(cycle)).hexdigest()
    db.set('transaction:{}'.format(transaction_id), json.dumps(transaction))
    offset = -1 if is_user(cycle[0]) else 0
    all_users = {}
    all_users[user['id']] = user
    for i in xrange(offset, len(cycle) + offset, 2):
        user_id = cycle[i - 1]
        print i, user_id
        card_to_get_id = cycle[i]
        card_to_put_id = cycle[i - 2]
        if user['id'] == user_id:
            add_user_transaction(
                user, card_to_put_id, card_to_get_id, transaction_id
            )
        else:
            all_users[user_id] = get_user(user_id)
            add_user_transaction(
                all_users[user_id], card_to_put_id,
                card_to_get_id, transaction_id
            )
    return transaction_id, get_transaction_desc(t, cycle, user, all_users)

def get_transaction_desc(t, cycle, user, all_users):
    def get_user_name(i):
        user_id = cycle[i]
        user_data = all_users.get(user_id, {})
        return user_data.get('first_name', '?')

    offset = -1 if is_user(cycle[0]) else 0
    return [
        t(
            'transaction_line' + 
            '_from_you' if cycle[i - 3] == user['id'] else ('_to_you' if cycle[i - 1] == user['id'] else ''), 
            name_from=get_user_name(i - 3), 
            name_to=get_user_name(i - 1), 
            card=utils.cards.get(cycle[i - 2], {}).get('name', cycle[i - 2])
        ) for i in xrange(offset, len(cycle) + offset, 2)
    ]

def get_transaction(id):
    return json.loads(db.get('transaction:' + id))


def set_transaction(id, transaction):
    db.set('transaction:' + id, json.dumps(transaction))


def remove_if_exists(data, value):
    if value in data:
        data.remove(value)


def add_user_transaction(user, put, get, transaction_id):
    print user, put, get
    remove_if_exists(user['wanted'], get)
    remove_if_exists(user['collection'], put)
    card_to_put = get_card(put)
    remove_if_exists(card_to_put['owners'], user['id'])
    set_card(card_to_put)
    card_to_get = get_card(get)
    remove_if_exists(card_to_get['whished'], user['id'])
    set_card(card_to_get)
    user['transactions'][transaction_id] = dict(put=put, get=get)
    set_user(user)
