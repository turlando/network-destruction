from pprint import pprint
from network_destruction.ranking import make_graph, distance_ranking


if __name__ == "__main__":
    graph = make_graph()
    pprint(distance_ranking(graph))
