from ..helpers import read_problem, print_to_display, exception_handler
from .day04_1 import input_path


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_1 = "5-7,7-9"  # True
        test_2 = "2-8,3-7"  # True
        test_3 = "2-4,6-8"  # False
        test_4 = "2-3,4-5"  # False
        split_1 = test_1.split(",")
        split_2 = test_2.split(",")
        split_3 = test_3.split(",")
        split_4 = test_4.split(",")
        assert range_overlap(*split_1)
        assert range_overlap(*split_2)
        assert not range_overlap(*split_3)
        assert not range_overlap(*split_4)
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # Can still do this with comparisons, just 2 more though
    # id1_min <= id2_min and id2_min <= id1_max
    # id1_min <= id2_max and id2_max <= id1_max
    # and then do the same for id2 to id1
    pair_overlap = 0
    with open(input_path, "r") as file:
        for pair in file:
            range1, range2 = pair.strip().split(",")
            if range_overlap(range1, range2):
                pair_overlap += 1
    print_to_display(f"The assignment pairs overlap in {str(pair_overlap)} pairs", bold=True)
    print("\n\n")


def range_overlap_set(range1, range2):
    # let's solve this with sets
    id1_min, id1_max = range1.split("-")
    id2_min, id2_max = range2.split("-")
    id1_min = int(id1_min)
    id1_max = int(id1_max)
    id2_min = int(id2_min)
    id2_max = int(id2_max)
    set_1 = set(range(id1_min, id1_max + 1))
    set_2 = set(range(id2_min, id2_max + 1))
    common_set = set_1.intersection(set_2)
    if len(common_set) > 0:
        return True
    return False


def range_overlap(range1, range2):
    # This didn't work because I didn't convert to int!
    id1_min, id1_max = range1.split("-")
    id2_min, id2_max = range2.split("-")
    id1_min = int(id1_min)
    id1_max = int(id1_max)
    id2_min = int(id2_min)
    id2_max = int(id2_max)
    result = False
    olap_1 = id1_min <= id2_min <= id1_max
    olap_2 = id1_min <= id2_max <= id1_max
    olap_3 = id2_min <= id1_min <= id2_max
    olap_4 = id2_min <= id1_max <= id2_max
    if olap_1 or olap_2 or olap_3 or olap_4:
        result = True
    return result
