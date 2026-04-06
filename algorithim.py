from enum import Enum


class setList(Enum):
    wtr = 1
    arc = 2
    cru = 3
    mon = 4
    ele = 5
    evr = 6
    upr = 7
    hp1 = 8
    dyn = 9
    out = 10
    dtd = 11
    evo = 12
    hvy = 13
    mst = 14
    ros = 15
    hnt = 16
    sea = 17
    sup = 18
    pen = 19




def quick_sort_in_set(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2][1]
    left = [x for x in arr if x[1] < pivot]
    middle = [x for x in arr if x[1] == pivot]
    right = [x for x in arr if x[1] > pivot]

    return quick_sort_in_set(left) + middle + quick_sort_in_set(right)


def quick_sort_sets(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[(len(arr) // 2)].value  # pick middle element as pivot
    left = [x for x in arr if x.value < pivot]  # smaller than pivot
    middle = [x for x in arr if x.value == pivot]  # equal to pivot
    right = [x for x in arr if x.value > pivot]  # larger than pivot

    return quick_sort_sets(left) + middle + quick_sort_sets(right)