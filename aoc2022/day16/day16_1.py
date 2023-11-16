from ..helpers import read_problem, print_to_display, exception_handler
import os
import re


path_to_dir = os.path.dirname(__file__)
input_file = path_to_dir + "\\tunnels.txt"
test_file = path_to_dir + "\\test_tunnels.txt"


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_pipeline = Pipeline(test_file, 30)
        test_pipeline.extract_valves()
        for valve in test_pipeline.valves.values():
            print(f"{valve} has neighbors {valve.neighbors.values()}\nand a flow rate of {valve.flow_rate}")
            if valve.flow_rate != 0:
                print(f"The release array is {valve.pressure_released}")
            print()
        print(f"The max number of valves to open is {test_pipeline.to_open}")
        print(f"The number of total valves in the pipeline is {len(test_pipeline.all_valves_set)}")
        start_valve = test_pipeline.valves["AA"]
        max_pressure = test_pipeline.dfs_max_pressure(start_valve, 0, set(), set(), [])
        print(max_pressure)
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # This is a graph traversal problem
    # This is some sort of twisted DFS algorithm
    # It's a directed weighted graph where the weights change depending on the time and if the node has been previously
    # visited
    # Unfortunately, we during the DFS, we must be able to traverse backwards in case there are rooms that are dead ends
    # I want to be able to stop the DFS if the traversal goes through rooms A -> B -> A -> B
    # As soon as the last 4 paths are the same we should break out of it to save on run time
    # We should make a Valve class that will store its flow rate and connections to other valves
    # We can compare the __eq__ and __ne__ to the name of the valve
    # Because the weight of the edge will always be a function of time, the directed edge (total pressure released)
    # towards a valve can be calculated using its flow rate
    # However, if it's been visited already, it should return 0 to the total pressure released
    # We'll have a Valve and a Pipeline class that will store all valves
    # The Pipeline class will also handle the DFS algo and admin info (like seconds to traverse, starting node, etc)
    # Do we need to consider the possibility of going through a valve without opening it?
    # Let's just assume for now that it's always best to open an unopened valve as you pass through it
    # We can refactor later if that is not the case...
    # What do we need to track for the DFS?
    # Open valves(this needs to be copied in recursion), time limit, and curr_time
    # Needs to evaluate results for passing to every neighboring valve or opening current valve
    # Can only open current valve if valve flow rate > 0 and its not in the open valves set
    pass


class Valve:
    def __init__(self, name: str, flow_rate: int, neighbors: list):
        self.name = name
        self.flow_rate = flow_rate
        self.pressure_released = None
        self.neighbors = dict()
        self.add_neighbors(neighbors)

    def add_neighbors(self, neighbors):
        # Might not be the most efficient way to add a connection to each other
        # I can add a more robust neighbor addition later
        for neighbor in neighbors:
            try:
                self.neighbors[neighbor.name]
            except KeyError:
                self.neighbors[neighbor.name] = neighbor
                neighbor.add_neighbors([self])

    def __str__(self):
        return "Valve " + self.name

    def __repr__(self):
        return "Valve " + self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def create_release_array(self, time_limit: int):
        pressure_release = []
        for i in range(time_limit, 0, -1):
            pressure_release.append((i - 1) * self.flow_rate)
        self.pressure_released = pressure_release


class Pipeline:
    def __init__(self, file_path, time_limit):
        self.file_path = file_path
        self.time_limit = time_limit
        self.valves = dict()
        self.valve_name_re = re.compile(r"(?<=Valve )[A-Z]{2}")
        self.flow_re = re.compile(r"(?<=rate=)\d+")
        self.to_open = 0
        self.all_valves_set = None
        # I edited a few lines in the input to make this work
        # Some of the singular connections just say valve, the lookbehind cannot be of variable size
        self.neighbors_re = re.compile(r"(?<=valves ).+$")

    def extract_valves(self):
        with open(self.file_path, "r") as file:
            for line in file:
                line_strip = line.strip()
                valve_match = self.valve_name_re.search(line_strip)
                flow_match = self.flow_re.search(line_strip)
                neighbors_match = self.neighbors_re.search(line_strip)
                valve_name = valve_match.group()
                flow_rate = flow_match.group()
                neighbor_list = neighbors_match.group().split(", ")
                neighbors = []  # handles creating the neighbor valves if not existing
                for neighbor_text in neighbor_list:
                    if neighbor_text in self.valves:
                        neighbors.append(self.valves[neighbor_text])
                    else:
                        new_valve = Valve(neighbor_text, 0, [])
                        neighbors.append(new_valve)
                        self.valves[neighbor_text] = new_valve
                if valve_name in self.valves:
                    curr_valve = self.valves[valve_name]
                    curr_valve.flow_rate = int(flow_rate)
                    curr_valve.add_neighbors(neighbors)
                else:
                    curr_valve = Valve(valve_name, int(flow_rate), neighbors)
                    self.valves[valve_name] = curr_valve
                curr_valve.create_release_array(self.time_limit)
                if int(flow_rate) > 0:
                    self.to_open += 1
        self.all_valves_set = set(self.valves.values())

    def dfs_max_pressure(self, valve: Valve, curr_time: int, open_set: set, visited: set, path: list):
        # Add a visited set
        # Influence path to go to non-visited unless it has all been visited
        # break if everything has been visited
        # TODO Floyd-Warshal implementation... only visit unopened valves and stop when all valves are open or timeout
        new_path = path[:]
        new_path.append(valve.name)
        repeat_path = False
        if len(new_path) >= 4:
            repeat_path = new_path[-4: -2] == new_path[-2:]
        if curr_time == self.time_limit - 1 or visited == self.all_valves_set or repeat_path:
            if valve not in open_set:
                return valve.pressure_released[curr_time]
            else:
                return 0
        new_visited = visited.copy()
        new_visited.add(valve)
        next_time = curr_time + 1
        pressures = []
        if valve.flow_rate != 0 and valve not in open_set:
            copy_open = open_set.copy()
            copy_open.add(valve)
            next_pressure = self.dfs_max_pressure(valve, next_time, copy_open, new_visited, new_path)
            next_pressure += valve.pressure_released[curr_time]
            pressures.append(next_pressure)
        not_visited = []
        for neighbor in valve.neighbors.values():
            if neighbor not in visited:
                not_visited.append(neighbor)
        to_traverse = not_visited
        if len(not_visited) == 0:
            to_traverse = valve.neighbors.values()
        for neighbor in to_traverse:
            pressures.append(self.dfs_max_pressure(neighbor, next_time, open_set, new_visited, new_path))
        max_pressure = max(pressures)
        # if curr_time % 10 == 0:
        if new_path == ["AA", "DD", "DD", "CC", "BB", "BB", "AA", "II", "JJ", "JJ", "II", "AA", "DD", "EE", "FF", "GG", "HH", "HH", "GG", "FF", "EE", "EE", "DD", "CC", "CC"]:
            print(curr_time, open_set)
            print(max_pressure)
        return max_pressure
