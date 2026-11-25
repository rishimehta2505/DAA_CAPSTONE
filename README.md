# Mini-Courier Planner

## 1. Project overview

Mini-Courier Planner is a Python prototype that combines sorting, dynamic
programming, shortest-path graph algorithms, and an approximation technique
to support a small courier-planning workflow.

The program:
1. Prioritizes parcels by priority and then by delivery deadline.
2. Selects a high-value set of parcels that fits a vehicle weight capacity.
3. Calculates shortest paths from a starting delivery location using Dijkstra's algorithm.
4. Produces a delivery tour using the nearest-neighbor TSP approximation.
5. Measures algorithm runtimes on increasing parcel and graph input sizes.

## 2. Project structure

```text
Mini-Courier-Planner/
├── data/
│   └── parcels.json
├── outputs/
│   ├── performance_results.json
│   ├── parcel_algorithm_performance.png
│   └── graph_algorithm_performance.png
├── screenshots/
├── main.py
├── sorting.py
├── knapsack.py
├── dijkstra.py
├── tsp.py
├── performance.py
└── README.md
```

## 3. Requirements

- Python 3.10 or later
- Matplotlib

Install Matplotlib:

```bash
python -m pip install matplotlib
```

On Windows, if `python` is not recognized, use:

```powershell
py -m pip install matplotlib
```

## 4. How to run

Open a terminal in the project root directory.

Run the integrated planner:

```powershell
py main.py
```

Run individual algorithm modules:

```powershell
py sorting.py
py knapsack.py
py dijkstra.py
py tsp.py
```

Run performance testing and generate charts:

```powershell
py performance.py
```

The performance script writes JSON results and two PNG charts into `outputs/`.

## 5. Input dataset

The sample dataset is stored in `data/parcels.json`. Each parcel contains:

| Field | Meaning |
|---|---|
| `parcel_id` | Unique parcel identifier |
| `destination` | Delivery location |
| `weight` | Parcel weight in kilograms |
| `value` | Value used by the knapsack objective |
| `deadline` | Delivery deadline value used for sorting |
| `priority` | Lower number represents higher priority |

The vehicle capacity in `main.py` is currently set to 15 kg. The road network
is represented in `dijkstra.py` as an adjacency dictionary. Each edge weight
represents distance in kilometres.

## 6. Algorithms and complexity

| Component | Technique | Time complexity | Space complexity |
|---|---|---|---|
| Parcel prioritization | Merge Sort | O(n log n) | O(n) auxiliary space, plus recursive stack |
| Packing | 0/1 Knapsack DP | O(nW) | O(nW) |
| Shortest paths | Dijkstra with a binary heap | O((V + E) log V) | O(V + E) |
| Delivery tour | Nearest-neighbor with repeated Dijkstra calls | O(V(V + E) log V) for this implementation | O(V + E) working space, excluding returned route |

Here, `n` is the number of parcels, `W` is the integer vehicle capacity,
`V` is the number of graph vertices, and `E` is the number of graph edges.
The TSP method is an approximation; it does not guarantee an optimal tour.

## 7. Performance methodology

The performance script:
- Tests parcel counts of 10, 50, 100, 200, 500, and 1000.
- Measures Merge Sort and Knapsack separately.
- Increases Knapsack capacity using `max(50, parcel_count * 5)` so both the
  number of items and DP capacity are represented in the experiment.
- Tests graph sizes of 5, 10, 15, 20, 30, 40, and 50 locations.
- Generates connected, undirected, weighted graphs for graph algorithm tests.
- Repeats each measurement five times and reports the arithmetic mean.
- Uses `time.perf_counter()` for elapsed-time measurement.
- Uses a fixed random seed so generated test data can be reproduced.

Sorting/Knapsack and Dijkstra/TSP are plotted separately because their input
size measures differ. Runtime results are machine-dependent and should be
interpreted as experimental observations, not exact theoretical values.

## 8. Limitations and possible future improvements

- The nearest-neighbor TSP algorithm is approximate and may produce a tour
  longer than the optimal tour.
- The sample road network and parcel dataset are small demonstrations, not
  live map or traffic data.
- The current packing objective maximizes parcel value under a weight limit;
  it does not yet enforce deadlines or destination grouping during packing.
- Future work could add a larger real-world road dataset, route visualization,
  deadline-aware scheduling, and comparison with other optimization methods.

## 9. Evidence to capture for submission

Capture your own screenshots after running:
1. `py main.py` showing the integrated output.
2. `py performance.py` showing successful completion.
3. `outputs/parcel_algorithm_performance.png`.
4. `outputs/graph_algorithm_performance.png`.
5. The project files open in your editor.

Place the screenshots in the `screenshots/` folder. Do not use sample or
fabricated screenshots as evidence of execution.
