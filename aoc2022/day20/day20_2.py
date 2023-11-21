from ..helpers import read_problem, print_to_display, exception_handler
from .day20_1 import Node, get_x_element_from_node, get_node_list, get_list_from_node, test_file, input_file


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        node_list, zero_node = get_node2_list(test_file)
        list_len = len(node_list)
        for node in node_list:
            node.create_real_value(list_len)
        for _ in range(10):
            for node in node_list:
                node.shift_node(list_len)
        assert get_grove_sum_node2(zero_node, list_len) == 1623178306
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # Modify the node class, store the actual value in a different attribute
    # We need to keep the current "value" field as the effective shifting number
    # The effective shifting number is the (abs(product) % (len(list) - 1)) neg or positive
    node_list, zero_node = get_node2_list(input_file)
    list_len = len(node_list)
    for node in node_list:
        node.create_real_value(list_len)
    for _ in range(10):
        for node in node_list:
            node.shift_node(list_len)
    grove_sum = get_grove_sum_node2(zero_node, list_len)
    print_to_display(f"The sum of the three coordinates is {str(grove_sum)}", bold=True)
    print("\n\n")


class Node2(Node):
    def __init__(self, value: int, head=None, tail=None):
        super().__init__(value, head, tail)
        self.multiplication_factor = 811589153
        self.actual_value = None

    def create_real_value(self, list_len: int):
        self.actual_value = self.multiplication_factor * self.value
        is_neg = False
        if self.value < 0:
            is_neg = True
        self.value = abs(self.actual_value) % (list_len - 1)
        if is_neg:
            self.value = -self.value

    def __str__(self):
        return str(self.actual_value)

    def __repr__(self):
        return str(self.actual_value)


def get_node2_list(file_path):
    node_list = []
    zero_node = None
    with open(file_path, "r") as file:
        for line in file:
            last_node = None
            if node_list:
                last_node = node_list[-1]
            new_node = Node2(int(line.strip()), last_node)
            if last_node:
                last_node.tail = new_node
            node_list.append(new_node)
            if new_node.value == 0:
                zero_node = new_node
    node_list[0].head = node_list[-1]
    node_list[-1].tail = node_list[0]
    return node_list, zero_node


def get_grove_sum_node2(zero_node: Node2, list_len: int):
    curr_node = zero_node
    curr_sum = 0
    for _ in range(3):
        curr_node = get_x_element_from_node(curr_node, 1000, list_len)
        curr_sum += curr_node.actual_value
    return curr_sum
