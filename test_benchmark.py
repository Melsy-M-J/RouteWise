
from data.graph_data import create_road_network
from utils.benchmark import benchmark_algorithms


# Generate the road network
road_network, graph, positions = create_road_network(
    rows=8,
    cols=8
)


# Define start and destination
start = (0, 0)
destination = (7, 7)


# Benchmark both algorithms
results = benchmark_algorithms(
    graph,
    positions,
    start,
    destination,
    repetitions=30
)


print("========== ALGORITHM BENCHMARK ==========")

for algorithm, result in results.items():

    print(f"\n{algorithm}")

    print("Path cost:", result["cost"])

    print("Explored nodes:", result["explored_nodes"])

    print(
        "Average execution time:",
        round(result["average_time_ms"], 6),
        "ms"
    )

    print(
        "Median execution time:",
        round(result["median_time_ms"], 6),
        "ms"
    )


print("\n========== COMPARISON ==========")

print(
    "Same shortest-path cost:",
    results["Dijkstra"]["cost"] == results["A*"]["cost"]
)
