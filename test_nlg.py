from src.connectors import messenger_sender
from src import texts
from src import nlg
from src import database as db

julian = '1760389324081001'
quimey = '1664422086988784'

if __name__ == '__main__':
    sender = db.get_user(quimey)
    # transaction_id = sender['transactions'][0]['id']
    # transaction = db.get_transaction(sender['transactions'][0]['id'])
    # print(transaction['cycle'][1::2])
    t = texts.get_texts(sender)
    messenger_sender.send_messages({'id': str(quimey)}, nlg.new_trade(t))
