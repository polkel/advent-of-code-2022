from ..helpers import read_problem, print_to_display, exception_handler
import re
import os


path_to_dir = os.path.dirname(__file__)
input_file = path_to_dir + "\\input_monkeys.txt"
test_file = path_to_dir + "\\test_monkeys.txt"


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        monkey_business = MonkeyBusiness(test_file)
        monkey_business.start_monkeys(20)
        monkey1 = monkey_business.monkey_group[0]
        monkey2 = monkey_business.monkey_group[1]
        monkey3 = monkey_business.monkey_group[2]
        monkey4 = monkey_business.monkey_group[3]
        assert monkey1.inspections == 101
        assert monkey2.inspections == 95
        assert monkey3.inspections == 7
        assert monkey4.inspections == 105
        assert monkey_business.get_monkey_business() == 10605
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # The monkey's inventory acts like a queue, because it throws whatever is first
    # and receives anything at the back of the queue
    # Each monkey behaves the same way, however their inspection worry operations, tests, and recipients are different
    # Firstly, we'll need to find a way to extract each monkey from the input
    # The relief after inspection is always divided by 3, so that can be integer division
    # I also have to track how many times each monkey has inspected an item, not hard at all
    # Lastly we need to find the top two inspection times and multiply to figure out monkey business value
    # It seems that the items thrown are not important, so I don't have to create a class for them
    # I think I need to create a Monkey class
    # Then I need to create a MonkeyBusiness class that would just handle every round and things outside the monkeys
    monkey_business = MonkeyBusiness(input_file)
    monkey_business.start_monkeys(20)
    monkey_value = monkey_business.get_monkey_business()
    print_to_display(f"After 20 rounds, the amount of monkey business is {monkey_value}", bold=True)
    print("\n\n")


class Monkey:
    def __init__(self, items: list, operation, test, true_monkey, false_monkey, tribe):
        self.items = items
        self.operation = operation
        self.test = test
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.inspections = 0
        self.tribe = tribe

    def inspect_item(self):  # I'll only make it so that the monkeys can only see the next in queue
        item = self.items.pop()
        item = self.operation(item)
        self.items.append(item)
        self.inspections += 1

    def relief_item(self):
        item = self.items.pop()
        item = item // 3
        self.items.append(item)

    def throw_item(self):
        item = self.items.pop()
        if self.test(item):
            receiver = self.true_monkey
        else:
            receiver = self.false_monkey
        self.tribe[receiver].receive_item(item)

    def receive_item(self, item):
        self.items.insert(0, item)

    def has_item(self):
        if len(self.items) > 0:
            return True
        return False


class MonkeyBusiness:
    def __init__(self, monkey_file):
        self.monkey_group = []
        self.monkey_file = monkey_file
        self.re_tests = self._create_re_tests()
        self._create_monkey_group()

    def _create_monkey_group(self):
        with open(self.monkey_file, "r") as file:
            full_text = file.read()
        monkey_list = re.split("Monkey \d+:\n  ", full_text)
        monkey_list = monkey_list[1:]  # Get rid of empty string from split
        for monkey_text in monkey_list:
            self.monkey_group.append(self._monkey_from_text(monkey_text))

    def _monkey_from_text(self, monkey_paragraph):
        items = self.re_tests["items"].search(monkey_paragraph)
        operation = self.re_tests["operation"].search(monkey_paragraph)
        test = self.re_tests["test"].search(monkey_paragraph)
        true_monkey = self.re_tests["true"].search(monkey_paragraph)
        false_monkey = self.re_tests["false"].search(monkey_paragraph)
        item_list = items[0].strip().split(", ")
        if item_list[0] != "":
            new_list = []
            for i in range(len(item_list)):
                new_list.insert(0, int(item_list[i]))
            item_list = new_list
        else:
            item_list = []
        operation = operation[0]
        operation = operation.replace(" new = ", "")
        operation_inputs = operation.split()
        operation_func = self._create_operation(*operation_inputs)
        test = test[0]
        test_func = self._create_test(test)
        true_monkey = int(true_monkey[0].split()[-1])
        false_monkey = int(false_monkey[0].split()[-1])
        return Monkey(item_list, operation_func, test_func, true_monkey, false_monkey, self.monkey_group)

    @staticmethod
    def _create_re_tests():
        items_re = re.compile("(?<=Starting items:).*(?=\n)")
        operation_re = re.compile("(?<=Operation:).*(?=\n)")
        test_re = re.compile("(?<=Test:).*(?=\n)")
        true_re = re.compile("(?<=If true:).*(?=\n)")
        false_re = re.compile("(?<=If false:).*")
        re_dict = dict()
        re_dict["items"] = items_re
        re_dict["operation"] = operation_re
        re_dict["test"] = test_re
        re_dict["true"] = true_re
        re_dict["false"] = false_re
        return re_dict

    @staticmethod
    def _create_operation(var1, op, var2):  # This will return a function based on the operation listed
        if var1 == var2:
            if op == "+":  # we can add more ops later if needed
                return lambda x: x + x
            else:
                return lambda x: x * x
        else:
            if op == "+":
                return lambda x: x + int(var2)
            else:
                return lambda x: x * int(var2)

    @staticmethod
    def _create_test(test_line):  # Will return true or false function for each monkey
        # It's always going to be a divisible check
        num = int(test_line.split()[-1])
        return lambda x: (x % num) == 0

    def start_monkeys(self, rounds: int):
        for _ in range(rounds):
            for monkey in self.monkey_group:
                while monkey.has_item():
                    monkey.inspect_item()
                    monkey.relief_item()
                    monkey.throw_item()

    def get_monkey_business(self):
        first_max = 0
        second_max = 0
        for monkey in self.monkey_group:
            if monkey.inspections > second_max:
                second_max = monkey.inspections
            if monkey.inspections > first_max:
                second_max = first_max
                first_max = monkey.inspections
        return first_max * second_max
