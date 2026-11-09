
import time
import statistics

from algorithms.dijkstra import dijkstra
from algorithms.astar import astar


def benchmark_algorithms(
    graph,
    positions,
    start,
    destination,
    repetitions=30
):

    results = {}

    # Run each algorithm separately
    algorithms = {
        "Dijkstra": lambda: dijkstra(
            graph, start, destination
        ),

        "A*": lambda: astar(
            graph, start, destination, positions
        )
    }

    for name, algorithm in algorithms.items():

        execution_times = []

        # Run once before measuring to warm up
        algorithm()

        # Repeat the measurement
        for _ in range(repetitions):

            start_time = time.perf_counter()

            result = algorithm()

            end_time = time.perf_counter()

            elapsed_time = (end_time - start_time) * 1000

            execution_times.append(elapsed_time)

        # Calculate average and median execution time
        average_time = statistics.mean(execution_times)
        median_time = statistics.median(execution_times)

        results[name] = {
            "path": result["path"],
            "cost": result["cost"],
            "explored_nodes": len(result["explored_nodes"]),
            "average_time_ms": average_time,
            "median_time_ms": median_time
        }

    return results
