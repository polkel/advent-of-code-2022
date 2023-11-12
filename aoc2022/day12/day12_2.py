from ..helpers import read_problem, print_to_display, exception_handler
from .day12_1 import Node, Grid, Path, input_file, test_file


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        grid = Grid(test_file)
        assert find_min_path_from_a(grid) == 29
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # Let's see what happens if we just run a BFS for every "a" in the grid
    grid = Grid(input_file)
    min_path = find_min_path_from_a(grid)
    print_to_display(f"The fewest steps required to get from any a to E is {str(min_path)}", bold=True)


def find_min_path_from_a(grid: Grid):
    path = PathExtended(grid)
    min_path = None
    for row in grid.grid:
        for node in row:
            if node.letter == "a" or node.letter == "S":
                curr_path = path.find_shortest_path_node(node)
                if curr_path is None:
                    continue
                if min_path is None or curr_path < min_path:
                    min_path = curr_path
    return min_path


class PathExtended(Path):
    def __init__(self, grid):
        super().__init__(grid)
        self.visited = set()
        self.path_coords = None

    def find_shortest_path_node(self, node: Node):
        curr_depth = [(node, [])]
        self.visited.add(node)
        self._real_bfs_helper(curr_depth)
        self.visited = set()
        if self.path_coords is None:
            return None
        path_len = len(self.path_coords) - 1
        self.path_coords = None
        return path_len
