import re

from ..helpers import read_problem, print_to_display, exception_handler
import os


path_to_dir = os.path.dirname(__file__)
input_file = path_to_dir + "\\path.txt"
test_file = path_to_dir + "\\test_path.txt"


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        assert get_password(test_file) == 6032
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # As we traverse through the input file, let's keep track of the maxes and mins of each row and column
    # any time there is an item, we update the row or column max
    # and also store each item as a set of spaces or a set of walls
    # As for the path traversal, my first instinct is to step through everything one at a time
    # Algo for finding walls and spaces is
    # start at 1 for rows, enumerate the letters
    # First check if it's an object, if it is, update the rows max min, update columns max min
    # Then depending on if it's a wall or a space, store the coordinate in the proper set
    # If the line is equal to \n
    # We know the next line is the path string, so we store the next line
    password = get_password(input_file)
    print_to_display(f"The final password is {str(password)}", bold=True)
    print("\n\n")


class Maze:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.row_limits = dict()
        self.col_limits = dict()
        self.walls = set()
        self.paths = set()
        self.instructions = None
        self.parse_file()

    def parse_file(self):
        with open(self.file_path, "r") as file:
            row = 1
            last_line = ""
            for line in file:
                last_line = line.strip("\n")
                for i, letter in enumerate(last_line):
                    col = i + 1
                    if letter in ".#":
                        curr_coord = (row, col)
                        self.update_limits((row, col))
                        if letter == ".":
                            self.paths.add(curr_coord)
                        else:
                            self.walls.add(curr_coord)
                row += 1
        self.instructions = last_line

    def update_limits(self, coordinate: tuple):
        row, col = coordinate
        self.set_limit(self.row_limits, row, col)
        self.set_limit(self.col_limits, col, row)

    @staticmethod
    def set_limit(limit_dict: dict, index: int, value: int):
        try:
            if limit_dict[index]["max"] < value:
                limit_dict[index]["max"] = value
            if limit_dict[index]["min"] > value:
                limit_dict[index]["min"] = value
        except KeyError:
            limit_dict[index] = dict()
            limit_dict[index]["max"] = value
            limit_dict[index]["min"] = value

    def get_start_coord(self):
        row = 1
        col = self.row_limits[row]["min"]
        return row, col


class Traveler:
    def __init__(self, start_coord: tuple, path_string: str):
        self.location = start_coord
        self.path_string = path_string
        self.moves = []
        self.turns = []
        self.turn_index = 0
        self.turn_order = ["R", "D", "L", "U"]
        self.direction = (0, 1)
        self.moves_re = re.compile(r"\d+")
        self.turns_re = re.compile(r"[RL]")
        self.get_moves_turns()

    def get_moves_turns(self):
        self.moves = self.moves_re.findall(self.path_string)
        self.turns = self.turns_re.findall(self.path_string)

    def turn(self, turn_letter: str):
        if turn_letter == "R":
            self.turn_index += 1
        else:
            self.turn_index -= 1
        self.turn_index = self.turn_index % len(self.turn_order)
        self.set_direction()

    def set_direction(self):
        dir_letter = self.turn_order[self.turn_index]
        direction = None
        match dir_letter:
            case "R":
                direction = (0, 1)
            case "D":
                direction = (1, 0)
            case "L":
                direction = (0, -1)
            case _:
                direction = (-1, 0)
        self.direction = direction

    def move_paths(self, maze: Maze):
        move_index = 0
        while move_index < len(self.moves):
            curr_move = int(self.moves[move_index])
            for _ in range(curr_move):
                row, col = self.location
                add_row, add_col = self.direction
                next_row, next_col = row + add_row, col + add_col
                if (next_row, next_col) not in maze.paths and (next_row, next_col) not in maze.walls:
                    match self.turn_order[self.turn_index]:
                        case "R":
                            next_col = maze.row_limits[row]["min"]
                        case "L":
                            next_col = maze.row_limits[row]["max"]
                        case "D":
                            next_row = maze.col_limits[col]["min"]
                        case "U":
                            next_row = maze.col_limits[col]["max"]
                next_coord = (next_row, next_col)
                if next_coord in maze.walls:
                    break
                else:
                    self.location = next_coord
            try:
                turn = self.turns[move_index]
                self.turn(turn)
            except IndexError:
                pass
            move_index += 1


def get_password(file_path: str):
    maze = Maze(file_path)
    traveler = Traveler(maze.get_start_coord(), maze.instructions)
    traveler.move_paths(maze)
    password = 1000 * traveler.location[0] + 4 * traveler.location[1] + traveler.turn_index
    return password
