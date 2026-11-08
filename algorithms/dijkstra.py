
import heapq


def dijkstra(graph, start, destination):

    # Step 1: Store the shortest known distance to each node
    distances = {node: float("inf") for node in graph}

    # Distance from the starting node to itself is zero
    distances[start] = 0

    # Store the previous node to reconstruct the shortest path
    previous = {}

    # Priority queue: (distance, node)
    priority_queue = [(0, start)]

    # Keep track of nodes that have been explored
    explored_nodes = []

    # Step 2: Continue until there are no nodes left to explore
    while priority_queue:

        # Get the node with the smallest distance
        current_distance, current_node = heapq.heappop(priority_queue)

        # Ignore outdated entries in the priority queue
        if current_distance > distances[current_node]:
            continue

        # Record the explored node
        explored_nodes.append(current_node)

        # Stop when we reach the destination
        if current_node == destination:
            break

        # Step 3: Check all neighbouring nodes
        for neighbor, weight in graph[current_node].items():

            # Calculate the distance through the current node
            new_distance = current_distance + weight

            # Step 4: Update if we found a shorter route
            if new_distance < distances[neighbor]:

                distances[neighbor] = new_distance

                # Remember how we reached this neighbour
                previous[neighbor] = current_node

                # Add the neighbour to the priority queue
                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    # Step 5: Reconstruct the shortest path
    path = []

    if distances[destination] != float("inf"):

        current = destination

        while current != start:
            path.append(current)
            current = previous[current]

        path.append(start)
        path.reverse()

    # Return the results
    return {
        "path": path,
        "cost": distances[destination],
        "explored_nodes": explored_nodes
    }
