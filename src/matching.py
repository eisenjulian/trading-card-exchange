import networkx as nx
import attr
from collections import defaultdict


@attr.s
class Transaction(object):
    put = attr.ib(default=None)
    get = attr.ib(default=None)


class Matching(object):
    WANTED = 'wanted'
    OWNERS = 'owners'
    PUT = 'put'
    GET = 'get'

    def __init__(self, redis):
        self.redis = redis

    def add_wanted(self, user, wanted):
        for card in wanted:
            self.add_one_wanted(user, card)
        return self.compute_match(user)

    def add_one_wanted(self, user, card):
        self.redis.hset(self.get_wanted_key(user), card, 1)

    def get_wanted_key(self, user):
        return '{}:{}'.format(self.WANTED, user)

    def get_owners_key(self, card):
        return '{}:{}'.format(self.OWNERS, card)

    def get_put_key(self, user):
        return '{}:{}'.format(user, self.PUT)

    def get_get_key(self, user):
        return '{}:{}'.format(user, self.GET)

    def run_transaction(self, user, card, ttype, success):
        if ttype == self.GET:
            if success:
                self.redis.hdel(self.get_get_key(user), card)
            else:
                self.redis.hset(self.get_wanted_key(user), card, 1)
        if ttype == self.PUT:
            if success:
                self.redis.hdel(self.get_put_key(user), card)
            else:
                self.redis.hset(self.get_owners_key(user), card, 1)
        raise Exception('Error with transaction {} {} {} {}'.format(
            user, card, ttype, success
        ))

    def add_collection(self, user, collection):
        for card in collection:
            self.add_one_collection(user, card)
        return self.compute_match(user)

    def add_one_collection(self, user, card):
        self.redis.hset(self.get_owners_key(card), user, 1)

    def get_transactions_from_cycle(self, cycle):
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

    def compute_match(self, start_user=None):
        graph = nx.DiGraph()
        for key in self.redis.keys('{}:*'.format(self.WANTED)):
            _, user = key.split(':')
            for card, _ in self.redis.hgetall(key).iteritems():
                graph.add_edge(user, card)
        for key in self.redis.keys('{}:*'.format(self.OWNERS)):
            _, card = key.split(':')
            for user, _ in self.redis.hgetall(key).iteritems():
                graph.add_edge(card, user)
        if start_user is None:
            # TODO: Process output to generate exchanges
            return nx.simple_cycles(graph)
        try:
            transactions = self.get_transactions_from_cycle(
                nx.find_cycle(graph, start_user)
            )
            for user, transaction in transactions.iteritems():
                # Put the transaction in redis and mark the corresponding cards as
                # unavailable
                self.redis.hset(self.get_put_key(user), transaction.put, 1)
                self.redis.hdel(self.get_owners_key(user), transaction.put)
                self.redis.hset(self.get_get_key(user), transaction.get, 1)
                self.redis.hdel(self.get_wanted_key(user), transaction.get)
            return transactions
        except nx.exception.NetworkXNoCycle:
            return defaultdict(Transaction)
