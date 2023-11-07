from ..helpers import read_problem, print_to_display, exception_handler
import numpy as np
import os


path_to_dir = os.path.dirname(__file__)
input_file = path_to_dir + "\\trees.txt"
test_file = path_to_dir + "\\test_trees.txt"


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_array = [[3, 0, 3, 7, 3],
                      [2, 5, 5, 1, 2],
                      [6, 5, 3, 3, 2],
                      [3, 3, 5, 4, 9],
                      [3, 5, 3, 9, 0]]
        test_np = np.array(test_array)
        result_np = trees_to_array(test_file)
        assert np.array_equal(test_np, result_np)
        assert total_visible_trees(result_np) == 21
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # We could solve this by iterating over all internal elements
    # However, I wonder if there is a more elegant solution
    # Let's not overcomplicate the problem and just solve this recursively
    # Couple of helper functions
    # input_to_array(input_file) and returns a numpy array
    # check_visibility(coordinate) returns true or false on visibility
    trees_np = trees_to_array(input_file)
    visible_trees = total_visible_trees(trees_np)
    print_to_display(f"The total number of visible trees from the outside is {str(visible_trees)}", bold=True)
    print("\n\n")


def trees_to_array(file_path):
    tree_grid = []
    with open(file_path, "r") as file:
        for line in file:
            new_row = []
            for num in line.rstrip():
                new_row.append(int(num))
            tree_grid.append(new_row)
    return np.array(tree_grid)


def check_visibility(coordinate, np_array):
    curr_val = np_array[coordinate]
    row = coordinate[0]
    col = coordinate[1]
    up_sub = np_array[:row, col]
    down_sub = np_array[row + 1:, col]
    left_sub = np_array[row, : col]
    right_sub = np_array[row, col + 1:]
    arrays_to_check = [up_sub, down_sub, left_sub, right_sub]
    for array in arrays_to_check:
        check_result = np.where(array >= curr_val)
        taller_trees = len(check_result[0])  # this returns how many taller trees there are in each direction
        if taller_trees == 0:
            return True
    return False


def total_visible_trees(np_array):
    visible_trees = 0
    total_rows = len(np_array)
    total_cols = len(np_array[0])
    for i in range(total_rows):
        for j in range(total_cols):
            coordinate = (i, j)
            if check_visibility(coordinate, np_array):
                visible_trees += 1
    return visible_trees
