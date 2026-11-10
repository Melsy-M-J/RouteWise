
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


def update_road_cost(road_network, graph, node1, node2, new_weight):

    # Road costs must be positive
    if new_weight < 1.00:
        raise ValueError("Road cost must be at least one.")

    # Check whether the road exists
    if not road_network.has_edge(node1, node2):
        raise ValueError("This road does not exist.")

    # Update the cost in NetworkX
    road_network[node1][node2]["weight"] = new_weight

    # Update the adjacency dictionary in both directions
    graph[node1][node2] = new_weight
    graph[node2][node1] = new_weight


def close_road(road_network, graph, node1, node2):

    # Check whether the road exists
    if not road_network.has_edge(node1, node2):
        raise ValueError("This road is already closed or does not exist.")

    # Remove the road from NetworkX
    road_network.remove_edge(node1, node2)

    # Remove the road from our algorithm's graph
    del graph[node1][node2]
    del graph[node2][node1]
