
from data.graph_data import (
    create_road_network,
    update_road_cost,
    close_road
)

from algorithms.dijkstra import dijkstra
from algorithms.astar import astar

from visualization.graph_visualizer import draw_road_network


# Step 1: Generate the road network
road_network, graph, positions = create_road_network(
    rows=8,
    cols=8
)

start = (0, 0)
destination = (7, 7)


# Step 2: Find the original shortest route
original_result = dijkstra(
    graph,
    start,
    destination
)

print("========== ORIGINAL ROUTE ==========")

print("Path:", original_result["path"])
print("Cost:", original_result["cost"])


# Step 3: Select a road from the original route
original_path = original_result["path"]

road_start = original_path[0]
road_end = original_path[1]


# Step 4: Close that road
print("\nClosing road:", road_start, "to", road_end)

close_road(
    road_network,
    graph,
    road_start,
    road_end
)


# Step 5: Calculate the new route using Dijkstra
new_dijkstra_result = dijkstra(
    graph,
    start,
    destination
)


# Step 6: Calculate the new route using A*
new_astar_result = astar(
    graph,
    start,
    destination,
    positions
)


print("\n========== AFTER ROAD CLOSURE ==========")

print("\nDIJKSTRA")

print("New path:", new_dijkstra_result["path"])
print("New cost:", new_dijkstra_result["cost"])


print("\nA*")

print("New path:", new_astar_result["path"])
print("New cost:", new_astar_result["cost"])


print("\n========== COMPARISON ==========")

print(
    "Both algorithms found the same cost:",
    new_dijkstra_result["cost"] == new_astar_result["cost"]
)


# Step 7: Visualize the new route
draw_road_network(
    road_network,
    positions,
    path=new_dijkstra_result["path"],
    title="RouteWise - Route After Road Closure"
)
