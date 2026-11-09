
from data.graph_data import create_road_network
from algorithms.dijkstra import dijkstra
from visualization.graph_visualizer import draw_road_network


# Generate the road network
road_network, graph, positions = create_road_network(
    rows=8,
    cols=8
)


# Set starting and destination intersections
start = (0, 0)
destination = (7, 7)


# Calculate the shortest path
result = dijkstra(
    graph,
    start,
    destination
)


# Display the road network and shortest path
draw_road_network(
    road_network,
    positions,
    path=result["path"],
    title="RouteWise - Dijkstra Shortest Path"
)
