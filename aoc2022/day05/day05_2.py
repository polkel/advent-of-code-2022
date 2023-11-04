from ..helpers import read_problem, print_to_display, exception_handler
from . import day05_1


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_stack = day05_1.extract_stack(day05_1.test_path)
        move_stacks_9001(test_stack, day05_1.test_path)
        result_stack = dict()
        result_stack[1] = ["M"]
        result_stack[2] = ["C"]
        result_stack[3] = ["P", "Z", "N", "D"]
        assert test_stack == result_stack
    except Exception as e:
        exception_handler(e)


def solve_problem():
    stacks = day05_1.extract_stack(day05_1.input_path)
    move_stacks_9001(stacks, day05_1.input_path)
    result_str = day05_1.stack_message(stacks)
    print_to_display(f"The crates that end up on top of each stack from the 9001 are {result_str}", bold=True)
    print("\n\n")


def move_stacks_9001(stack_dict: dict, stack_file_path: str):
    with open(stack_file_path, "r") as file:
        for instruction in file:
            if instruction[: 4] != "move":
                continue
            instruction_split = instruction.split(" ")
            num_items = int(instruction_split[1])
            from_stack = int(instruction_split[3])
            to_stack = int(instruction_split[5])
            mid_stack = []  # This could be more efficient with slices, but this is more straight forward
            for _ in range(num_items):
                mid_stack.append(stack_dict[from_stack].pop())
            for _ in range(num_items):
                stack_dict[to_stack].append(mid_stack.pop())
