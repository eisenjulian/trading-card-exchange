import redis
import os

db = redis.from_url(os.environ.get("REDIS_URL"))

def get_user(id):
    return db.get('user:' + id) or {}

def set_user(user):
    db.set('user:' + user['id'], user)
