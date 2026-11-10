
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

from visualization.graph_visualizer import draw_road_network


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

    if selected_result["path"]:

        fig = draw_road_network(
            road_network,
            positions,
            path=selected_result["path"],
            title=selected_title,
            show=False
        )

        st.pyplot(fig)

        plt.close(fig)

        st.write("### Shortest Route")

        st.code(
            " → ".join(str(node) for node in selected_result["path"])
        )

    else:

        st.error("No route is available between these intersections.")


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
