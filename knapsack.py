
import json


def knapsack(parcels, capacity):
    """
    0/1 Knapsack using Dynamic Programming.
    Supports decimal parcel weights by converting kg into grams.
    """

    n = len(parcels)

    # Convert capacity from kg to grams
    capacity_grams = round(capacity * 1000)

    # Convert all parcel weights into grams
    weights = [
        round(parcel["weight"] * 1000)
        for parcel in parcels
    ]

    # Create DP table
    dp = [[0 for _ in range(capacity_grams + 1)]
          for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):

        weight = weights[i - 1]
        value = parcels[i - 1]["value"]

        for w in range(capacity_grams + 1):

            if weight <= w:
                dp[i][w] = max(
                    value + dp[i - 1][w - weight],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    # Find selected parcels
    selected = []
    w = capacity_grams

    for i in range(n, 0, -1):

        if dp[i][w] != dp[i - 1][w]:

            selected.append(parcels[i - 1])
            w -= weights[i - 1]

    selected.reverse()

    return selected, dp[n][capacity_grams]


def display_result(selected, total_value):

    total_weight = sum(p["weight"] for p in selected)

    print("\n========== KNAPSACK RESULTS ==========")

    for parcel in selected:
        print(
            f"Parcel ID: {parcel['parcel_id']} | "
            f"Weight: {parcel['weight']} kg | "
            f"Value: {parcel['value']}"
        )

    print("-------------------------------------")
    print(f"Total Weight: {total_weight:.2f} kg")
    print("Total Value:", total_value)


if __name__ == "__main__":

    with open("data/parcels.json", "r") as file:
        parcels = json.load(file)

    vehicle_capacity = 15

    selected, total_value = knapsack(
        parcels, vehicle_capacity
    )

    display_result(selected, total_value)
