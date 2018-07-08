from src.connectors import messenger
from src import texts
from src import nlg
from src import database as db

julian = '2122139661146635'
quimey = '1979317408746429'

if __name__ == '__main__':
    sender = db.get_user(quimey)
    t = texts.get_texts(sender)
    messenger.send_messages(
        {'id': sender['id']}, nlg.show_trades(t, sender['transactions'])
    )
