from ..helpers import read_problem, print_to_display, exception_handler
import os


path_to_dir = os.path.dirname(__file__)
input_file = path_to_dir + "\\monkeys.txt"
test_file = path_to_dir + "\\test_monkeys.txt"


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_business = MonkeyBusiness(test_file)
        test_business.parse_file()
        assert int(test_business.unpack("root")) == 152
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # This looks like a problem in recursion
    # I think I should scan all the monkeys first
    # and maybe store each monkey buy its key in a dict
    # then store the value by either a function or an int depending on what is in the text
    monkey_business = MonkeyBusiness(input_file)
    monkey_business.parse_file()
    root_num = int(monkey_business.unpack("root"))
    print_to_display(f"The monkey at root will yell the number {str(root_num)}", bold=True)
    print("\n\n")


class MonkeyBusiness:
    def __init__(self, file_path):
        self.file_path = file_path
        self.monkey_dict = dict()

    def unpack(self, var_str):
        if isinstance(self.monkey_dict[var_str], int):
            return self.monkey_dict[var_str]
        else:
            return self.monkey_dict[var_str][0](*self.monkey_dict[var_str][1])

    def add(self, var1, var2):
        return self.unpack(var1) + self.unpack(var2)

    def sub(self, var1, var2):
        return self.unpack(var1) - self.unpack(var2)

    def mul(self, var1, var2):
        return self.unpack(var1) * self.unpack(var2)

    def div(self, var1, var2):
        return self.unpack(var1) / self.unpack(var2)

    def get_monkey_output(self, monkey_string: str):
        try:
            return int(monkey_string)
        except ValueError:
            monkey_str = monkey_string.strip()
            var1, operation, var2 = monkey_str.split()
            match operation:
                case "+":
                    func_return = self.add
                case "-":
                    func_return = self.sub
                case "*":
                    func_return = self.mul
                case _:
                    func_return = self.div
            return func_return, (var1, var2)

    def parse_file(self):
        with open(self.file_path, "r") as file:
            for line in file:
                curr_line = line.strip()
                monkey, monkey_line = curr_line.split(": ")
                self.monkey_dict[monkey] = self.get_monkey_output(monkey_line)
