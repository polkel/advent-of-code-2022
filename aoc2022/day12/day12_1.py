from ..helpers import read_problem, print_to_display, exception_handler
import os


path_to_dir = os.path.dirname(__file__)
input_file = path_to_dir + "\\elevation_map.txt"
test_file = path_to_dir + "\\test_elevation.txt"


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        grid = Grid(test_file)
        path = Path(grid)
        assert path.steps == 31
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # Looks like a graph problem
    # We can implement a BFS algorithm to find the shortest path
    # Let's create a function to convert the array of letters to an array of Nodes with the letter converted to values
    # using ord
    # We can find the neighbors as it iterates through the BFS so that we don't have to do it for every node
    grid = Grid(input_file)
    path = Path(grid)
    print_to_display(f"The fewest number of steps to get to good signal is {str(path.steps)}", bold=True)
    print("\n\n")


class Node:
    def __init__(self, letter: str, coordinate: tuple):
        self.letter = letter
        self.coordinate = coordinate  # tuple pair row, column (0, 0) top left
        self.value = None
        self.get_letter_value()

    def get_letter_value(self):
        if self.letter == "S":
            self.value = ord("a")
        elif self.letter == "E":
            self.value = ord("z")
        else:
            self.value = ord(self.letter)

    def __str__(self):
        return self.letter

    def __repr__(self):
        return self.letter

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.coordinate == other.coordinate

    def __hash__(self):
        return hash(self.coordinate)

    def __ne__(self, other):
        if not isinstance(other, Node):
            return True
        return self.coordinate != other.coordinate


class Grid:
    def __init__(self, elevation_file_path: str):
        self.grid = []  # I'll just use lists instead of numpy
        self.start = None
        self.end = None
        self.file_path = elevation_file_path
        self.get_grid()
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def get_grid(self):
        if self.grid:
            return
        with open(self.file_path, "r") as file:
            row = 0
            for line in file:
                new_row = []
                curr_line = line.rstrip()
                for col in range(len(curr_line)):
                    curr_letter = curr_line[col]
                    curr_node = Node(curr_letter, (row, col))
                    if curr_letter == "S":
                        self.start = curr_node
                    elif curr_letter == "E":
                        self.end = curr_node
                    new_row.append(curr_node)
                self.grid.append(new_row)
                row += 1

    def get_node(self, row: int, col: int):
        try:
            if row < 0 or col < 0:
                raise IndexError
            return self.grid[row][col]
        except IndexError:
            return None

    def __str__(self):
        return str(self.grid)

    def __repr__(self):
        return str(self.grid)


class Path:
    def __init__(self, grid: Grid):
        self.path_coords = None
        self.grid = grid
        self.visited = set()
        self.find_shortest_path()
        self.steps = len(self.path_coords) - 1

    def find_shortest_path(self):  # This should be bfs...
        curr_depth = [(self.grid.start, [])]  # tuple of current node and the visited path
        self.visited.add(self.grid.start)
        self._real_bfs_helper(curr_depth)

    def _real_bfs_helper(self, depth):
        new_depth = []
        if len(depth) == 0 or self.path_coords is not None:
            return
        for node, curr_path in depth:
            curr_path.append(node)
            if node == self.grid.end:
                self.path_coords = curr_path
                break
            row = node.coordinate[0]
            col = node.coordinate[1]
            up = (row - 1, col)
            down = (row + 1, col)
            left = (row, col - 1)
            right = (row, col + 1)
            directions = [up, down, left, right]
            for direction in directions:
                curr_node = self.grid.get_node(*direction)
                not_none = curr_node is not None
                if not_none:
                    not_visited = curr_node not in self.visited
                    climbable = curr_node.value - node.value <= 1
                    if climbable and not_visited:
                        new_path = curr_path[:]
                        new_depth.append((curr_node, new_path))
                        self.visited.add(curr_node)
        self._real_bfs_helper(new_depth)

    def _bfs_helper(self, node: Node, this_path: set):  # This is not bfs... this is dfs
        if self.path_coords is not None:
            return
        this_path.add(node)
        self.visited.add(node)
        if node == self.grid.end:
            this_path.add(self.grid.end)
            self.path_coords = this_path
            return
        row = node.coordinate[0]
        col = node.coordinate[1]
        up = (row - 1, col)
        down = (row + 1, col)
        left = (row, col - 1)
        right = (row, col + 1)
        directions = [up, down, left, right]
        for direction in directions:
            curr_node = self.grid.get_node(*direction)
            not_none = curr_node is not None
            not_visited = curr_node not in self.visited
            if not_none and not_visited:
                climbable = curr_node.value - node.value <= 1
                if climbable:
                    self._bfs_helper(curr_node, this_path)
