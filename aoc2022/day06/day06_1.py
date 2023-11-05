from ..helpers import read_problem, print_to_display, exception_handler
import os


input_name = "signal_chars.txt"
input_path = os.path.dirname(__file__) + "\\" + input_name


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_1 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"  # 7
        test_2 = "bvwbjplbgvbhsrlpgdmjqwftvncz"  # 5
        test_3 = "nppdvjthqldpwncqszvftbrmjlhg"  # 6
        test_4 = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"  # 10
        test_5 = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"  # 11
        assert find_unique_substr(test_1, 4) == 7
        assert find_unique_substr(test_2, 4) == 5
        assert find_unique_substr(test_3, 4) == 6
        assert find_unique_substr(test_4, 4) == 10
        assert find_unique_substr(test_5, 4) == 11
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # We just need to find the index of the first character after 4 unique characters
    # It's going to be at least 4
    # Let's not make this too complicated and just do a linear scan
    with open(input_path, "r") as file:
        char_marker = 0
        for line in file:
            char_marker = find_unique_substr(line, 4)
    print_to_display(f"{str(char_marker)} characters need to be processed before the start-of-packet marker", bold=True)
    print("\n\n")


def unique_chars(chars: str):
    char_len = len(chars)
    char_set = set(chars)
    if char_len == len(char_set):
        return True
    else:
        return False


def find_unique_substr(line: str, num_char: int):
    """
    Returns the first index after num_char unique characters in a row.
    e.g. "bvwbjplbgvbhs" and num_char = 4 would return 5 because "p" is the first char after 4 unique characters
    :param line: string to scan for unique characters in a row
    :param num_char: int of necessary unique characters before returning
    :return: int of index or -1 if there are no unique characters
    """
    for i in range(num_char, len(line)):
        start_ind = i - num_char
        substr = line[start_ind: i]
        if unique_chars(substr):
            return i
    return -1
