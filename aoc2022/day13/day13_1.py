from ..helpers import read_problem, print_to_display, exception_handler
import os


path_to_dir = os.path.dirname(__file__)
input_file = path_to_dir + "\\packets.txt"
test_file = path_to_dir + "\\test_packets.txt"


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_1 = create_list("[1,1,3,1,1]")
        assert test_1 == [1, 1, 3, 1, 1]
        test_2 = create_list("[[1],[2,3,4]]")
        assert test_2 == [[1], [2, 3, 4]]
        test_3 = create_list("[]")
        assert test_3 == []
        test_4 = create_list("[[[]]]")
        assert test_4 == [[[]]]
        test_5 = create_list("[1,[2,[3,[4,[5,6,0]]]],8,9]")
        assert test_5 == [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
        assert compare_lists([], []) == "continue"
        assert compare_lists([[]], []) == "disorder"
        test_array1 = [1, 1, 3, 1, 1]
        test_array2 = [1, 1, 5, 0, 1]
        assert compare_lists(test_array1, test_array2) == "order"
        assert compare_lists(test_array2, test_array1) == "disorder"
        assert sum_ordered_index(test_file) == 13
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # Really complicated logic
    # But if we break it down to recursive functions, it should be easy
    # This is insane
    # Let's first make a function to convert a line to an element
    # Then we did the comparison recursively with the logic given to us
    # I spent a few minutes wrapping my head around the logic
    # Once I figured out the base cases, implementation was trivial
    sum_ordered = sum_ordered_index(input_file)
    print_to_display(f"The sum of the indices of ordered packet pairs is {str(sum_ordered)}", bold=True)
    print("\n\n")


def create_list(list_str: str):  # No validation for any list string with types other than ints
    parse_str = list_str[1: -1]  # Take away outer brackets
    str_len = len(parse_str)
    cursor = 0
    result = []
    element_begin = None
    sub_list_traversal = False
    left_brackets = 0
    right_brackets = 0
    while cursor != str_len:
        char = parse_str[cursor]
        if element_begin is None:
            element_begin = cursor
            if char == "[":
                sub_list_traversal = True
        if char == ",":
            if sub_list_traversal and left_brackets == right_brackets:
                result.append(create_list(parse_str[element_begin: cursor]))
                sub_list_traversal = False
                element_begin = None
            elif not sub_list_traversal:
                result.append(int(parse_str[element_begin: cursor]))
                element_begin = None
        elif char == "]":
            right_brackets += 1
        elif char == "[":
            left_brackets += 1
        cursor += 1
    if sub_list_traversal:
        result.append(create_list(parse_str[element_begin:]))
    elif element_begin is not None:  # we can't do int on an empty string
        result.append(int(parse_str[element_begin:]))
    return result


def compare_lists(list1, list2):
    # We need to compare the lists element by element
    # I am going to assume that if the lists are the same, they are in order
    # It will always have to be in order or out of order
    # We need to break, the first moment that we find a difference
    # If we are doing this recursively, we will have to find some base cases
    # Base case 1, two integers being compared of different values
    # Base case 2, one list runs out of items before the other
    # Base case 3, both lists are out of items, we can say it is in order
    # Recursion case, if both upcoming elements are of different types or are both lists
    element_num = 0
    list1_len = len(list1)
    list2_len = len(list2)
    while element_num < list1_len and element_num < list2_len:
        item1 = list1[element_num]
        item2 = list2[element_num]
        int_1 = isinstance(item1, int)
        int_2 = isinstance(item2, int)
        if int_1 and int_2:
            if item1 == item2:
                element_num += 1
                continue
            elif item1 > item2:  # Base case 1
                return "disorder"
            else:
                return "order"
        else:  # recursion case, two diff elements
            if int_1:
                temp_list = [item1]
                item1 = temp_list
            if int_2:
                temp_list = [item2]
                item2 = temp_list
            recursion_result = compare_lists(item1, item2)
            if recursion_result == "continue":
                element_num += 1
            else:
                return recursion_result
    if list1_len < list2_len:  # Base cases 2 and 3
        return "order"
    elif list1_len == list2_len:
        return "continue"
    else:
        return "disorder"


def sum_ordered_index(file_path):
    with open(file_path, "r") as file:
        text = file.read()
    pairs = text.split("\n\n")
    sum_ordered = 0
    for ind, pair in enumerate(pairs):
        text1, text2 = pair.split("\n")
        list1 = create_list(text1)
        list2 = create_list(text2)
        if compare_lists(list1, list2) == "order":
            sum_ordered += ind + 1
    return sum_ordered
