
import json


def merge_sort(parcels):
    """
    Sort parcels using Merge Sort.
    Priority: Lowest number first.
    Deadline: Earliest first.
    """

    if len(parcels) <= 1:
        return parcels

    mid = len(parcels) // 2

    left = merge_sort(parcels[:mid])
    right = merge_sort(parcels[mid:])

    return merge(left, right)


def merge(left, right):
    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        key_left = (left[i]["priority"], left[i]["deadline"])
        key_right = (right[j]["priority"], right[j]["deadline"])

        if key_left <= key_right:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def display_parcels(parcels):

    print("\n========== SORTED PARCELS ==========")

    for parcel in parcels:
        print(
            f"Parcel ID: {parcel['parcel_id']} | "
            f"Destination: {parcel['destination']} | "
            f"Priority: {parcel['priority']} | "
            f"Deadline: {parcel['deadline']}"
        )


if __name__ == "__main__":

    with open("data/parcels.json", "r") as file:
        parcels = json.load(file)

    sorted_parcels = merge_sort(parcels)

    display_parcels(sorted_parcels)
