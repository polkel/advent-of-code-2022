from ..helpers import read_problem, print_to_display, exception_handler
from . import day11_1


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        monkey_business = MonkeyBusinessNoRelief(day11_1.test_file)
        monkey_business.start_monkeys_no_relief(10000)
        assert monkey_business.get_monkey_business() == 2713310158
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # Let's inherit the class, but have no relief
    # It isn't optimized, seems to be holding up on multiplication processes
    # I think that it's struggling to work with really large numbers
    # Okay, we don't have to work with really large numbers!
    # We just have to work with numbers that are as many digits as the operations call for
    # Ok I'm not sure how the math works
    # But if you just take the modulus by the first common multiple of all the monkey tests it works
    # So I'm not sure tbh, not happy with how I got here. I'm not a math guy :(
    monkey_business = MonkeyBusinessNoRelief(day11_1.input_file)
    monkey_business.start_monkeys_no_relief(10000)
    business_value = monkey_business.get_monkey_business()
    print_to_display(f"The total amount of monkey business after 10000 rounds is {str(business_value)}", bold=True)
    print("\n\n")


class MonkeyBusinessNoRelief(day11_1.MonkeyBusiness):
    def __init__(self, monkey_file):
        super().__init__(monkey_file)
        self.group_factor = self.find_monkey_nums()

    def find_monkey_nums(self):
        curr_monkey_factor = 1
        for monkey in self.monkey_group:
            for i in range(1, 99):
                if monkey.test(i):
                    curr_monkey_factor *= i
                    break
        return curr_monkey_factor

    def start_monkeys_no_relief(self, rounds):
        for i in range(rounds):
            for monkey in self.monkey_group:
                while monkey.has_item():
                    monkey.inspect_item()
                    monkey.items[-1] = monkey.items[-1] % self.group_factor
                    monkey.throw_item()
