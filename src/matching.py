import networkx as nx
import database as db


def compute_match(start_user_id=None):
    graph = nx.DiGraph()
    for user_id in db.get_users():
        user = db.get_user(user_id)
        for card_id in user['wanted']:
            graph.add_edge(user_id, card_id)
    for card_id in db.get_cards():
        card = db.get_card(card_id)
        for user_id in card['owners']:
            graph.add_edge(card_id, user_id)
    if start_user_id is None:
        # TODO: Process output to generate exchanges
        return nx.simple_cycles(graph)
    try:
        return db.add_transaction(nx.find_cycle(graph, start_user_id))
    except nx.exception.NetworkXNoCycle:
        return None
