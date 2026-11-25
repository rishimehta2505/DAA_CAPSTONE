"""Benchmark the Mini-Courier Planner algorithms on scalable inputs.

Parcel algorithms are measured against parcel count. Graph algorithms are
measured against the number of delivery locations (vertices), rather than
repeatedly timing the same five-node graph.
"""

import json
import os
import random
import statistics
import time

import matplotlib.pyplot as plt

from sorting import merge_sort
from knapsack import knapsack
from dijkstra import dijkstra
from tsp import nearest_neighbor


OUTPUT_DIR = "outputs"
PARCEL_SIZES = [10, 50, 100, 200, 500, 1000]
GRAPH_SIZES = [5, 10, 15, 20, 30, 40, 50]
REPEATS = 5
RANDOM_SEED = 42


def measure_average_time(function, *args, repeats=REPEATS):
    """Return average wall-clock runtime over repeated executions."""
    timings = []
    for _ in range(repeats):
        start = time.perf_counter()
        function(*args)
        timings.append(time.perf_counter() - start)
    return statistics.mean(timings)


def generate_parcels(size, rng):
    """Create reproducible parcel data for a requested input size."""
    destinations = ["A", "B", "C", "D", "E"]
    return [
        {
            "parcel_id": i + 1,
            "destination": rng.choice(destinations),
            "weight": rng.randint(1, 10),
            "value": rng.randint(10, 100),
            "deadline": rng.randint(1, 10),
            "priority": rng.randint(1, 5),
        }
        for i in range(size)
    ]


def generate_graph(size, rng):
    """Create a connected, undirected weighted graph of `size` locations."""
    if size < 2:
        raise ValueError("Graph size must be at least 2.")

    nodes = [f"Location_{i + 1}" for i in range(size)]
    generated_graph = {node: {} for node in nodes}

    # A cycle guarantees that every location is reachable.
    for i in range(size):
        first = nodes[i]
        second = nodes[(i + 1) % size]
        weight = rng.randint(1, 20)
        generated_graph[first][second] = weight
        generated_graph[second][first] = weight

    # Add extra roads to create more realistic route choices.
    extra_edges = max(size // 2, 1)
    for _ in range(extra_edges):
        first, second = rng.sample(nodes, 2)
        weight = rng.randint(1, 20)
        old_weight = generated_graph[first].get(second)
        if old_weight is None or weight < old_weight:
            generated_graph[first][second] = weight
            generated_graph[second][first] = weight

    return generated_graph


def save_plot(x_values, series, title, x_label, filename):
    """Save a separate chart so algorithms with different scales remain readable."""
    plt.figure(figsize=(9, 5))
    for label, values in series.items():
        plt.plot(x_values, values, marker="o", label=label)

    plt.xlabel(x_label)
    plt.ylabel("Average execution time (seconds)")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=150)
    plt.close()


def performance_analysis():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    rng = random.Random(RANDOM_SEED)

    parcel_results = {
        "input_sizes": PARCEL_SIZES,
        "repeats_per_size": REPEATS,
        "knapsack_capacity_rule": "max(50, parcel_count * 5)",
        "sorting_times": [],
        "knapsack_times": [],
    }

    for size in PARCEL_SIZES:
        print(f"Testing parcel input size: {size}")
        parcels = generate_parcels(size, rng)
        capacity = max(50, size * 5)

        parcel_results["sorting_times"].append(
            measure_average_time(merge_sort, parcels)
        )
        parcel_results["knapsack_times"].append(
            measure_average_time(knapsack, parcels, capacity)
        )

    graph_results = {
        "vertex_counts": GRAPH_SIZES,
        "repeats_per_size": REPEATS,
        "dijkstra_times": [],
        "tsp_times": [],
    }

    for size in GRAPH_SIZES:
        print(f"Testing graph size: {size} locations")
        test_graph = generate_graph(size, rng)
        start_node = next(iter(test_graph))

        graph_results["dijkstra_times"].append(
            measure_average_time(dijkstra, test_graph, start_node)
        )
        graph_results["tsp_times"].append(
            measure_average_time(nearest_neighbor, test_graph, start_node)
        )

    all_results = {
        "methodology": {
            "repeats": REPEATS,
            "measurement": "Arithmetic mean measured with time.perf_counter",
            "random_seed": RANDOM_SEED,
            "note": (
                "Sorting and Knapsack are measured against parcel count. "
                "Dijkstra and TSP are measured against graph vertex count. "
                "Graph tests use connected, undirected, weighted graphs."
            ),
        },
        "parcel_algorithms": parcel_results,
        "graph_algorithms": graph_results,
    }

    with open(os.path.join(OUTPUT_DIR, "performance_results.json"), "w") as file:
        json.dump(all_results, file, indent=4)

    save_plot(
        PARCEL_SIZES,
        {
            "Merge Sort": parcel_results["sorting_times"],
            "0/1 Knapsack": parcel_results["knapsack_times"],
        },
        "Parcel Algorithms: Runtime vs Parcel Count",
        "Number of parcels",
        "parcel_algorithm_performance.png",
    )

    save_plot(
        GRAPH_SIZES,
        {
            "Dijkstra": graph_results["dijkstra_times"],
            "Nearest-Neighbor TSP": graph_results["tsp_times"],
        },
        "Graph Algorithms: Runtime vs Number of Locations",
        "Number of delivery locations (vertices)",
        "graph_algorithm_performance.png",
    )

    print("\nPerformance analysis completed.")
    print("Results and charts saved in the outputs folder.")


if __name__ == "__main__":
    performance_analysis()
