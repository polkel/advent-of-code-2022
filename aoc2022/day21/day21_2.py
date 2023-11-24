from ..helpers import read_problem, print_to_display, exception_handler
from .day21_1 import MonkeyBusiness, input_file, test_file
import re


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        assert find_humn(test_file) == 301
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # Find the two strings that root has from parsing through the file
    # Set humn to 1 and check the absolute difference between the two string of root
    # Add 1 to humn
    # if absolute distance decreases, multiply humn to 10
    # check again and continue
    # once it increases, we know that we are a factor of 10 too far,
    # record which factor of 10 we are at, and subtract the next factor of 10 down
    # Check abs difference again
    # add 1 to humn
    # if the abs difference increased, it means the number is lower, we have to subtract again
    # once the absolute difference decreases with adding 1,
    # we know we have that correct factor of 10
    # move to the next factor of 10 and repeat the process, until we are at the ones digit where
    # we can just iterate to find the value
    humn = find_humn(input_file)
    print_to_display(f"The number that I have to shout is {str(int(humn))}", bold=True)


def find_humn(file_path):
    monkey_business = MonkeyBusiness(file_path)
    monkey_business.parse_file()
    str1, str2 = find_root_strings(file_path)
    last_diff = -2
    curr_humn = 1
    while last_diff < 0:
        monkey_business.monkey_dict["humn"] = curr_humn
        init_dist = abs(monkey_business.unpack(str1) - monkey_business.unpack(str2))
        monkey_business.monkey_dict["humn"] += 1
        next_dist = abs(monkey_business.unpack(str1) - monkey_business.unpack(str2))
        last_diff = next_dist - init_dist
        curr_humn *= 10
    monkey_business.monkey_dict["humn"] -= 1
    curr_factor = monkey_business.monkey_dict["humn"] / 10
    next_dist = 10
    while last_diff != 0:
        while last_diff > 0:
            monkey_business.monkey_dict["humn"] -= curr_factor
            init_dist = abs(monkey_business.unpack(str1) - monkey_business.unpack(str2))
            monkey_business.monkey_dict["humn"] += 1
            next_dist = abs(monkey_business.unpack(str1) - monkey_business.unpack(str2))
            if next_dist == 0:
                break
            last_diff = next_dist - init_dist
            monkey_business.monkey_dict["humn"] -= 1
        if next_dist == 0:
            break
        monkey_business.monkey_dict["humn"] += curr_factor
        curr_factor = curr_factor / 10
        last_diff = 1
    return monkey_business.monkey_dict["humn"]


def find_root_strings(file_path):
    root_re = re.compile(r"(?<=root: ).+(?=\n)")
    with open(file_path, "r") as file:
        x = file.read()
    str1, operation, str2 = root_re.search(x).group().split()
    return str1, str2
