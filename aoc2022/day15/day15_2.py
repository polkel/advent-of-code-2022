from ..helpers import read_problem, print_to_display, exception_handler
from .day15_1 import Sensor, get_all_sensors_from_file, input_file, test_file


LOWER_BOUND = 0
UPPER_BOUND = 4000000
TEST_LOWER = 0
TEST_UPPER = 20


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        sensors = get_sensor2_list(test_file, TEST_LOWER, TEST_UPPER)
        beacon = None
        for y in range(TEST_LOWER, TEST_UPPER + 1):
            x_ranges = get_x_ranges(sensors, y)
            x_result = find_x_beacon(x_ranges, TEST_LOWER, TEST_UPPER)
            if x_result is not None:
                beacon = (x_result, y)
                break
        assert get_tuning_frequency(beacon) == 56000011
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # I think the problem is telling me that I need to find the only x and y position that can hold a beacon
    # where 0 <= x < 4000000 and 0 <= y < 4000000
    # 4000000 is included
    # I am not sure if there is math trick I can utilize to make this easier
    # The first approach I can think if is brute forcing this and scanning from y 0 -> 4000000
    # Finding the first one with a set that has a len of 3999999
    # That seems really inefficient though
    # We also need to include the sensor positions in the positions that the beacon cannot be,
    # I think with the existing function, that's already the case
    # So instead of finding the range at each y, I think we need to simplify it by just calculating
    # The bounds of the x of each sensor
    # Let's make a new method that gets the min_x and max_x of the sensor at a specific y_level
    # It should be and inclusive range on both ends
    # It should return None if nothing is in range of 0 -> 4000000
    sensors = get_sensor2_list(input_file, LOWER_BOUND, UPPER_BOUND)
    beacon = None
    for y in range(LOWER_BOUND, UPPER_BOUND + 1):
        x_ranges = get_x_ranges(sensors, y)
        x_result = find_x_beacon(x_ranges, LOWER_BOUND, UPPER_BOUND)
        if x_result is not None:
            beacon = (x_result, y)
            break
    tune_freq = get_tuning_frequency(beacon)
    print_to_display(f"The tuning frequency of the beacon is {str(tune_freq)}", bold=True)
    print("\n\n")


class Sensor2(Sensor):
    def __init__(self, raw_input, lower, upper):
        super().__init__(raw_input)
        self.lower = lower
        self.upper = upper

    def get_exclusion_range(self, dest_y: int):
        leftover_dist = self.man_dist - abs(dest_y - self.sens_location[1])
        if leftover_dist < 0:
            return
        low_x = self.sens_location[0] - leftover_dist
        high_x = self.sens_location[0] + leftover_dist
        if low_x > self.upper or high_x < self.lower:
            return
        if low_x < self.lower:
            low_x = self.lower
        if high_x > self.upper:
            high_x = self.upper
        return [low_x, high_x]


def get_x_ranges(sensor_list: list, dest_y):
    x_ranges = []  # We will sort this later by the first element
    for sensor in sensor_list:
        curr_range = sensor.get_exclusion_range(dest_y)
        if curr_range:
            x_ranges.append(curr_range)
    x_ranges.sort(key=lambda item: item[0])
    return x_ranges


def find_x_beacon(x_ranges: list, lower: int, upper: int):
    min_x, max_x = x_ranges[0]  # returns None if no beacon at the level
    if min_x != lower:
        return lower
    for i in range(1, len(x_ranges)):
        curr_min, curr_max = x_ranges[i]
        if curr_min > max_x + 1:
            return max_x + 1
        else:
            if curr_max > max_x:
                max_x = curr_max
    if max_x != upper:
        return upper


def get_tuning_frequency(coordinate: tuple):
    x, y = coordinate
    freq = x * 4000000 + y
    return freq


def get_sensor2_list(file_path, lower, upper):
    sensors = []
    with open(file_path, "r") as file:
        for line in file:
            sensors.append(Sensor2(line, lower, upper))
    return sensors
