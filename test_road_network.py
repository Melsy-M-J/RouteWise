
from data.graph_data import create_road_network
from algorithms.dijkstra import dijkstra
from algorithms.astar import astar


# Generate an 8 x 8 road network
road_network, graph, positions = create_road_network(
    rows=8,
    cols=8
)


# Define starting and destination intersections
start = (0, 0)
destination = (7, 7)


# Run Dijkstra
dijkstra_result = dijkstra(
    graph,
    start,
    destination
)


# Run A*
astar_result = astar(
    graph,
    start,
    destination,
    positions
)


print("========== ROAD NETWORK ==========")

print("Number of intersections:", road_network.number_of_nodes())

print("Number of roads:", road_network.number_of_edges())


print("\n========== DIJKSTRA RESULTS ==========")

print("Path:", dijkstra_result["path"])
print("Cost:", dijkstra_result["cost"])
print("Explored nodes:", len(dijkstra_result["explored_nodes"]))


print("\n========== A* RESULTS ==========")

print("Path:", astar_result["path"])
print("Cost:", astar_result["cost"])
print("Explored nodes:", len(astar_result["explored_nodes"]))


print("\n========== COMPARISON ==========")

print(
    "Both algorithms found the same cost:",
    dijkstra_result["cost"] == astar_result["cost"]
)
