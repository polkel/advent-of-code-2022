from ..helpers import read_problem, print_to_display, exception_handler
import os


path_to_dir = os.path.dirname(__file__)
input_file = path_to_dir + "\\rope_bridge.txt"
test_file = path_to_dir + "\\test_bridge.txt"


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_head = Head()
        test_tail = Tail(test_head)
        with open(test_file, "r") as file:
            for line in file:
                test_head.process_move(line.rstrip())
                if test_tail.move_required():
                    test_tail.move_to_head()
        assert test_tail.get_all_visited() == 13

    except Exception as e:
        exception_handler(e)


def solve_problem():
    # I thought there would be a mathematical trick to this problem
    # I think it would be easy to find the resulting tail position after every head movement
    # if you know the relative position of the head
    # I guess you still can figure out the starting and ending position of the tail in one movement
    # It will only ever move in the direction that the head goes
    # This way we won't have to simulate every single step of movement
    # We can calculate the tail's movements knowing the head's ending position after every move
    # e.g. both H and T start at (0, 0)
    # If after the first move, H ends up at (1, 0), we know that T doesn't have to move, they are adjacent
    # If after the next move, H is now at (1, 3), T will have to move from (0, 0)
    # First diagonally, because neither coordinate matches H's ending coordinate, so (1, 1)
    # Now T will move one dimensionally towards H until they touch so (1,2)
    # T will only move if either the x or y coordinate absolute difference is greater than 2
    # Then starting point is diagonal if neither x or y coordinate equal
    # Ending tail will always be relative to H. If T moved at all, based on H's if (x, y) is H's ending coordinate
    # T's ending coordinate is for R is (x - 1, y), L (x + 1, y), U (x, y - 1), and D (x, y + 1)
    # T will always be one step behind H if it moved
    head = Head()
    tail = Tail(head)
    with open(input_file, "r") as file:
        for line in file:
            head.process_move(line.rstrip())
            if tail.move_required():
                tail.move_to_head()
    visited_positions = tail.get_all_visited()
    print_to_display(f"The tail visited {str(visited_positions)} positions", bold=True)
    print("\n\n")


class Head:
    def __init__(self):
        self.location = (0, 0)
        self.tail_location = (0, 0)
        self.last_move = None

    def process_move(self, move):
        direction, times = move.split()
        times = int(times)
        # tail is always 1 step behind the head if it has to move
        self.tail_location = coord_helper(self.location, direction, times - 1)
        self.location = coord_helper(self.location, direction, times)
        self.last_move = move


class Tail:
    def __init__(self, head: Head):
        self.location = (0, 0)
        self.head = head
        self.visited = set()
        self.visited.add((0, 0))

    def move_required(self):
        # Checks if tail needs to move after a head movement
        x_diff = abs(self.location[0] - self.head.location[0])
        y_diff = abs(self.location[1] - self.head.location[1])
        if x_diff > 1 or y_diff > 1:
            return True
        return False

    def first_move(self):
        # Finds the first location of T if it needs to move after an H movement
        direction, times = self.head.last_move.split()
        if direction in "RL":
            coordinate = (self.location[0], self.head.location[1])
        else:
            coordinate = (self.head.location[0], self.location[1])
        return coord_helper(coordinate, direction)

    def move_to_head(self):
        curr_coord = self.first_move()
        last_coord = self.head.tail_location
        direction, times = self.head.last_move.split()
        self.visited.add(curr_coord)
        while curr_coord != last_coord:
            curr_coord = coord_helper(curr_coord, direction)
            self.visited.add(curr_coord)
        self.location = curr_coord

    def get_all_visited(self):
        return len(self.visited)


def coord_helper(coordinate, movement, times=1):
    # Takes an input coordinate, and returns it according to the movement and times
    x = coordinate[0]
    y = coordinate[1]
    if movement == "R":
        x += times
    elif movement == "L":
        x -= times
    elif movement == "U":
        y += times
    elif movement == "D":
        y -= times
    return x, y
