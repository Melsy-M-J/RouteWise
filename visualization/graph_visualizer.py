
import networkx as nx
import matplotlib.pyplot as plt


def draw_road_network(
    road_network,
    positions,
    path=None,
    title="Road Network",
    show=True
):

    # Create the figure and drawing area
    fig, ax = plt.subplots(figsize=(12, 9))

    # Draw all roads
    nx.draw_networkx_edges(
        road_network,
        positions,
        edge_color="lightgray",
        width=1.5,
        ax=ax
    )

    # Draw all intersections
    nx.draw_networkx_nodes(
        road_network,
        positions,
        node_color="skyblue",
        node_size=350,
        ax=ax
    )

    # Display intersection labels
    nx.draw_networkx_labels(
        road_network,
        positions,
        font_size=7,
        ax=ax
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
        font_size=6,
        ax=ax
    )

    # Highlight the shortest path
    if path:

        path_edges = list(zip(path, path[1:]))

        nx.draw_networkx_edges(
            road_network,
            positions,
            edgelist=path_edges,
            edge_color="red",
            width=3.5,
            ax=ax
        )

        # Starting point
        nx.draw_networkx_nodes(
            road_network,
            positions,
            nodelist=[path[0]],
            node_color="green",
            node_size=450,
            ax=ax
        )

        # Destination
        nx.draw_networkx_nodes(
            road_network,
            positions,
            nodelist=[path[-1]],
            node_color="orange",
            node_size=450,
            ax=ax
        )

    ax.set_title(title, fontsize=16)
    ax.axis("off")

    fig.tight_layout()

    if show:
        plt.show()

    return fig
