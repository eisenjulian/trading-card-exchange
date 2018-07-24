import random
import src.database as db

names = ['Mark', 'Carlos', 'Jose', 'Laura', 'Susan', 'Angela', 'John', 'Jane']
last_names = ['Fernandez', 'Smith', 'Rodriguez', 'Doe', 'Brown', 'Davis']


for i in range(50):
    user_id = str(random.randint(10 ** 6, 2 * 10 ** 6))

    user = db.get_user(user_id)
    user['id'] = user_id
    user['first_name'] = random.choice(names)
    user['last_name'] = random.choice(last_names)
    user['tester'] = True

    cards = ['1104', '1136', '1163']
    random.shuffle(cards)
    db.add_wanted(user, cards[:1])
    db.add_collection(user, cards[1:])
