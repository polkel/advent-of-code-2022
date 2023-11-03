import importlib
import os
from .helpers import create_new_day


def main():
    os.system("")

    welcome_message = """\n\nWelcome to my advent of code 2022 library. Please choose a menu item:
    
    1. View problem and solution for a given day
    2. Create a directory for a new day
    3. Exit\n\n"""

    menu_options = [view_day, create_day, exit_aoc]

    try:
        user_input = int(input(welcome_message))
        print("\n\n")
        menu_item = menu_options[user_input - 1]

    except (ValueError, IndexError):
        print("Please enter a valid menu item \n\n")
        main()

    else:
        menu_item()


def view_day():
    user_input = input("Which day would you like to see?\n\n").strip()
    print("\n\n")

    try:
        if int(user_input) < 10:
            user_input = "0" + user_input
        day_module = importlib.import_module(".day" + user_input, "aoc2022")
    except ModuleNotFoundError:
        print("That day does not exist. Going back to the main menu.\n")
    else:
        day_module.main()
    finally:
        main()


def create_day():
    try:
        user_input = int(input("Which day would you like to create?\n\n"))
        print("\n\n")
        if user_input < 1 or user_input > 31:
            raise ValueError
    except ValueError:
        print("Please enter a valid day\n")
    else:
        create_new_day(user_input)
    finally:
        main()


def exit_aoc():
    print("Goodbye!")
