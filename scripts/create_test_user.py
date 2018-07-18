import random
import src.database as db


user_id = str(random.randint(10 ** 6, 2 * 10 ** 6))

user = db.get_user(user_id)
user['id'] = user_id

db.add_wanted(user, map(str, range(1, 101)))
db.add_collection(user, map(str, range(101, 201)))
