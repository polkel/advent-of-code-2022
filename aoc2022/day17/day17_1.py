from ..helpers import read_problem, print_to_display, exception_handler
import os


path_to_dir = os.path.dirname(__file__)
pieces_file = path_to_dir + "\\pieces.txt"
input_file = path_to_dir + "\\input_moves.txt"
test_file = path_to_dir + "\\test_moves.txt"


ROCK = "#"
EMPTY = "."


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        templates = get_template_list(pieces_file)
        with open(test_file, "r") as file:
            moves = file.read()
        moves = moves.strip()
        test_grid = Grid(7, (3, 2), moves, templates)
        for _ in range(2022):
            test_grid.add_piece()
        assert test_grid.highest_point == 3068
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # Let's just simulate this with a big array
    # I am just so tired from day 16 lmao
    # We will need the input of how many pieces should be on the board
    # With that, we will know how tall our array needs to be
    # we can assume to make the array as tall as all the pieces combined * (moves + num pieces) / num pieces
    # we don't even really need an array
    # we can just make a set of coordinates of where the pieces are
    templates = get_template_list(pieces_file)
    with open(input_file, "r") as file:
        moves = file.read()
    moves = moves.strip()
    grid = Grid(7, (3, 2), moves, templates)
    for _ in range(2022):
        grid.add_piece()
    print_to_display(f"After 2022 rocks have fallen, the tower will be {str(grid.highest_point)} units tall", bold=True)
    print("\n\n")


class Grid:
    def __init__(self, width: int, piece_start: tuple, moves: str, piece_templates: list):
        # bottom left point of the grid is 0, 0; row, col
        self.width = width
        self.piece_start = piece_start
        self.pieces = set()
        self.moves_before_check = piece_start[0] + 1
        self.moves = moves  # string from moves
        self.piece_templates = piece_templates  # list of piece templates
        self.piece_counter = 0
        self.move_counter = 0
        self.piece_mod = len(piece_templates)
        self.move_mod = len(moves)
        self.highest_point = 0  # this is the unit height
        self.num_pieces = 0

    def get_insertion_point(self):
        return self.highest_point, self.piece_start[1]

    def get_move(self):
        move = self.moves[self.move_counter]
        self.move_counter = (self.move_counter + 1) % self.move_mod
        return move

    def get_piece_template(self):
        piece_template = self.piece_templates[self.piece_counter]
        self.piece_counter = (self.piece_counter + 1) % self.piece_mod
        return piece_template

    def add_piece(self):
        piece = Piece(self.get_piece_template(), self)
        while piece.move("v"):
            piece.move(self.get_move())
        self.pieces.update(piece.coordinates)
        if piece.highest + 1 > self.highest_point:
            self.highest_point = piece.highest + 1
        self.num_pieces += 1


class PieceTemplate:
    def __init__(self, piece_text: str):
        self.raw_text = piece_text
        self.piece_coordinates = set()
        self.height = 0
        self.get_piece_locations()

    def get_piece_locations(self):
        piece_lines = self.raw_text.split("\n")
        curr_row = 0
        while len(piece_lines) != 0:
            curr_line = piece_lines.pop()
            col = 0
            for letter in curr_line:
                if letter == ROCK:
                    self.piece_coordinates.add((curr_row, col))
                col += 1
            curr_row += 1
        self.height = curr_row


class Piece:
    def __init__(self, piece_template: PieceTemplate, grid: Grid):
        self.piece_template = piece_template
        self.coordinates = set()
        self.grid = grid
        self.highest = 0
        self.start_position()

    def start_position(self):
        self.coordinates = self.piece_template.piece_coordinates.copy()
        new_coords = set()
        for coord in self.coordinates:
            row, col = coord
            add_row, add_col = self.grid.get_insertion_point()
            new_coord = row + add_row, col + add_col
            new_coords.add(new_coord)
        self.coordinates = new_coords
        for _ in range(self.grid.moves_before_check):
            self.move(self.grid.get_move())

    def move(self, move_str: str):
        match move_str:
            case "<":
                add_row, add_col = (0, -1)
            case ">":
                add_row, add_col = (0, 1)
            case _:
                add_row, add_col = (-1, 0)
        new_moves = set()
        max_row = 0
        for row, col in self.coordinates:
            new_row, new_col = row + add_row, col + add_col
            if (new_row, new_col) in self.grid.pieces or new_col < 0 or new_col >= self.grid.width or new_row < 0:
                if move_str in "<>":
                    return True
                else:
                    return False
            if new_row > max_row:
                max_row = new_row
            if new_row == 0:
                hit_the_floor = True
            new_moves.add((new_row, new_col))
        self.highest = max_row
        self.coordinates = new_moves
        return True


def get_template_list(file_path: str):
    templates = []
    with open(file_path, "r") as file:
        raw_text = file.read()
    templates_raw = raw_text.split("\n\n")
    for template in templates_raw:
        templates.append(PieceTemplate(template))
    return templates
