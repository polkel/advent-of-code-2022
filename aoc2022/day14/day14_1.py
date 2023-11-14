from ..helpers import read_problem, print_to_display, exception_handler
import numpy as np
import sys
import os


np.set_printoptions(threshold=np.inf)
path_to_dir = os.path.dirname(__file__)
input_file = path_to_dir + "\\input_cave.txt"
test_file = path_to_dir + "\\test_cave.txt"


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_cave = Cave(test_file)
        test_cave.generate_cave()
        test_cave.fill_sand()
        assert test_cave.get_sand() == 24
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # We will need a couple things
    # First we need to extract all the nodes of walls from the text input
    # That can be done with a couple of split operations
    # Next we will need to store all the wall positions (coordinates) in a set to check against later
    # Maybe we can store a physical array in a numpy to do this easier...
    # If we only keep the wall coordinates in a set, it will have to scan through linearly through the set
    # every time it checks if it can move down
    # If we store it once in an array, then we can just immediately pull the data from the specific index
    # So I think we can make a class called grid
    # And it will adjust the column position x to 0 wherever the minimum wall is
    # We'll also have to simulate a sand class (maybe)
    # The sand will forever flow into the abyss the moment that a sand piece goes beyond the last wall
    # either on the left, right, or bottom
    # or if the entry point is blocked with sand (500, 1)
    # That will be our trigger to stop adding sand and return how much sand is in the cave
    # The weird thing about the text file is that the first number is actually the column
    # the second number is the row, so we'll have to flip it
    cave = Cave(input_file)
    cave.generate_cave()
    cave.fill_sand()
    sands = cave.get_sand()
    print_to_display(f"There are {str(sands)} units of sand that are at rest", bold=True)
    print("\n\n")


class Cave:
    def __init__(self, file_path):
        self.file_path = file_path
        self.cave_array = None
        self.col_adjustment = None
        self.sand_entry = (0, 500)
        self.adjusted_entry = None
        self.wall_symbol = "#"
        self.empty_symbol = "."
        self.sand_symbol = "o"
        self.entry_symbol = "+"
        self.width = None
        self.height = None

    def generate_cave(self):
        walls = set()  # (row, col) coordinate of a wall, unadjusted for minimum wall
        with open(self.file_path, "r") as file:
            min_col = 1000
            max_col = 0
            max_row = 0
            for line in file:
                whole_wall = line.strip().split(" -> ")
                col, row = whole_wall[0].split(",")
                row = int(row)
                col = int(col)
                if row > max_row:
                    max_row = row
                if col > max_col:
                    max_col = col
                if col < min_col:
                    min_col = col
                walls.add((row, col))
                for i in range(1, len(whole_wall)):
                    col2, row2 = whole_wall[i].split(",")
                    col1, row1 = whole_wall[i - 1].split(",")
                    row1, col1, row2, col2 = int(row1), int(col1), int(row2), int(col2)
                    if col2 > max_col:
                        max_col = col2
                    if col2 < min_col:
                        min_col = col2
                    if row2 > max_row:
                        max_row = row2
                    curr_walls = self.generate_points((row1, col1), (row2, col2))
                    walls.update(curr_walls)
        self.col_adjustment = min_col
        self.height = max_row + 1
        self.width = max_col - min_col + 1
        self.adjusted_entry = (0, self.sand_entry[1] - self.col_adjustment)
        self.cave_array = np.full((self.height, self.width), self.empty_symbol)
        self.cave_array[self.adjusted_entry] = self.entry_symbol
        for wall in walls:
            wall_adjusted = (wall[0], wall[1] - self.col_adjustment)
            self.cave_array[wall_adjusted] = self.wall_symbol

    @staticmethod
    def generate_points(point1: tuple, point2: tuple):
        row1, col1 = point1
        row2, col2 = point2
        row = row1
        col = col1
        wall_section = set()
        if row1 != row2:
            high_row = row1
            low_row = row2
            if row2 > row1:
                high_row, low_row = low_row, high_row
            for i in range(low_row, high_row + 1):
                wall_section.add((i, col))
        if col1 != col2:
            high_col = col1
            low_col = col2
            if col2 > col1:
                high_col, low_col = low_col, high_col
            for i in range(low_col, high_col + 1):
                wall_section.add((row, i))
        return wall_section

    def print_cave(self):
        cave_string = np.array2string(self.cave_array)
        cave_string = cave_string.replace("\n", "").replace(" [", "").replace("[", "")
        cave_string = cave_string.replace("] ", "\n").replace("]", "\n").replace("'", "").replace("  ", " ")
        print(cave_string)

    def fill_sand(self):
        sand_row, sand_col = self.adjusted_entry
        directions = [(1, 0), (1, -1), (1, 1)]
        while sand_row < self.height and 0 <= sand_col < self.width:
            for direction in directions:
                new_row = sand_row + direction[0]
                new_col = sand_col + direction[1]
                if new_row >= self.height or new_col < 0 or new_col >= self.width:
                    sand_row, sand_col = new_row, new_col
                    break
                if self.cave_array[new_row, new_col] == self.empty_symbol:
                    sand_row, sand_col = new_row, new_col
                    break
            else:
                self.cave_array[sand_row, sand_col] = self.sand_symbol
                if (sand_row, sand_col) == self.adjusted_entry:
                    sand_row, sand_col = self.height, self.width  # This is to break out if the entry is full
                else:
                    sand_row, sand_col = self.adjusted_entry

    def get_sand(self):
        return len(np.where(self.cave_array == self.sand_symbol)[0])
