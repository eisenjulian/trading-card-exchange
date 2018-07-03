import networkx as nx
import attr
from collections import defaultdict
import database as db


@attr.s
class Transaction(object):
    put = attr.ib(default=None)
    get = attr.ib(default=None)


def run_transaction(user, card, ttype, success):
    if ttype == db.GET:
        if success:
            db.db.hdel(db.get_get_key(user), card)
        else:
            db.db.hset(db.get_wanted_key(user), card, 1)
    if ttype == db.PUT:
        if success:
            db.db.hdel(db.get_put_key(user), card)
        else:
            db.db.hset(db.get_owners_key(user), card, 1)
    raise Exception('Error with transaction {} {} {} {}'.format(
        user, card, ttype, success
    ))


def get_transactions_from_cycle(cycle):
    transactions = defaultdict(Transaction)
    for i, edge in enumerate(cycle):
        if i % 2 == 0:
            # user -> card
            user, card = edge
            transactions[user].put = card
        if i % 2 == 1:
            # card -> user
            card, user = edge
            transactions[user].get = card
    return transactions


def compute_match(start_user=None):
    graph = nx.DiGraph()
    for key in db.get_keys_for_wanted():
        _, user = key.split(':')
        for card, _ in db.db.hgetall(key).iteritems():
            graph.add_edge(user, card)
    for key in db.get_keys_for_owners():
        _, card = key.split(':')
        for user, _ in db.db.hgetall(key).iteritems():
            graph.add_edge(card, user)
    if start_user is None:
        # TODO: Process output to generate exchanges
        return nx.simple_cycles(graph)
    try:
        transactions = get_transactions_from_cycle(
            nx.find_cycle(graph, start_user)
        )
        for user, transaction in transactions.iteritems():
            # Put the transaction in db and mark the corresponding cards
            # as unavailable
            db.db.hset(db.get_put_key(user), transaction.put, 1)
            db.db.hdel(db.get_owners_key(user), transaction.put)
            db.db.hset(db.get_get_key(user), transaction.get, 1)
            db.db.hdel(db.get_wanted_key(user), transaction.get)
        return transactions
    except nx.exception.NetworkXNoCycle:
        return defaultdict(Transaction)
