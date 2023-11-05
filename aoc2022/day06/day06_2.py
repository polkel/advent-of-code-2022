from ..helpers import read_problem, print_to_display, exception_handler
from .day06_1 import find_unique_substr, input_path


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_1 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"  # 19
        test_2 = "bvwbjplbgvbhsrlpgdmjqwftvncz"  # 23
        test_3 = "nppdvjthqldpwncqszvftbrmjlhg"  # 23
        test_4 = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"  # 29
        test_5 = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"  # 26
        assert find_unique_substr(test_1, 14) == 19
        assert find_unique_substr(test_2, 14) == 23
        assert find_unique_substr(test_3, 14) == 23
        assert find_unique_substr(test_4, 14) == 29
        assert find_unique_substr(test_5, 14) == 26
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # My last functions handle this problem already, I just have to change 4 to 14
    with open(input_path, "r") as file:
        char_marker = 0
        for line in file:
            char_marker = find_unique_substr(line, 14)
    print_to_display(f"{str(char_marker)} characters are processed before the start-of-message marker", bold=True)
    print("\n\n")
