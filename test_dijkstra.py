
from algorithms.dijkstra import dijkstra


# Create a sample road network
graph = {
    "A": {"B": 4, "C": 2},
    "B": {"A": 4, "C": 1, "D": 5},
    "C": {"A": 2, "B": 1, "D": 8, "E": 10},
    "D": {"B": 5, "C": 8, "E": 2},
    "E": {"C": 10, "D": 2}
}


# Find the shortest route from A to E
result = dijkstra(graph, "A", "E")


# Display the results
print("========== DIJKSTRA RESULTS ==========")

print("Shortest path:", " -> ".join(result["path"]))

print("Total path cost:", result["cost"])

print("Explored nodes:", result["explored_nodes"])

print("Number of explored nodes:", len(result["explored_nodes"]))
