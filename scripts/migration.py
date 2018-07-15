import redis
import json
import os
# import fakeredis

db = redis.from_url(os.environ.get("REDIS_URL"))

# Testing
# db = fakeredis.FakeStrictRedis()
#
# db.set(
#     'user:1',
#     '{\"profile_pic\": \"https://platform-lookaside.fbsbx.com/platform/profilepic/?psid=1979317408746429&width=1024&ext=1530919079&hash=AeSxjCo3Tv-8o8Y8\", \"id\": \"1979317408746429\", \"wanted\": [\"61\"], \"first_name\": \"Quimey\", \"last_name\": \"Vivas\", \"transactions\": [{\"get\": \"12\", \"id\": \"0a46d467f4bd5f99840d88351cb5e9e3\", \"put\": \"56\"}, {\"get\": \"12\", \"id\": \"0a46d467f4bd5f99840d88351cb5e9e3\", \"put\": \"56\"}], \"collection\": [\"24\", \"98\", \"77\", \"123\", \"123\", \"133\", \"144\", \"201\", \"88\", \"4\", \"38\"], \"timezone\": -3, \"gender\": \"male\", \"locale\": \"en_US\"}'
# )

# db.set(
#     'transaction:1',
#     '[\"1979317408746429\", \"56\", \"2122139661146635\", \"123\"]'
# )

for key in db.keys('transaction:*'):
    cycle = json.loads(db.get(key))
    db.set(key, json.dumps(dict(cycle=cycle)))

for key in db.keys('user:*'):
    user = json.loads(db.get(key))
    transactions = user['transactions']
    new_transactions = {
        transaction['id']: dict(put=transaction['put'], get=transaction['get'])
        for transaction in transactions
    }
    user['transactions'] = new_transactions
    db.set(key, json.dumps(user))

# print db.get('user:1')
# print db.get('transaction:1')
