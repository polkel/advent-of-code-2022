import os

from ..helpers import read_problem, print_to_display


rps_file = "RPS_rounds.txt"
rps_file_path = os.path.dirname(__file__) + "\\" + rps_file
opp_choices = dict()
opp_choices["A"] = "rock"
opp_choices["B"] = "paper"
opp_choices["C"] = "scissors"
my_choices = dict()
my_choices["X"] = "rock"
my_choices["Y"] = "paper"
my_choices["Z"] = "scissors"
beats = dict()
beats["rock"] = "scissors"
beats["scissors"] = "paper"
beats["paper"] = "rock"
choice_score = dict()
choice_score["rock"] = 1
choice_score["paper"] = 2
choice_score["scissors"] = 3


def display_problem():
    read_problem(__file__)


def solve_problem():
    final_score = 0
    with open(rps_file_path, "r") as file:
        for line in file:
            final_score += process_round(line.strip())
    print_to_display(f"The total score with the strategy guide would be {str(final_score)}", bold=True)
    print()


def process_round(round_input):
    opp_choice, my_choice = round_input.split(" ")
    opp = opp_choices[opp_choice]
    me = my_choices[my_choice]
    score = choice_score[me]
    result = rps_decider(opp, me)
    if result == "draw":
        score += 3
    elif result == "win":
        score += 6
    return score


def rps_decider(opp, me):
    if opp == me:
        return "draw"
    elif beats[me] == opp:
        return "win"
    else:
        return "loss"

