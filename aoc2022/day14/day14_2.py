from ..helpers import read_problem, print_to_display, exception_handler
from .day14_1 import Cave, test_file, input_file, np


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_cave = Cave2(test_file)
        test_cave.generate_cave()
        test_cave.fill_sand()
        assert test_cave.get_sand() == 93
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # The total width of the pyramid formed by the sand can be found with the formula
    # w = (h - 2) * 2 + 1
    # where h is the height of the array (including the floor and the entry row)
    # w is centered at the entry point
    # so on each side of the entry point, the pyramid is h - 2 in length (not including the unit at the center)
    # so if we want the simulation to end without the sand going off the edge, the width should be 2h + 1
    # with the center at the sand entry
    cave = Cave2(input_file)
    cave.generate_cave()
    cave.fill_sand()
    sands = cave.get_sand()
    print_to_display(f"With the floor, there are {str(sands)} units of sand that come to rest", bold=True)
    print("\n\n")


class Cave2(Cave):
    def __init__(self, file_path):
        super().__init__(file_path)

    def generate_cave(self):
        walls = set()  # (row, col) coordinate of a wall, unadjusted for minimum wall
        with open(self.file_path, "r") as file:
            max_row = 0
            for line in file:
                whole_wall = line.strip().split(" -> ")
                col, row = whole_wall[0].split(",")
                row = int(row)
                col = int(col)
                if row > max_row:
                    max_row = row
                walls.add((row, col))
                for i in range(1, len(whole_wall)):
                    col2, row2 = whole_wall[i].split(",")
                    col1, row1 = whole_wall[i - 1].split(",")
                    row1, col1, row2, col2 = int(row1), int(col1), int(row2), int(col2)
                    if row2 > max_row:
                        max_row = row2
                    curr_walls = self.generate_points((row1, col1), (row2, col2))
                    walls.update(curr_walls)
        self.height = max_row + 1 + 2
        self.width = self.height * 2 + 1
        self.adjusted_entry = (0, self.height)
        self.col_adjustment = self.sand_entry[1] - self.adjusted_entry[1]
        self.cave_array = np.full((self.height, self.width), self.empty_symbol)
        self.cave_array[self.adjusted_entry] = self.entry_symbol
        for wall in walls:
            wall_adjusted = (wall[0], wall[1] - self.col_adjustment)
            self.cave_array[wall_adjusted] = self.wall_symbol
        for i in range(self.width):
            self.cave_array[self.height - 1, i] = self.wall_symbol
