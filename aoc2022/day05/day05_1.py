from ..helpers import read_problem, print_to_display, exception_handler
import os


input_file = "stacks_and_commands.txt"
input_path = os.path.dirname(__file__) + "\\" + input_file
test_file = "test_input.txt"
test_path = os.path.dirname(__file__) + "\\" + test_file


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_stack = dict()
        test_stack[1] = ["Z", "N"]
        test_stack[2] = ["M", "C", "D"]
        test_stack[3] = ["P"]
        assert extract_stack(test_path) == test_stack
        result_stack = dict()
        result_stack[1] = ["C"]
        result_stack[2] = ["M"]
        result_stack[3] = ["P", "D", "N", "Z"]
        move_stacks(test_stack, test_path)
        assert test_stack == result_stack
        assert stack_message(test_stack) == "CMZ"

    except Exception as e:
        exception_handler(e)


def solve_problem():
    # Pretty blatantly, this problem asks us to use stacks
    # I could import deque, but we don't really ever have to insert in the bottom of the stack
    # I will just use a regular list and insert in position 0 to initialize all the stacks
    # We need a few helper functions
    # One function to read the initial stacks
    # One function to process the moves for the stacks
    # I want to store the stacks in a dictionary where the keys are the stack numbers
    stacks = extract_stack(input_path)
    move_stacks(stacks, input_path)
    result = stack_message(stacks)
    print_to_display(f"The crates that end up on the tap of each stack is {result}", bold=True)
    print("\n\n")


def extract_stack(stack_file_path: str):
    # Assume stack items are always spaced out by 4
    # e.g. stack 1 item is in index 1, stack 2 item at 5, 3 at 9, etc.
    # Assume all stack items are always capital letters
    low_ord = ord("A")
    high_ord = ord("Z")
    char_separation = 4
    stacks = dict()
    keys = set()
    with open(stack_file_path, "r") as file:
        for stack_line in file:
            no_stack_items = True
            for i in range(1, len(stack_line), char_separation):
                curr_char = stack_line[i]
                key_val = (i // char_separation) + 1  # stack keys will mirror input label
                if key_val not in keys:
                    keys.add(key_val)
                    stacks[key_val] = []  # initialize stack first
                if low_ord <= ord(curr_char) <= high_ord:
                    stacks[key_val].insert(0, curr_char)
                    no_stack_items = False
            if no_stack_items:
                break
    return stacks


def move_stacks(stack_dict: dict, stack_file_path: str):
    # will modify the input stack vs duplicating and returning
    # This assumes that the instructions are reliable as well
    # That there are no empty moves
    with open(stack_file_path, "r") as file:
        for instruction in file:
            if instruction[: 4] != "move":
                continue
            instruction_split = instruction.split(" ")
            num_items = int(instruction_split[1])
            from_stack = int(instruction_split[3])
            to_stack = int(instruction_split[5])
            for _ in range(num_items):
                stack_dict[to_stack].append(stack_dict[from_stack].pop())


def stack_message(stack_dict: dict):
    # This assumes that every stack has a resulting item
    # No instructions have been provided for empty stacks
    stack_keys = list(stack_dict.keys())
    stack_keys.sort()
    result_str = ""
    for key in stack_keys:
        result_str += stack_dict[key].pop()
    return result_str
