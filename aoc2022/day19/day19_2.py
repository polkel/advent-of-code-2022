from ..helpers import read_problem, print_to_display, exception_handler
from .day19_1 import test_file, input_file, Inventory, Blueprint, optimal_blueprint, get_all_blueprints, InvRobotPair


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        pass
    except Exception as e:
        exception_handler(e)


def solve_problem():
    q_level_product = get_multiple_of_first_three(input_file)
    print_to_display(f"The product of the first 3 geodes is {str(q_level_product)}", bold=True)
    print("\n\n")


def get_multiple_of_first_three(file_path):
    blueprints = get_all_blueprints(file_path)
    q_product = 1
    for i in range(3):
        print(f"Blueprint {i}:\n")
        blueprint = blueprints[i]
        new_pair = InvRobotPair(Inventory(0, 0, 0, 0), Inventory(1, 0, 0, 0))
        visited = set()
        visited.add(new_pair)
        result_pair = optimal_blueprint(blueprint, 32, [new_pair], visited)
        q_product *= result_pair.inventory.geode
    return q_product
