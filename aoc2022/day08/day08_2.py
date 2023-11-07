from ..helpers import read_problem, print_to_display, exception_handler
from . import day08_1


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_np = day08_1.trees_to_array(day08_1.test_file)
        assert find_scene_score((1, 2), test_np) == 4
        assert find_scene_score((3, 2), test_np) == 8
        assert highest_scene_score(test_np) == 8
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # I am not sure if trees are visible if as you are viewing it, there is a shorter tree before the limit
    # so for example, if I am at tree 6, and my viewing line is 5, 4, 5, 6
    # I am able to see the first 5, but do I see the 4 or the second 5?
    # I am going to assume yes in this first pass, but if I am wrong, then I'll have to implement the other way
    # It's never going to be anything along the edge because that will always evaluate to 0
    # We can start iterating in the inner elements of the array
    trees_np = day08_1.trees_to_array(day08_1.input_file)
    highest_scene = highest_scene_score(trees_np)
    print_to_display(f"The highest scenic score possible is {str(highest_scene)}", bold=True)
    print("\n\n")


def find_scene_score_factor(tree_val, np_sub_array):
    curr_fac = 0
    for next_tree in np_sub_array:
        curr_fac += 1
        if tree_val <= next_tree:
            break
    return curr_fac


def find_scene_score(coordinate, np_array):
    curr_val = np_array[coordinate]
    row = coordinate[0]
    col = coordinate[1]
    up_sub = day08_1.np.flip(np_array[: row, col])
    down_sub = np_array[row + 1:, col]
    left_sub = day08_1.np.flip(np_array[row, : col])
    right_sub = np_array[row, col + 1:]
    all_subs = [up_sub, down_sub, left_sub, right_sub]
    scene_fac = 1
    for sub_array in all_subs:
        scene_fac = scene_fac * find_scene_score_factor(curr_val, sub_array)
    return scene_fac


def highest_scene_score(np_array):
    rows = len(np_array)
    cols = len(np_array[0])
    high_score = 0
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            coordinate = (i, j)
            scene_score = find_scene_score(coordinate, np_array)
            if scene_score > high_score:
                high_score = scene_score
    return high_score
