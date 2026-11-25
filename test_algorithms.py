
import unittest

from sorting import merge_sort
from knapsack import knapsack
from dijkstra import graph, dijkstra, get_path
from tsp import nearest_neighbor


class TestCourierPlanner(unittest.TestCase):

    def test_merge_sort(self):
        parcels = [
            {"parcel_id": 1, "priority": 2, "deadline": 1},
            {"parcel_id": 2, "priority": 1, "deadline": 3},
            {"parcel_id": 3, "priority": 1, "deadline": 1}
        ]
        result = merge_sort(parcels)
        self.assertEqual(
            [p["parcel_id"] for p in result],
            [3, 2, 1]
        )

    def test_knapsack(self):
        with open("data/parcels.json", "r") as file:
            import json
            parcels = json.load(file)

        selected, total_value = knapsack(parcels, 15)
        self.assertEqual(total_value, 240)

    def test_dijkstra(self):
        distances, previous = dijkstra(graph, "A")
        self.assertEqual(distances["E"], 10)
        self.assertEqual(
            get_path(previous, "E"),
            ["A", "C", "B", "D", "E"]
        )

    def test_tsp(self):
        route, distance = nearest_neighbor(graph, "A")
        self.assertEqual(route[0], "A")
        self.assertEqual(route[-1], "A")
        self.assertEqual(distance, 20)


if __name__ == "__main__":
    unittest.main(verbosity=2)