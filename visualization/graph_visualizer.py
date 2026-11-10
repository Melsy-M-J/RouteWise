
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def draw_road_network(
    road_network,
    positions,
    path=None,
    explored_nodes=None,
    title="Road Network",
    show=True
):
    fig, ax = plt.subplots(figsize=(10, 8))

    if explored_nodes is None:
        explored_nodes = []

    if path is None:
        path = []

    # 1. Draw all roads
    nx.draw_networkx_edges(
        road_network,
        positions,
        edge_color="lightgray",
        width=1.5,
        ax=ax
    )

    # 2. Draw all intersections
    nx.draw_networkx_nodes(
        road_network,
        positions,
        node_color="lightgray",
        node_size=350,
        ax=ax
    )

    # 3. Draw intersection labels
    nx.draw_networkx_labels(
        road_network,
        positions,
        font_size=7,
        ax=ax
    )

    # 4. Draw explored intersections
    nx.draw_networkx_nodes(
        road_network,
        positions,
        nodelist=list(set(explored_nodes)),
        node_color="cornflowerblue",
        node_size=400,
        ax=ax
    )

    # 5. Draw the shortest route
    if path:
        path_edges = list(zip(path, path[1:]))

        nx.draw_networkx_edges(
            road_network,
            positions,
            edgelist=path_edges,
            edge_color="red",
            width=3,
            ax=ax
        )

        # Intermediate route intersections
        nx.draw_networkx_nodes(
            road_network,
            positions,
            nodelist=path[1:-1],
            node_color="red",
            node_size=400,
            ax=ax
        )

        # Starting intersection
        nx.draw_networkx_nodes(
            road_network,
            positions,
            nodelist=[path[0]],
            node_color="green",
            node_size=500,
            ax=ax
        )

        # Destination intersection
        nx.draw_networkx_nodes(
            road_network,
            positions,
            nodelist=[path[-1]],
            node_color="orange",
            node_size=500,
            ax=ax
        )

    # 6. Draw road costs LAST so they appear above route edges
    edge_labels = nx.get_edge_attributes(
        road_network, "weight"
    )

    nx.draw_networkx_edge_labels(
        road_network,
        positions,
        edge_labels=edge_labels,
        font_size=7,
        font_color="black",
        font_weight="bold",
        rotate=False,
        bbox={
            "facecolor": "white",
            "edgecolor": "none",
            "alpha": 0.85,
            "pad": 1
        },
        ax=ax
    )

    ax.set_title(title, fontsize=14)
    ax.axis("off")
    fig.tight_layout()

    if show:
        plt.show()

    return fig


def draw_shared_legend():

    legend_items = [
        Line2D(
            [0], [0],
            marker="o",
            color="w",
            markerfacecolor="lightgray",
            markersize=9,
            label="Unexplored"
        ),

        Line2D(
            [0], [0],
            marker="o",
            color="w",
            markerfacecolor="cornflowerblue",
            markersize=9,
            label="Explored"
        ),

        Line2D(
            [0], [0],
            marker="o",
            color="w",
            markerfacecolor="red",
            markersize=9,
            label="Shortest Route"
        ),

        Line2D(
            [0], [0],
            marker="o",
            color="w",
            markerfacecolor="green",
            markersize=9,
            label="Start"
        ),

        Line2D(
            [0], [0],
            marker="o",
            color="w",
            markerfacecolor="orange",
            markersize=9,
            label="Destination"
        )
    ]

    fig, ax = plt.subplots(figsize=(10, 1.2))

    ax.legend(
        handles=legend_items,
        loc="center",
        ncol=5,
        frameon=False,
        fontsize=10
    )

    ax.axis("off")
    fig.tight_layout()

    return fig
