
from dijkstra import graph, dijkstra


def nearest_neighbor(graph, start):

    unvisited = set(graph.keys())
    unvisited.remove(start)

    route = [start]
    current = start
    total_distance = 0

    while unvisited:

        distances, previous = dijkstra(graph, current)

        next_location = min(
            unvisited,
            key=lambda node: distances[node]
        )

        total_distance += distances[next_location]

        route.append(next_location)

        current = next_location
        unvisited.remove(next_location)

    # Return to starting location
    distances, previous = dijkstra(graph, current)

    total_distance += distances[start]
    route.append(start)

    return route, total_distance


if __name__ == "__main__":

    start_location = "A"

    route, distance = nearest_neighbor(
        graph, start_location
    )

    print("\n========== TSP RESULTS ==========")

    print("Delivery Route:", " -> ".join(route))

    print("Total Distance:", distance, "km")
