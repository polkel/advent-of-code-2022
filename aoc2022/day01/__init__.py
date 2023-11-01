import os
from . import day01_1, day01_2

_module_path = os.path.dirname(__file__)


def main():
    day01_1.display_problem()
    day01_1.solve_problem()
    day01_2.display_problem()
    day01_2.solve_problem()
