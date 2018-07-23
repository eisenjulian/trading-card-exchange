import random
import src.database as db

for i in range(10):
    user_id = str(random.randint(10 ** 6, 2 * 10 ** 6))

    user = db.get_user(user_id)
    user['id'] = user_id

    cards = ['1104', '1136', '1163']
    random.shuffle(cards)
    db.add_wanted(user, cards[:1])
    db.add_collection(user, cards[1:])
