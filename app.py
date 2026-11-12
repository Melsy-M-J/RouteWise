import pandas as pd
import streamlit as st
import time
import matplotlib.pyplot as plt

from data.graph_data import (
    create_road_network,
    update_road_cost,
    close_road
)

from algorithms.dijkstra import dijkstra
from algorithms.astar import astar

from visualization.graph_visualizer import (
    draw_road_network,
    draw_shared_legend
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="RouteWise",
    page_icon="🛣️",
    layout="wide"
)

st.title("🛣️ RouteWise")
st.subheader("Comparative Visualization of Shortest-Path Algorithms")

st.write(
    "Explore road networks, compare Dijkstra and A*, "
    "and observe how routes change when roads are updated."
)


# ==========================================
# CREATE AND STORE ROAD NETWORK
# ==========================================

if "road_network" not in st.session_state:

    road_network, graph, positions = create_road_network(
        rows=8,
        cols=8
    )

    st.session_state.road_network = road_network
    st.session_state.graph = graph
    st.session_state.positions = positions


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("Route Configuration")

graph = st.session_state.graph
road_network = st.session_state.road_network
positions = st.session_state.positions

nodes = list(graph.keys())

start = st.sidebar.selectbox(
    "Starting intersection",
    nodes,
    index=0
)

destination = st.sidebar.selectbox(
    "Destination intersection",
    nodes,
    index=len(nodes) - 1
)

algorithm_choice = st.sidebar.radio(
    "Select algorithm",
    ["Compare Both", "Dijkstra", "A*"]
)


# ==========================================
# ROUTE CALCULATION
# ==========================================

def calculate_route(algorithm_name):

    start_time = time.perf_counter()

    if algorithm_name == "Dijkstra":

        result = dijkstra(
            graph,
            start,
            destination
        )

    else:

        result = astar(
            graph,
            start,
            destination,
            positions
        )

    end_time = time.perf_counter()

    execution_time = (end_time - start_time) * 1000

    return result, execution_time


# ==========================================
# DISPLAY ROAD NETWORK
# ==========================================

st.header("Road Network")

st.write(
    f"Intersections: {road_network.number_of_nodes()} | "
    f"Roads: {road_network.number_of_edges()}"
)


# ==========================================
# RUN ALGORITHMS
# ==========================================

if start == destination:

    st.info("Choose different starting and destination intersections.")

