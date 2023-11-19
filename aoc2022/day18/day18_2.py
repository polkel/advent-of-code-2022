from ..helpers import read_problem, print_to_display, exception_handler
from .day18_1 import get_sides, droplet_coordinate, test_file, input_file


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        assert get_exterior_surface_area(test_file) == 58
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # I am not sure if BFS or DFS is better for finding if an open side is in contact with the exterior
    # I do know that we can do this if we just
    # I think DFS because it will go further out first
    # How do I keep track of pockets that are inside or outside?
    # With sets perhaps?
    # When we find all the droplets, we need to find the max x, y, z and the min x, y, z
    # This will tell us when to break the DFS
    # Then we create a DFS recursion. If the node was already visited during the DFS, we should not recur again
    # I think this has been one of the issues in my other DFS algos
    # After, we track all the coordinates traverse by the DFS, and depending on the result we either store it in
    # a pocket_set or exterior_set
    # So that we can check all future nodes with these
    # DFS base cases
    # find a node that is in pocket_set, open_set, or droplets
    # find a node where x, y, or z is greater or less than max or min x, y, z (means its open)
    surface_area_exterior = get_exterior_surface_area(input_file)
    print_to_display(f"The surface area that touches the water is {str(surface_area_exterior)}", bold=True)
    print("\n\n")


def get_exterior_surface_area(file_path):
    droplets = set()
    with open(file_path, "r") as file:
        max_x, max_y, max_z = 0, 0, 0  # initialize low and high numbers for min maxes
        min_x, min_y, min_z = 1000, 1000, 1000
        for line in file:
            curr_droplet = droplet_coordinate(line)
            x, y, z = curr_droplet
            droplets.add(curr_droplet)
            max_x = x if x > max_x else max_x
            max_y = y if y > max_y else max_y
            max_z = z if z > max_z else max_z
            min_x = x if x < min_x else min_x
            min_y = y if y < min_y else min_y
            min_z = z if z < min_z else min_z
    min_coord = (min_x, min_y, min_z)
    max_coord = (max_x, max_y, max_z)
    pockets = set()
    outsides = set()
    exterior_sides = 0
    for droplet in droplets:
        all_sides = get_sides(droplet)
        for side in all_sides:
            visited = set()
            if is_exterior(side, droplets, pockets, outsides, max_coord, min_coord, visited):
                outsides.update(visited)
                exterior_sides += 1
            else:
                pockets.update(visited)
    return exterior_sides


def is_exterior(coord: tuple, droplets: set, pockets: set, exts: set, max_coord: tuple, min_coord: tuple, visited: set):
    # We will do a DFS?
    # Let's do the base cases
    # The only modified set is the visited
    if coord in droplets or coord in pockets:
        if coord in visited:
            visited.remove(coord)  # We don't want to record it if it's been recorded
        return False
    x, y, z = coord
    min_x, min_y, min_z = min_coord
    max_x, max_y, max_z = max_coord
    outside_coord = x < min_x or x > max_x or y < min_y or y > max_y or z < min_z or z > max_z
    if coord in exts or outside_coord:
        return True
    all_sides = get_sides(coord)
    exterior = False
    for side in all_sides:
        if side not in visited:
            visited.add(side)
            exterior = exterior or is_exterior(side, droplets, pockets, exts, max_coord, min_coord, visited)
    return exterior
