from ..helpers import read_problem, print_to_display, exception_handler
from . import day07_1


total_disk_space = 70000000
required_disk_space = 30000000


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_terminal = day07_1.Terminal()
        with open(day07_1.test_path, "r") as file:
            for line in file:
                test_terminal.process_command(line.rstrip())
        space_needed = find_space_needed(test_terminal)
        smallest_dir = find_smallest_directory(space_needed, test_terminal)
        assert smallest_dir.size == 24933642
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # First we need to find how much space we need to free to get the required amount of space
    # Then we need to scan all the directories to find the smallest directory we can delete
    # To fulfill the space requirement
    terminal = day07_1.Terminal()
    with open(day07_1.input_path, "r") as file:
        for line in file:
            terminal.process_command(line.rstrip())
    space_needed = find_space_needed(terminal)
    smallest_dir = find_smallest_directory(space_needed, terminal)
    print_to_display(f"The smallest directory to fulfill the size requirement is {smallest_dir}", bold=True)
    print_to_display(f"The parent directory is {terminal.parent_dir}", bold=True)
    print("\n\n")


def find_space_needed(terminal: day07_1.Terminal):
    curr_free_space = total_disk_space - terminal.parent_dir.size
    space_needed = required_disk_space - curr_free_space
    if space_needed < 0:
        return 0
    else:
        return space_needed


def find_smallest_directory(space_requirement: int, terminal: day07_1.Terminal):
    curr_smallest = None
    for directory in terminal.all_dirs:
        if directory.size >= space_requirement:
            if curr_smallest is None:
                curr_smallest = directory
            elif curr_smallest.size > directory.size:
                curr_smallest = directory
    return curr_smallest
