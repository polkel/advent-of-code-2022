import textwrap


def print_to_display(text, bold=False):
    to_print = textwrap.fill(text, 80)
    if bold:
        to_print = "\033[1m" + to_print + "\033[0m"
    print(to_print)


def read_problem(module_file_path):
    problem_file = module_file_path[:-2] + "txt"
    with open(problem_file, "r") as file:
        for line in file:
            print_to_display(line)
    print("\n")
