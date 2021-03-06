import networkx as nx
import database as db


def compute_match(start_user_id=None):
    print 'user id ', start_user_id
    graph = nx.DiGraph()
    for user_id in db.get_users():
        user = db.get_user(user_id)
        for card_id in user['wanted']:
            graph.add_edge(user_id, card_id)
        for card_id in user['collection']:
            graph.add_edge(card_id, user_id)
    cycles = nx.simple_cycles(graph)
    if start_user_id is None:
        return cycles
    for cycle in cycles:
        if start_user_id in cycle and len(cycle) > 2:
            return cycle
    return None
