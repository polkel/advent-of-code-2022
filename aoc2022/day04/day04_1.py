from ..helpers import read_problem, print_to_display, exception_handler
import os

input_name = "section_ids.txt"
input_path = os.path.dirname(__file__) + "\\" + input_name


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_1 = "2-4,6-8"
        test_2 = "2-3,4-5"
        test_3 = "5-7,7-9"
        test_4 = "2-8,3-7"
        split_1 = test_1.split(",")
        split_2 = test_2.split(",")
        split_3 = test_3.split(",")
        split_4 = test_4.split(",")
        assert not range_inclusive(*split_1)
        assert not range_inclusive(*split_2)
        assert not range_inclusive(*split_3)
        assert range_inclusive(*split_4)
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # for every pair (line of text), split the two ranges
    # I could use sets to figure this out, but I think two to four comparisons is enough
    # e.g. split the variables into id1_min id1_max id2_min id2_max
    # the pair is inclusive of the other if one of these two conditions are met:
    # id1_min <= id2_min and id1_max >= id2_max
    # OR
    # id2_min <= id1_min and id2_max >= id1_max
    inclusive_pairs = 0
    with open(input_path, "r") as file:
        for pair in file:
            range_pair = pair.strip().split(",")
            if range_inclusive(*range_pair):
                inclusive_pairs += 1
    print_to_display(f"One range fully contains the other in {str(inclusive_pairs)} assignment pairs", bold=True)
    print("\n\n")


def range_inclusive(range1, range2):
    result = False
    id1_min, id1_max = range1.split("-")
    id2_min, id2_max = range2.split("-")
    id1_min = int(id1_min)
    id1_max = int(id1_max)
    id2_min = int(id2_min)
    id2_max = int(id2_max)
    inclusive_1 = id1_min <= id2_min and id1_max >= id2_max
    inclusive_2 = id2_min <= id1_min and id2_max >= id1_max
    if inclusive_1 or inclusive_2:
        result = True
    return result
