from ..helpers import read_problem, print_to_display, exception_handler
from .day10_1 import Screen, Command, input_file, test_file, path_to_dir


test_solution = path_to_dir + "\\test_solution.txt"


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_screen = ScreenWriter(test_file)
        test_screen.start_program()
        # test_screen.print_screen()  # just a visual check
        with open(test_solution, "r") as file:
            test_output = ""
            for line in file:
                test_output += line
        assert test_screen.screen_text.rstrip() == test_output.rstrip()
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # Let us inherit the Screen class and improve upon it in this file
    screen = ScreenWriter(input_file)
    screen.start_program()
    screen.print_screen()
    print("\n\n")
    print_to_display("The 8 letters that appear are RKPJBPLA", bold=True)
    print("\n\n")


class ScreenWriter(Screen):
    def __init__(self, command_file):
        super().__init__(command_file)
        self.screen_text = ""
        self.screen_size = 40

    def get_cursor_position(self):
        return (self.curr_tick - 1) % self.screen_size

    def is_cursor_on_sprite(self):
        if self.get_cursor_position() in range(self.x_register - 1, self.x_register + 2):
            return True
        return False

    def cursor_end_of_line(self):
        if self.get_cursor_position() + 1 == self.screen_size:
            return True
        return False

    def start_program(self):
        with open(self.command_file, "r") as file:
            for line in file:
                self.curr_command = Command(line.rstrip())
                while self.curr_command is not None:
                    self.process_tick()
                    if self.is_cursor_on_sprite():
                        self.screen_text += "#"
                    else:
                        self.screen_text += "."
                    if self.cursor_end_of_line():
                        self.screen_text += "\n"
                    if self.curr_command.execute_command():  # The command change only registers after the tick
                        self.x_register += self.curr_command.register_change
                        self.curr_command = None

    def print_screen(self):
        print(self.screen_text)
