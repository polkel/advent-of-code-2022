import importlib
import os


def main():
    os.system("")

    user_input = input("Which day would you like to see?\n").strip()

    if int(user_input) < 10:
        user_input = "0" + user_input
    print()
    day_module = importlib.import_module(".day" + user_input, "aoc2022")
    day_module.main()
