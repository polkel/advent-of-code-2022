from ..helpers import read_problem, print_to_display
from . import day02_1


my_choice = dict()
my_choice["X"] = "loss"
my_choice["Y"] = "draw"
my_choice["Z"] = "win"


def display_problem():
    read_problem(__file__)


def solve_problem():
    final_score = 0
    with open(day02_1.rps_file_path, "r") as file:
        for line in file:
            final_score += process_round(line.strip())
    print_to_display(f"The total score with the new strategy guide would be {str(final_score)}", bold=True)
    print()


def process_round(round_input):
    opp_choice, me_choice = round_input.split(" ")
    opp = day02_1.opp_choices[opp_choice]
    score = 0
    result = my_choice[me_choice]
    if result == "draw":
        score += 3
    elif result == "win":
        score += 6
    me = find_my_choice(opp, result)
    score += day02_1.choice_score[me]
    return score


def find_my_choice(opp, result):
    if result == "draw":
        return opp
    elif result == "loss":
        return day02_1.beats[opp]
    for me, opponent in day02_1.beats.items():
        if opp == opponent:
            return me
