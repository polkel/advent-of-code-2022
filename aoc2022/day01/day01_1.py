import os

from ..helpers import read_problem, print_to_display


elf_list_file = "elf_snacks.txt"
elf_list_path = os.path.dirname(__file__) + "\\" + elf_list_file


def display_problem():
    read_problem(__file__)


def solve_problem():
    max_snack = 0
    curr_max = 0

    with open(elf_list_path, "r") as file:
        for line in file:
            if line == "\n":
                if curr_max > max_snack:
                    max_snack = curr_max
                curr_max = 0
            else:
                curr_max += int(line.strip())

    print_to_display(f"The elf carrying the most calories is carrying {str(max_snack)} calories", bold=True)
    print()
