import networkx as nx


class Matching(object):
    WANTED = 'wanted'
    OWNERS = 'owners'

    def __init__(self, redis):
        self.redis = redis

    def add_wanted(self, user, wanted):
        for card in wanted:
            self.add_one_wanted(user, card)
        return self.compute_match()

    def add_one_wanted(self, user, card):
        self.redis.hset(self.get_wanted_key(user), card, 1)

    def get_wanted_key(self, user):
        return '{}:{}'.format(self.WANTED, user)

    def get_owners_key(self, card):
        return '{}:{}'.format(self.OWNERS, card)

    def run_transaction(self, user1, user2, card):
        pass

    def add_collection(self, user, collection):
        for card in collection:
            self.add_one_collection(user, card)
        return self.compute_match()

    def add_one_collection(self, user, card):
        self.redis.hset(self.get_owners_key(card), user, 1)

    def compute_match(self):
        graph = nx.DiGraph()
        for key in self.redis.keys('{}:*'.format(self.WANTED)):
            _, user = key.split(':')
            for card, _ in self.redis.hgetall(key).iteritems():
                graph.add_edge(user, card)
        for key in self.redis.keys('{}:*'.format(self.OWNERS)):
            _, card = key.split(':')
            for user, _ in self.redis.hgetall(key).iteritems():
                graph.add_edge(card, user)
        return nx.simple_cycles(graph)
