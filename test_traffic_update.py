
from data.graph_data import (
    create_road_network,
    update_road_cost
)

from algorithms.dijkstra import dijkstra
from algorithms.astar import astar


# Generate the road network
road_network, graph, positions = create_road_network(
    rows=8,
    cols=8
)

start = (0, 0)
destination = (7, 7)


# Find the original route
original = dijkstra(graph, start, destination)

print("Original path:", original["path"])
print("Original cost:", original["cost"])


# Select a road on the original route
road_start = original["path"][0]
road_end = original["path"][1]


# Simulate heavy traffic by increasing its cost
old_weight = graph[road_start][road_end]

new_weight = old_weight + 20

update_road_cost(
    road_network,
    graph,
    road_start,
    road_end,
    new_weight
)


print("\nTraffic update:")
print("Road:", road_start, "to", road_end)
print("Old cost:", old_weight)
print("New cost:", new_weight)


# Recalculate both routes
dijkstra_result = dijkstra(graph, start, destination)

astar_result = astar(
    graph,
    start,
    destination,
    positions
)


print("\n========== AFTER TRAFFIC UPDATE ==========")

print("Dijkstra path:", dijkstra_result["path"])
print("Dijkstra cost:", dijkstra_result["cost"])

print("A* path:", astar_result["path"])
print("A* cost:", astar_result["cost"])

print(
    "\nSame optimal cost:",
    dijkstra_result["cost"] == astar_result["cost"]
)
