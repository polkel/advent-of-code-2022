from ..helpers import read_problem, print_to_display, exception_handler
import os


path_to_dir = os.path.dirname(__file__)
input_file = path_to_dir + "\\input.txt"
test_file = path_to_dir + "\\test_input.txt"


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        node_list, zero_node = get_node_list(test_file)
        list_len = len(node_list)
        for node in node_list:
            node.shift_node(list_len)
        result_node_1 = get_x_element_from_node(zero_node, 1000, list_len)
        result_node_2 = get_x_element_from_node(zero_node, 2000, list_len)
        result_node_3 = get_x_element_from_node(zero_node, 3000, list_len)
        assert result_node_1.value == 4
        assert result_node_2.value == -3
        assert result_node_3.value == 2
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # This might be easy with cyclical linked lists?
    # Each node will be indexed in a linked list class
    # We keep track of each node in a separate list to iterate through it in the original order
    # To find the x'th element from an index i in the list, the index is (i + x) % len(list)
    # Need to consider the case where a number wraps around the list to its original position
    # How do you handle the new index?
    # So if you move in any direction a distance where distance % (len(list) - 1) == 0, you get back to original spot
    # So always do that when calculating distance
    # In a sequence like [9, 8, 7, 6, 5, 4]
    # The original index of 9 is 0, but it ends up at index 4 at the end
    # So index result is (original index + (num % (len(list) - 1))) % len(list)
    # (0 + (9 % (6 - 1))) % 6 = 4
    # Let's find the location of the second element, assuming all previous elements have already moved
    # (1 + (8 % (6 - 1))) % 6 = 4
    # (5 + (4 % (5)) % 6 = 3
    # We just have to link everything from head to tail
    # Then we have to find a fast way to calculate the index
    # Position change = abs(num) % (len(list) - 1)
    # direction is dictated by num positivity (right) or negativity (left)
    # [1, 4, 2, -6, 3, 2]
    # Let's just try to iterate this the straightforward way, then we can find a smarter way later
    node_list, zero_node = get_node_list(input_file)
    for node in node_list:
        node.shift_node(len(node_list))
    coordinates_sum = get_grove_coordinates(zero_node, len(node_list))
    print_to_display(f"The sum of the grove coordinates is {str(coordinates_sum)}", bold=True)
    print("\n\n")


class Node:
    def __init__(self, value: int, head=None, tail=None):
        self.head = head
        self.tail = tail
        self.value = value

    def shift_node(self, list_len: int):
        direction = "head"
        opp_direction = "tail"
        if self.value > 0:
            direction = "tail"
            opp_direction = "head"
        shifts = abs(self.value) % (list_len - 1)
        if self.value == 0 or shifts == 0:
            return
        next_node = getattr(self, direction)
        self.head.tail = self.tail
        self.tail.head = self.head
        for _ in range(shifts - 1):
            next_node = getattr(next_node, direction)
        setattr(self, direction, getattr(next_node, direction))
        setattr(self, opp_direction, next_node)
        setattr(getattr(next_node, direction), opp_direction, self)
        setattr(next_node, direction, self)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


def get_node_list(file_path):  # returns node list and the zero node
    node_list = []
    zero_node = None
    with open(file_path, "r") as file:
        for line in file:
            last_node = None
            if node_list:
                last_node = node_list[-1]
            new_node = Node(int(line.strip()), last_node)
            if last_node:
                last_node.tail = new_node
            node_list.append(new_node)
            if new_node.value == 0:
                zero_node = new_node
    node_list[0].head = node_list[-1]
    node_list[-1].tail = node_list[0]
    return node_list, zero_node


def get_list_from_node(node: Node):
    node_list = []
    next_node = node.tail
    node_list.append(node)
    while next_node != node:
        node_list.append(next_node)
        next_node = next_node.tail
    return node_list


def get_x_element_from_node(node: Node, elements: int, list_len: int):
    traversal = elements % list_len
    result_node = node
    for _ in range(traversal):
        result_node = result_node.tail
    return result_node


def get_grove_coordinates(zero_node: Node, list_len: int):
    coordinates = [1000, 2000, 3000]
    sum_coords = 0
    for coord in coordinates:
        sum_coords += get_x_element_from_node(zero_node, coord, list_len).value
    return sum_coords
