from src.connectors import messenger
from src import texts
from src import nlg
from src import database as db

if __name__ == '__main__':
    sender = db.get_user('2122139661146635')
    t = texts.get_texts(sender)
    messenger.send_messages({'id': sender['id']}, nlg.show_collection(t, ['65', '78']))