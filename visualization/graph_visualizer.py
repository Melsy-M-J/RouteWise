
import networkx as nx
import matplotlib.pyplot as plt


def draw_road_network(road_network, positions, path=None, title="Road Network"):

    # Create a drawing area
    plt.figure(figsize=(12, 9))

    # Draw all roads in grey
    nx.draw_networkx_edges(
        road_network,
        positions,
        edge_color="lightgray",
        width=1.5
    )

    # Draw all intersections in blue
    nx.draw_networkx_nodes(
        road_network,
        positions,
        node_color="skyblue",
        node_size=350
    )

    # Display intersection labels
    nx.draw_networkx_labels(
        road_network,
        positions,
        font_size=7
    )

    # Display road weights
    edge_labels = nx.get_edge_attributes(
        road_network,
        "weight"
    )

    nx.draw_networkx_edge_labels(
        road_network,
        positions,
        edge_labels=edge_labels,
        font_size=6
    )

    # Highlight the shortest path, if one exists
    if path:

        path_edges = list(zip(path, path[1:]))

        # Highlight the route in red
        nx.draw_networkx_edges(
            road_network,
            positions,
            edgelist=path_edges,
            edge_color="red",
            width=3.5
        )

        # Highlight the starting intersection in green
        nx.draw_networkx_nodes(
            road_network,
            positions,
            nodelist=[path[0]],
            node_color="green",
            node_size=450
        )

        # Highlight the destination in orange
        nx.draw_networkx_nodes(
            road_network,
            positions,
            nodelist=[path[-1]],
            node_color="orange",
            node_size=450
        )

    # Add title and display the graph
    plt.title(title, fontsize=16)

    plt.axis("off")

    plt.tight_layout()

    plt.show()
