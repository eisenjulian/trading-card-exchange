import redis

db = redis.from_url(os.environ.get("REDIS_URL"))