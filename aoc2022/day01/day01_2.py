import os
from ..helpers import read_problem, print_to_display


elf_list_file = "elf_snacks.txt"
elf_list_path = os.path.dirname(__file__) + "\\" + elf_list_file


def display_problem():
    read_problem(__file__)


def solve_problem():
    first_max = 0
    second_max = 0
    third_max = 0
    curr_max = 0
    with open(elf_list_path, "r") as file:
        for line in file:
            if line == "\n":
                if curr_max > third_max:
                    third_max = curr_max
                if curr_max > second_max:
                    third_max = second_max
                    second_max = curr_max
                if curr_max > first_max:
                    second_max = first_max
                    first_max = curr_max
                curr_max = 0
            else:
                curr_max += int(line.strip())

    total_calories = first_max + second_max + third_max
    print_to_display(f"The top three elves are carrying {str(total_calories)} calories together", bold=True)
    print()
