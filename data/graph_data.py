
import networkx as nx
import random


def create_road_network(rows=8, cols=8, seed=42):

    # Create a random number generator
    rng = random.Random(seed)

    # Create an empty road network
    road_network = nx.grid_2d_graph(rows, cols)

    # Assign a travel cost to every road
    for node1, node2 in road_network.edges():

        road_network[node1][node2]["weight"] = round(
            rng.uniform(1, 5), 2
        )

    # Store coordinates of each intersection
    positions = {
        node: (node[1], node[0])
        for node in road_network.nodes()
    }

    # Convert NetworkX graph into the format
    # expected by our Dijkstra and A* functions
    adjacency_graph = {
        node: {
            neighbor: details["weight"]
            for neighbor, details in road_network[node].items()
        }
        for node in road_network.nodes()
    }

    return road_network, adjacency_graph, positions
