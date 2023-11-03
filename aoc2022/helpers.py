import textwrap
import os


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


def create_new_day(day_num: int):
    curr_dir = os.path.dirname(__file__)
    if day_num < 10:
        dir_name = f"day0{str(day_num)}"
    else:
        dir_name = f"day{str(day_num)}"
    dir_items = os.listdir(curr_dir)
    if dir_name in dir_items:
        print("That day already exists!\n\n")
    else:
        os.chdir(curr_dir)
        os.mkdir(dir_name)
        os.chdir(dir_name)
        with open("__init__.py", "w") as file:
            file.write("def main():\n")
            file.write("    pass\n")
        print("New directory created successfully!\n\n")


def exception_handler(exception_item):
    print("Error in tests\n\n")
    tb = exception_item.__traceback__
    file_name = ""
    line_num = ""
    func_name = ""
    while tb is not None:
        file_name = tb.tb_frame.f_code.co_filename
        func_name = tb.tb_frame.f_code.co_name
        line_num = tb.tb_lineno
        tb = tb.tb_next
    print(type(exception_item).__name__, exception_item)
    print(file_name, func_name, f"line {line_num}\n\n")
