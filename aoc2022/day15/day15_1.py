from ..helpers import read_problem, print_to_display, exception_handler
import os
import re


path_to_dir = os.path.dirname(__file__)
input_file = path_to_dir + "\\sensors.txt"
test_file = path_to_dir + "\\test_sensors.txt"


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        sensors = get_all_sensors_from_file(test_file)
        excluded_xs = set()
        y_level = 10
        for sensor in sensors:
            excluded_xs.update(sensor.get_beacon_exclusion(y_level))
        assert len(excluded_xs) == 26
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # We are going to need to do some math for this problem
    # We can't simulate a real array in this problem because the sensors and beacons are so far apart
    # The first part of the problem is just finding the number of spots that a beacon can't exist
    # in a specific Y coordinate
    # The manhattan distance is defined as the sum of the absolute values of the cartesian coordinate differences
    # We need to make a sensor class
    # The sensor class will have to calculate the manhattan distance from its beacon
    # We should also store the beacon coordinates somewhere
    # First function, extract sensors and beacons from text
    # When extracting the sensor, we have to find the manhattan distance to its beacon
    # I guess we can also store the beacon for now in the sensor object
    # After we extract this, we can find the number of spots on the specific y that it excludes from having a beacon
    # so if destination y (dest_y) manhattan distance to sensor y (sens_y) is equal to the manhattan distance,
    # there's only one spot it excludes
    # if abs(dest_y - sens_y) < manhattan distance
    # then excluded spots are
    # leftover_distance = manhattan_distance - abs(dest_y - sens_y)
    # spots = abs((sens_x - leftover_distance) - (sens_x + leftover_distance) + 1)
    # spots = abs(2 * leftover_distance + 1)  This is the case if leftover_distance >= 0
    # I just realized the above works for single sensors, but it doesn't handle overlap
    # We need to instead return a set of x's
    sensors = get_all_sensors_from_file(input_file)
    excluded_xs = set()
    y_level = 2000000
    for sensor in sensors:
        excluded_xs.update(sensor.get_beacon_exclusion(y_level))
    excluded = len(excluded_xs)
    print_to_display(f"In position 2000000, {str(excluded)} positions cannot contain the beacon", bold=True)
    print("\n\n")


class Sensor:
    def __init__(self, raw_input: str):
        self.raw_input = raw_input.strip()
        self.sens_location = None
        self.beacon_location = None
        self.man_dist = None
        self.get_locations()
        self.get_man_dist()

    def get_locations(self):
        re_x = re.compile(r"(?<=x=)-*\d+")
        re_y = re.compile(r"(?<=y=)-*\d+")
        sens_x, beacon_x = re_x.findall(self.raw_input)
        sens_y, beacon_y = re_y.findall(self.raw_input)
        self.sens_location = (int(sens_x), int(sens_y))
        self.beacon_location = (int(beacon_x), int(beacon_y))

    def get_man_dist(self):
        sens_x, sens_y = self.sens_location
        beacon_x, beacon_y = self.beacon_location
        self.man_dist = abs(sens_x - beacon_x) + abs(sens_y - beacon_y)

    def get_beacon_exclusion(self, dest_y: int):
        x_set = set()
        leftover_distance = self.man_dist - abs(self.sens_location[1] - dest_y)
        if leftover_distance < 0:
            return x_set
        x_set = set(range(self.sens_location[0] - leftover_distance, self.sens_location[0] + leftover_distance + 1))
        if self.beacon_location[1] == dest_y:
            x_set.remove(self.beacon_location[0])
        return x_set


def get_all_sensors_from_file(file_path):
    sensors = []
    with open(file_path, "r") as file:
        for line in file:
            sensors.append(Sensor(line))
    return sensors
