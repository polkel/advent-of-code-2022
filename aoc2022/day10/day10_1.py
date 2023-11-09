from ..helpers import read_problem, print_to_display, exception_handler
import os


path_to_dir = os.path.dirname(__file__)
input_file = path_to_dir + "\\input_program.txt"
test_file = path_to_dir + "\\test_program.txt"


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_screen = Screen(test_file)
        test_screen.start_program()
        assert test_screen.get_signal_sum() == 13140
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # Let's create a class to handle the inputs and record the signal strengths at the intervals asked for
    screen = Screen(input_file)
    screen.start_program()
    signal_strength_sum = screen.get_signal_sum()
    print_to_display(f"The sum of the 6 signal strengths is {str(signal_strength_sum)}", bold=True)
    print("\n\n")


class Screen:
    def __init__(self, command_file: str):
        self.signal_strengths = dict()
        self.curr_command = None
        self.curr_tick = 0
        self.x_register = 1
        self.command_file = command_file

    def record_signal_strength(self):
        record_interval = (self.curr_tick - 20) % 40 == 0
        if not record_interval:
            return
        curr_strength = self.curr_tick * self.x_register
        self.signal_strengths[self.curr_tick] = curr_strength

    def start_program(self):
        with open(self.command_file, "r") as file:
            for line in file:
                self.curr_command = Command(line.rstrip())
                while self.curr_command is not None:
                    self.process_tick()
                    self.record_signal_strength()
                    if self.curr_command.execute_command():  # The command change only registers after the tick
                        self.x_register += self.curr_command.register_change
                        self.curr_command = None

    def process_tick(self):
        self.curr_tick += 1
        self.curr_command.process_tick()

    def get_signal_sum(self, tick_limit=220):
        curr_sum = 0
        for tick_num, signal_strength in self.signal_strengths.items():
            if tick_num <= tick_limit:
                curr_sum += signal_strength
        return curr_sum


class Command:
    def __init__(self, command_str):
        self.ticks_remaining = None
        self.register_change = 0
        self.command_str = command_str
        self.parse_command()

    def parse_command(self):
        commands = self.command_str.split()
        if len(commands) == 1:  # This is noop
            self.ticks_remaining = 1
        else:
            self.ticks_remaining = 2
            self.register_change = int(commands[1])

    def execute_command(self):
        if self.ticks_remaining == 0:
            return True
        return False

    def process_tick(self):
        self.ticks_remaining -= 1
