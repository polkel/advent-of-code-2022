from ..helpers import read_problem, print_to_display, exception_handler
from . import day09_1


test_file = day09_1.path_to_dir + "\\test_bridge_2.txt"


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        rope_knots = 10
        head = Knot()
        tail = head
        for _ in range(rope_knots - 1):
            tail = tail.add_tail()
        with open(test_file, "r") as file:
            for line in file:
                direction, times = line.rstrip().split()
                times = int(times)
                head.process_move(direction, times)
        assert tail.get_visited() == 36
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # Need to make a more general knot class
    # A knot can be a head if the head property is None
    # We can add tail attribute as well, to link all the knots
    # for every movement, we will have to process all movements starting at the head sequentially
    # I have to modify the first move method from the first part
    # I think I'll just create a new class instead of inheriting the last one
    # Okay this idea doesn't work. We need to process moves of the knots one at a time
    rope_knots = 10
    head = Knot()
    tail = head
    for _ in range(rope_knots - 1):
        tail = tail.add_tail()
    with open(day09_1.input_file, "r") as file:
        for line in file:
            direction, times = line.rstrip().split()
            times = int(times)
            head.process_move(direction, times)
    print_to_display(f"The tail visited {str(tail.get_visited())} positions with {str(rope_knots)} knots", bold=True)
    print("\n\n")


class Knot:
    def __init__(self, head=None):
        self.head = head
        self.tail = None
        self.location = (0, 0)
        self.visited = set()
        self.visited.add(self.location)

    def process_move(self, direction: str, times: int):
        self.location = day09_1.coord_helper(self.location, direction)
        if self.tail is not None:
            self.tail.move_to_head()
        self.visited.add(self.location)
        if times != 1:
            self.process_move(direction, times - 1)

    def move_to_head(self):  # we can modify this later, this always should just always go to the first move
        if self.move_required():
            curr_loc = self.find_first_move()
            head_loc = self.head.location
            curr_x = curr_loc[0]
            curr_y = curr_loc[1]
            head_x = head_loc[0]
            head_y = head_loc[1]
            if curr_x < head_x:
                direction = "R"
            elif curr_x > head_x:
                direction = "L"
            elif curr_y < head_y:
                direction = "U"
            else:
                direction = "D"
            while self.move_required():
                self.visited.add(curr_loc)
                self.location = curr_loc
                curr_loc = day09_1.coord_helper(curr_loc, direction)
            if self.tail is not None:
                self.tail.move_to_head()

    def add_tail(self):
        self.tail = Knot(self)
        return self.tail

    def move_required(self):
        x = self.location[0]
        y = self.location[1]
        head_x = self.head.location[0]
        head_y = self.head.location[1]
        if abs(x - head_x) > 1 or abs(y - head_y) > 1:
            return True
        return False

    def find_first_move(self):
        next_x = self.location[0]
        next_y = self.location[1]
        head_x = self.head.location[0]
        head_y = self.head.location[1]
        if next_x < head_x:
            next_x += 1
        elif next_x > head_x:
            next_x -= 1
        if next_y < head_y:
            next_y += 1
        elif next_y > head_y:
            next_y -= 1
        return next_x, next_y

    def get_visited(self):
        return len(self.visited)
