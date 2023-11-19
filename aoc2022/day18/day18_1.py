from ..helpers import read_problem, print_to_display, exception_handler
import os


path_to_dir = os.path.dirname(__file__)
input_file = path_to_dir + "\\droplets.txt"
test_file = path_to_dir + "\\test_droplets.txt"


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        assert get_surface_area(test_file)
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # This seems really easy. We can process this in linear time based on scans
    # We initialize two sets. open_sides and droplets
    # For every droplet, we add the droplet coordinate to droplets
    # And remove it from open_sides if it's in open_sides
    # Then, we create all the open_side coordinates of the droplet and check if it's in droplets
    # If it's in droplets, then we don't add it to open_side
    # Can't do it in the way above, because each droplet can have a cube face in the open_side coordinate
    # We have to iterate twice through the list
    surface_area = get_surface_area(input_file)
    print_to_display(f"The total surface area is {str(surface_area)}", bold=True)
    print("\n\n")


def droplet_coordinate(raw_text: str):
    x, y, z = raw_text.strip().split(",")
    return int(x), int(y), int(z)


def get_sides(droplet_coord: tuple):  # We can do single iteration if we check it with the droplet set here too
    x, y, z = droplet_coord
    directions = [(0, 0, 1),
                  (0, 0, -1),
                  (0, 1, 0),
                  (0, -1, 0),
                  (1, 0, 0),
                  (-1, 0, 0)]
    all_sides = []
    for add_x, add_y, add_z in directions:
        new_x, new_y, new_z = x + add_x, y + add_y, z + add_z
        all_sides.append((new_x, new_y, new_z))
    return all_sides


def get_surface_area(file_path):
    droplets = set()
    with open(file_path, "r") as file:
        for line in file:
            droplet_coord = droplet_coordinate(line)
            droplets.add(droplet_coord)
    open_sides = 0
    for droplet in droplets:
        all_sides = get_sides(droplet)
        for side in all_sides:
            if side not in droplets:
                open_sides += 1
    return open_sides
