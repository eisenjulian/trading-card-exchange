import os
import json
import redis


db = redis.from_url(os.environ.get("REDIS_URL"))

WANTED = 'wanted'
OWNERS = 'owners'
PUT = 'put'
GET = 'get'


def get_user(id):
    return json.loads(db.get('user:' + id) or '{}')


def set_user(user):
    db.set('user:' + user['id'], json.dumps(user))


def add_wanted(user, wanted):
    for card in wanted:
        add_one_wanted(user, card)


def add_one_wanted(user, card):
    db.hset(get_wanted_key(user), card, 1)


def get_wanted_key(user):
    return '{}:{}'.format(WANTED, user)


def get_owners_key(card):
    return '{}:{}'.format(OWNERS, card)


def get_put_key(user):
    return '{}:{}'.format(user, PUT)


def get_get_key(user):
    return '{}:{}'.format(user, GET)


def add_collection(user, collection):
    for card in collection:
        add_one_collection(user, card)


def add_one_collection(user, card):
    db.hset(get_owners_key(card), user, 1)


def get_keys_for_wanted():
    return db.keys('{}:*'.format(WANTED))


def get_keys_for_owners():
    return db.keys('{}:*'.format(OWNERS))
