from ..helpers import read_problem, print_to_display, exception_handler
from . import day03_1


def display_problem():
    read_problem(__file__)


def solve_problem():
    # Find the common character for every 3 lines
    # Sum up the value of those common characters
    # Again we can just use sets here, but extracting 3 lines at a time will be somewhat tricky
    # let's just do readlines and extract the lines into a list
    curr_sum = 0
    with open(day03_1.rucksack_file_path, "r") as file:
        all_sacks = file.readlines()
        for i in range(0, len(all_sacks), 3):
            line_1 = all_sacks[i].strip()
            line_2 = all_sacks[i + 1].strip()
            line_3 = all_sacks[i + 2].strip()
            common_letter = find_common_letter(line_1, line_2, line_3)
            curr_sum += day03_1.find_letter_value(common_letter)
    print_to_display(f"The sum of priorities of the elf badges is {str(curr_sum)}", bold=True)
    print("\n\n")


def test_problem():
    try:
        test_1_line_1 = "vJrwpWtwJgWrhcsFMMfFFhFp"
        test_1_line_2 = "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL"
        test_1_line_3 = "PmmdzqPrVvPwwTWBwg"  # should be r
        test_2_line_1 = "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn"
        test_2_line_2 = "ttgJtRGJQctTZtZT"
        test_2_line_3 = "CrZsJsPPZsGzwwsLwLmpwMDw"  # should be Z
        assert find_common_letter(test_1_line_1, test_1_line_2, test_1_line_3) == "r"
        assert find_common_letter(test_2_line_1, test_2_line_2, test_2_line_3) == "Z"
    except Exception as e:
        exception_handler(e)


def find_common_letter(line1, line2, line3):
    set_1 = set(line1)
    set_2 = set(line2)
    set_3 = set(line3)
    common_set = set_1.intersection(set_2)
    common_set = common_set.intersection(set_3)
    return common_set.pop()
