from ..helpers import read_problem, print_to_display, exception_handler
import os


rucksack_file = "rucksacks.txt"
rucksack_file_path = os.path.dirname(__file__) + "\\" + rucksack_file


def display_problem():
    read_problem(__file__)


def solve_problem():
    # Scan through each rucksack
    # Find the common letter in both sides
    # split in half and use set intersection
    # use ord to find the corresponding letter value
    curr_sum = 0
    with open(rucksack_file_path, "r") as file:
        for line in file:
            common_letter = find_common_letter(line.strip())
            letter_val = find_letter_value(common_letter)
            curr_sum += letter_val
    print_to_display(f"The sum of priorities of item types incorrectly sorted is {str(curr_sum)}", bold=True)
    print("\n\n")


def test_problem():
    try:
        light_tests()
    except Exception as e:
        exception_handler(e)


def light_tests():
    test_sack_1 = "vJrwpWtwJgWrhcsFMMfFFhFp"  # p is common
    test_sack_2 = "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL"  # L is common
    test_sack_3 = "PmmdzqPrVvPwwTWBwg"  # P is common
    test_letter_1 = "a"  # should be 1
    test_letter_2 = "e"  # should be 5
    test_letter_3 = "G"  # should be 33
    assert find_common_letter(test_sack_1) == "p"
    assert find_common_letter(test_sack_2) == "L"
    assert find_common_letter(test_sack_3) == "P"
    assert find_letter_value(test_letter_1) == 1
    assert find_letter_value(test_letter_2) == 5
    assert find_letter_value(test_letter_3) == 33


def find_letter_value(letter: str):
    # a is 1, z is 26, A is 27, Z is 52
    cap_a_num = ord("A")
    a_num = ord("a")
    cap_sub = cap_a_num - 27
    low_sub = a_num - 1
    if letter.isupper():
        return ord(letter) - cap_sub
    else:
        return ord(letter) - low_sub


def find_common_letter(line: str):
    total_char = len(line)
    line_1 = line[: total_char // 2]
    line_2 = line[total_char // 2:]
    set_1 = set(line_1)
    set_2 = set(line_2)
    common_set = set_1.intersection(set_2)
    return common_set.pop()
