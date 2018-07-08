from src.connectors import messenger_sender
from src import texts
from src import nlg
from src import database as db

julian = '2122139661146635'
quimey = '1979317408746429'

if __name__ == '__main__':
    sender = db.get_user(julian)
    # transaction = db.get_transaction(sender['transactions'][0]['id'])
    # print(transaction['cycle'][1::2])
    t = texts.get_texts(sender)
    messenger_sender.send_messages(
        {'id': sender['id']}, nlg.show_trades(t, sender['transactions'])
    )
