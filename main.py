
import json

from sorting import merge_sort, display_parcels
from knapsack import knapsack, display_result
from dijkstra import graph, dijkstra, get_path
from tsp import nearest_neighbor


def main():

    # Load parcel data
    with open("data/parcels.json", "r") as file:
        parcels = json.load(file)

    print("\n====================================")
    print("       MINI-COURIER PLANNER")
    print("====================================")

    # 1. Merge Sort
    print("\n1. PARCEL PRIORITIZATION")

    sorted_parcels = merge_sort(parcels)
    display_parcels(sorted_parcels)

    # 2. Knapsack
    print("\n2. OPTIMAL PARCEL SELECTION")

    capacity = 15

    selected, total_value = knapsack(
        parcels, capacity
    )

    display_result(selected, total_value)

    # 3. Dijkstra
    print("\n3. SHORTEST PATH CALCULATION")

    distances, previous = dijkstra(graph, "A")

    for destination in graph:

        path = get_path(previous, destination)

        print(
            f"A to {destination}: "
            f"{distances[destination]} km | "
            f"{' -> '.join(path)}"
        )

    # 4. TSP
    print("\n4. DELIVERY ROUTE OPTIMIZATION")

    route, distance = nearest_neighbor(graph, "A")

    print("Delivery Route:", " -> ".join(route))
    print("Total Distance:", distance, "km")

    print("\n====================================")
    print("       PLANNING COMPLETED")
    print("====================================")


if __name__ == "__main__":
    main()
