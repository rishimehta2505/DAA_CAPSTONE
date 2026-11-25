
import heapq


# Road network represented as an adjacency list
graph = {
    "A": {"B": 4, "C": 2},
    "B": {"A": 4, "C": 1, "D": 5},
    "C": {"A": 2, "B": 1, "D": 8, "E": 10},
    "D": {"B": 5, "C": 8, "E": 2},
    "E": {"C": 10, "D": 2}
}


def dijkstra(graph, start):

    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}

    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:

        current_distance, current_node = heapq.heappop(
            priority_queue
        )

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():

            distance = current_distance + weight

            if distance < distances[neighbor]:

                distances[neighbor] = distance
                previous[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (distance, neighbor)
                )

    return distances, previous


def get_path(previous, destination):

    path = []

    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    return path[::-1]


if __name__ == "__main__":

    start_location = "A"

    distances, previous = dijkstra(
        graph, start_location
    )

    print("\n========== DIJKSTRA RESULTS ==========")

    for destination in graph:

        path = get_path(previous, destination)

        print(
            f"From {start_location} to {destination}: "
            f"Distance = {distances[destination]} km | "
            f"Path = {' -> '.join(path)}"
        )
