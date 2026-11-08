
import heapq
import math


def heuristic(node, destination, positions):

    # Calculate straight-line distance between two nodes
    x1, y1 = positions[node]
    x2, y2 = positions[destination]

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def astar(graph, start, destination, positions):

    # Store the cheapest known cost from start to each node
    g_score = {node: float("inf") for node in graph}

    g_score[start] = 0

    # Remember the previous node for path reconstruction
    previous = {}

    # Priority queue: (estimated total cost, actual cost, node)
    priority_queue = [(0, 0, start)]

    # Track explored nodes
    explored_nodes = []

    while priority_queue:

        # Get the node with the lowest estimated total cost
        f_score, current_g, current_node = heapq.heappop(
            priority_queue
        )

        # Ignore outdated entries
        if current_g > g_score[current_node]:
            continue

        explored_nodes.append(current_node)

        # Stop when the destination is reached
        if current_node == destination:
            break

        # Check neighbouring nodes
        for neighbor, weight in graph[current_node].items():

            # Calculate the actual cost to reach this neighbour
            tentative_g = current_g + weight

            # Check whether this route is better
            if tentative_g < g_score[neighbor]:

                g_score[neighbor] = tentative_g

                previous[neighbor] = current_node

                # Estimate the remaining distance
                h_score = heuristic(
                    neighbor,
                    destination,
                    positions
                )

                # Calculate estimated total cost
                f_score = tentative_g + h_score

                heapq.heappush(
                    priority_queue,
                    (f_score, tentative_g, neighbor)
                )

    # Reconstruct the shortest path
    path = []

    if g_score[destination] != float("inf"):

        current = destination

        while current != start:
            path.append(current)
            current = previous[current]

        path.append(start)
        path.reverse()

    return {
        "path": path,
        "cost": g_score[destination],
        "explored_nodes": explored_nodes
    }