else:

    dijkstra_result, dijkstra_time = calculate_route("Dijkstra")

    astar_result, astar_time = calculate_route("A*")

    selected_result = None
    selected_title = ""

    if algorithm_choice == "Dijkstra":

        selected_result = dijkstra_result
        selected_title = "Dijkstra Shortest Path"

    elif algorithm_choice == "A*":

        selected_result = astar_result
        selected_title = "A* Shortest Path"

    else:

        selected_result = dijkstra_result
        selected_title = "Dijkstra Shortest Path"

    # ======================================
    # METRICS
    # ======================================

    if algorithm_choice == "Compare Both":

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Dijkstra")

            st.metric(
                "Path Cost",
                round(dijkstra_result["cost"], 2)
            )

            st.metric(
                "Explored Nodes",
                len(dijkstra_result["explored_nodes"])
            )

            st.metric(
                "Execution Time",
                f"{dijkstra_time:.6f} ms"
            )

        with col2:

            st.subheader("A*")

            st.metric(
                "Path Cost",
                round(astar_result["cost"], 2)
            )

            st.metric(
                "Explored Nodes",
                len(astar_result["explored_nodes"])
            )

            st.metric(
                "Execution Time",
                f"{astar_time:.6f} ms"
            )

        if dijkstra_result["cost"] == astar_result["cost"]:

            st.success("Both algorithms found the same optimal path cost.")

        else:

            st.warning("The algorithms returned different path costs.")

    else:

        st.metric(
            "Path Cost",
            round(selected_result["cost"], 2)
        )

        st.metric(
            "Explored Nodes",
            len(selected_result["explored_nodes"])
        )

        execution_time = (
            dijkstra_time
            if algorithm_choice == "Dijkstra"
            else astar_time
        )

        st.metric(
            "Execution Time",
            f"{execution_time:.6f} ms"
        )

    # ======================================
    # VISUALIZATION
    # ======================================

    
    if algorithm_choice == "Compare Both":

        if dijkstra_result["path"] and astar_result["path"]:

            # Display both graphs side by side
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Dijkstra Shortest Path")

                fig1 = draw_road_network(
                    road_network,
                    positions,
                    path=dijkstra_result["path"],
                    explored_nodes=dijkstra_result["explored_nodes"],
                    title="Dijkstra Algorithm",
                    show=False
                )

                st.pyplot(fig1)
                plt.close(fig1)

                st.caption(
                    f"Path Cost: {dijkstra_result['cost']:.2f} | "
                    f"Explored Nodes: {len(dijkstra_result['explored_nodes'])}"
                )

            with col2:
                st.subheader("A* Shortest Path")

                fig2 = draw_road_network(
                    road_network,
                    positions,
                    path=astar_result["path"],
                    explored_nodes=astar_result["explored_nodes"],
                    title="A* Algorithm",
                    show=False
                )

                st.pyplot(fig2)
                plt.close(fig2)

                st.caption(
                    f"Path Cost: {astar_result['cost']:.2f} | "
                    f"Explored Nodes: {len(astar_result['explored_nodes'])}"
                )

            # Separate legend section BELOW both graphs
            st.divider()
            st.subheader("Graph Legend")

            legend_fig = draw_shared_legend()
            st.pyplot(legend_fig, width='stretch')
            plt.close(legend_fig)

        else:
            st.error("One or both algorithms could not find a route.")

    else:

        if selected_result["path"]:

            fig = draw_road_network(
                road_network,
                positions,
                path=selected_result["path"],
                explored_nodes=selected_result["explored_nodes"],
                title=selected_title,
                show=False
            )

            st.pyplot(fig)
            plt.close(fig)
            legend_fig = draw_shared_legend()
            st.pyplot(legend_fig, width='stretch')
            plt.close(legend_fig)

        else:
            st.error("No route is available between these intersections.")


    # ==========================================
    # PERFORMANCE COMPARISON
    # ==========================================

    st.divider()
    st.header("Algorithm Performance Comparison")

    dijkstra_nodes = len(dijkstra_result["explored_nodes"])
    astar_nodes = len(astar_result["explored_nodes"])

    # Calculate percentage reduction in explored nodes
    if dijkstra_nodes > 0:
        reduction = (
            (dijkstra_nodes - astar_nodes)
            / dijkstra_nodes
        ) * 100
    else:
        reduction = 0

    # Display explored-node comparison
    st.subheader("1. Explored Nodes Comparison")

    node_col1, node_col2 = st.columns(2)

    with node_col1:
        st.metric("Dijkstra Explored Nodes", dijkstra_nodes)

    with node_col2:
        st.metric("A* Explored Nodes", astar_nodes)

    st.bar_chart(
        {
            "Algorithm": ["Dijkstra", "A*"],
            "Explored Nodes": [dijkstra_nodes, astar_nodes]
        },
        x="Algorithm",
        y="Explored Nodes"
    )

    if reduction > 0:
        st.success(
            f"A* explored {reduction:.2f}% fewer nodes than Dijkstra."
        )
    elif reduction < 0:
        st.info(
            f"A* explored {abs(reduction):.2f}% more nodes than Dijkstra."
        )
    else:
        st.info("Both algorithms explored the same number of nodes.")

    # Execution-time comparison
    st.subheader("2. Execution Time Comparison")

    time_col1, time_col2 = st.columns(2)

    with time_col1:
        st.metric(
            "Dijkstra Execution Time",
            f"{dijkstra_time:.6f} ms"
        )

    with time_col2:
        st.metric(
            "A* Execution Time",
            f"{astar_time:.6f} ms"
        )

    st.bar_chart(
        {
            "Algorithm": ["Dijkstra", "A*"],
            "Execution Time (ms)": [
                dijkstra_time,
                astar_time
            ]
        },
        x="Algorithm",
        y="Execution Time (ms)"
    )

    # Shortest-path cost comparison
    st.subheader("3. Shortest Path Cost Comparison")

    st.write(
        f"Dijkstra Path Cost: {dijkstra_result['cost']:.2f}"
    )

    st.write(
        f"A* Path Cost: {astar_result['cost']:.2f}"
    )

    if abs(
        dijkstra_result["cost"] - astar_result["cost"]
    ) < 1e-9:
        st.success(
            "Both algorithms found routes with the same optimal cost."
        )
    else:
        st.warning(
            "The algorithms returned different path costs. "
            "Investigate their correctness before interpreting performance."
        )



# ==========================================
# DYNAMIC ROAD UPDATES
# ==========================================

st.divider()

st.header("Dynamic Road Management")

st.write(
    "Simulate traffic congestion or road closures "
    "and observe how the shortest route changes."
)

road_options = list(road_network.edges())

if road_options:

    selected_road = st.selectbox(
        "Select a road to update",
        road_options,
        format_func=lambda edge: f"{edge[0]} ↔ {edge[1]}"
    )

    col1, col2 = st.columns(2)

    with col1:

        new_weight = st.number_input(
            "New travel cost",
            min_value=1.00,
            value=10.0,
            step=1.0
        )

        if st.button("Update Road Cost"):

            update_road_cost(
                road_network,
                graph,
                selected_road[0],
                selected_road[1],
                new_weight
            )

            st.success("Road cost updated successfully.")

            st.rerun()

    with col2:

        if st.button("Close Selected Road"):

            close_road(
                road_network,
                graph,
                selected_road[0],
                selected_road[1]
            )

            st.success("Road closed successfully.")

            st.rerun()


# ==========================================
# RESET NETWORK
# ==========================================

st.divider()

if st.button("Reset Road Network"):

    road_network, graph, positions = create_road_network(
        rows=8,
        cols=8
    )

    st.session_state.road_network = road_network
    st.session_state.graph = graph
    st.session_state.positions = positions

    st.rerun()
