from ..helpers import read_problem, print_to_display, exception_handler
from .day17_1 import pieces_file, test_file, input_file, Piece, PieceTemplate, Grid, get_template_list


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        target_pieces = 1000000000000
        templates = get_template_list(pieces_file)
        with open(test_file, "r") as file:
            moves = file.read()
        moves = moves.strip()
        precycle_pieces, precycle_height, cyc_pieces, cyc_height = get_cycle_repeat(7, (3, 2), moves, templates)
        cycles_in_target = (target_pieces - precycle_pieces) // cyc_pieces
        leftover_in_target = (target_pieces - precycle_pieces) % cyc_pieces
        test_grid = Grid(7, (3, 2), moves, templates)
        for _ in range(precycle_pieces + leftover_in_target):
            test_grid.add_piece()
        final_height = test_grid.highest_point + cycles_in_target * cyc_height
        assert final_height == 1514285714288
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # This is what I was trying to think of in part 1
    # After the moves and the number of pieces line up, it's going to add the same height
    # First let's figure out how many pieces are added when the first move lines up with the first piece addition
    # That should be when Grid.piece_counter == 0 and Grid.move_counter == 0 in between adding pieces
    # Okay, so the same concept above, but for all pieces and all moves in the move counter
    # 0, 0 never lines up, but the cycle does line up in a different piece and a different move
    # So I need to find that first and then we can do a calculation without simulating the whole thing
    target = 1000000000000
    templates = get_template_list(pieces_file)
    with open(input_file, "r") as file:
        moves = file.read()
    moves = moves.strip()
    pre_pieces, pre_height, cyc_pieces, cyc_height = get_cycle_repeat(7, (3, 2), moves, templates)
    cyc_in_target = (target - pre_pieces) // cyc_pieces
    leftover_target = (target - pre_pieces) % cyc_pieces
    grid = Grid(7, (3, 2), moves, templates)
    for _ in range(pre_pieces + leftover_target):
        grid.add_piece()
    final_height = grid.highest_point + cyc_height * cyc_in_target
    print_to_display(f"The height of the tower after a trillion rocks have fallen is {str(final_height)}", bold=True)
    print("\n\n")


def get_cycle_repeat(width, start_position, moves, templates):
    # Returns number of pieces before first cycle
    # Height before first cycle
    # Number of pieces in a cycle
    # Height of a cycle
    grid = Grid(width, start_position, moves, templates)
    combos = set()
    while (grid.piece_counter, grid.move_counter) not in combos:
        combos.add((grid.piece_counter, grid.move_counter))
        grid.add_piece()
    combo = (grid.piece_counter, grid.move_counter)
    precycle_height = grid.highest_point
    precycle_pieces = grid.num_pieces
    grid.add_piece()
    while combo != (grid.piece_counter, grid.move_counter):
        grid.add_piece()
    cycle_height = grid.highest_point - precycle_height
    cycle_pieces = grid.num_pieces - precycle_pieces
    return precycle_pieces, precycle_height, cycle_pieces, cycle_height
