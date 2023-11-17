from ..helpers import read_problem, print_to_display, exception_handler
from .day16_1 import Pipeline, Valve, input_file, test_file
import itertools


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_pipeline = Pipeline2(test_file, 26)
        test_pipeline.extract_valves()
        test_pipeline.bfs_adjacency()
        # for valve, adjacency in test_pipeline.adjacency.items():
        #     print(f"Adjacency matrix for {valve}")
        #     for dest_valve, value in adjacency.items():
        #         print(f"{dest_valve}: {value} ", end="")
        #     print("\n")
        start_val = test_pipeline.valves["AA"]
        test_pipeline.generate_half_sets()
        pressure_results = []
        for half_set in test_pipeline.half_sets:
            pressure_results.append(test_pipeline.dfs_max_new(start_val, 0, half_set))
        curr_max = 0
        for result, opened in pressure_results:
            for result2, opened2 in pressure_results:
                copy_opened = opened.copy()
                copy_opened.update(opened2)
                results = result + result2
                if copy_opened == test_pipeline.to_open and curr_max < results:
                    curr_max = results
        assert curr_max == 1707
        # max_pressure = test_pipeline.dfs_max_double(0, start_val, 0, start_val, 0, set())
        # assert max_pressure[0] == 1707
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # Maybe I can modify the DFS to take in two openers starting at AA?
    # This was a horrible idea but it kinda worked
    # I just split it into two
    # ran the DFS to simulate opening half the valves and then combined results
    pipeline = Pipeline2(input_file, 26)
    pipeline.extract_valves()
    pipeline.bfs_adjacency()
    # for valve, adjacency in pipeline.adjacency.items():
    #     print(f"Adjacency matrix for {valve}")
    #     for dest_valve, value in adjacency.items():
    #         print(f"{dest_valve}: {value} ", end="")
    #     print("\n")
    start_val = pipeline.valves["AA"]
    pipeline.generate_half_sets()
    pressure_results = []
    for half_set in pipeline.half_sets:
        pressure_results.append(pipeline.dfs_max_new(start_val, 0, half_set))
    curr_max = 0
    for result, opened in pressure_results:
        for result2, opened2 in pressure_results:
            results = result + result2
            if len(opened.intersection(opened2)) == 0 and curr_max < results:
                curr_max = results
    print_to_display(f"The pressure released in 26 minutes by me and the elephant is {str(curr_max)}", bold=True)
    print("\n\n")


class Pipeline2(Pipeline):
    def __init__(self, file_path, time_limit):
        super().__init__(file_path, time_limit)
        self.extract_valves()
        self.bfs_adjacency()
        self.half_sets = []

    def generate_half_sets(self):
        half_sets = []
        half_set_len = [len(self.to_open) // 2]
        if len(self.to_open) % 2 == 1:
            half_set_len.append((len(self.to_open) // 2) + 1)
        copy_to_open = self.to_open.copy()
        for half_len in half_set_len:
            combos = itertools.combinations(copy_to_open, half_len)
            for combo in combos:
                half_sets.append(set(combo))
        self.half_sets = half_sets

    def dfs_max_new(self, valve: Valve, curr_time: int, open_set: set):
        remaining_to_open = self.to_open.difference(open_set)
        pressures = [(0, set())]
        for item in remaining_to_open:
            open_time = curr_time + self.adjacency[valve.name][item.name]
            opened = set()
            opened.add(item)
            new_time = open_time + 1
            if open_time >= self.time_limit - 1:
                continue
            pressure = item.pressure_released[open_time]
            new_open = open_set.copy()
            new_open.add(item)
            if new_open == self.to_open:
                pressure_result = (0, set())
            else:
                pressure_result = self.dfs_max_new(item, new_time, new_open)
            pressure += pressure_result[0]
            opened.update(pressure_result[1])
            pressures.append((pressure, opened))
        pressures.sort(key=lambda x: x[0])
        return pressures[-1]

    def dfs_max_double(self, curr_time: int, me_val: Valve, me_time: int, el_val: Valve, el_time: int, open_set: set):
        remaining_open = self.to_open.difference(open_set)
        if me_val is None and el_val is None or curr_time >= self.time_limit:
            return 0, set()
        me_new = me_time == 0  # Checks if me or el needs to go to a new valve
        el_new = el_time == 0
        pressures = [(0, set())]
        curr_pressure_sum = 0
        opened = set()
        if me_new:
            curr_pressure_sum += me_val.pressure_released[curr_time]
            opened.add((me_val, curr_time))
        if el_new:
            curr_pressure_sum += el_val.pressure_released[curr_time]
            opened.add((el_val, curr_time))
        pressures.append((curr_pressure_sum, opened))
        for valve in remaining_open:
            el_remaining = remaining_open.copy()
            new_me_val = me_val
            new_me_time = me_time
            if me_new:
                new_me_time = self.adjacency[me_val.name][valve.name]
                if curr_time != 0:
                    new_me_time += 1
                new_me_val = valve
                el_remaining.remove(valve)
            for other_valve in el_remaining:
                new_el_time = el_time
                new_el_val = el_val
                if el_new:
                    new_el_time = self.adjacency[el_val.name][other_valve.name]
                    if curr_time != 0:
                        new_el_time += 1
                    new_el_val = other_valve
                new_open = open_set.copy()
                new_open.add(new_me_val)
                new_open.add(new_el_val)
                new_curr, new_me, new_el = self.adjust_times(curr_time, new_me_time, new_el_time)
                if new_curr < self.time_limit - 1:
                    pressure_copy = curr_pressure_sum
                    pressure_result = self.dfs_max_double(new_curr, new_me_val, new_me, new_el_val, new_el, new_open)
                    pressure_copy += pressure_result[0]
                    result_open = opened.copy()
                    result_open.update(pressure_result[1])
                    pressures.append((pressure_copy, result_open))
            else:
                new_el_val = el_val
                new_el_time = el_time
                if el_new:
                    new_el_val = None
                    new_el_time = 1000
                if len(el_remaining) == 0:
                    new_curr, new_me, new_el = self.adjust_times(curr_time, new_me_time, new_el_time)
                    pressure_copy = curr_pressure_sum
                    new_open = open_set.copy()
                    new_open.add(new_me_val)
                    if new_curr < self.time_limit - 1:
                        pressure_result = self.dfs_max_double(new_curr, new_me_val, new_me, new_el_val, new_el, new_open)
                        pressure_copy += pressure_result[0]
                        result_open = opened.copy()
                        result_open.update(pressure_result[1])
                        pressures.append((pressure_copy, result_open))
        if len(remaining_open) == 0:
            new_me_val = me_val
            new_me_time = me_time
            new_el_val = el_val
            new_el_time = el_time
            if me_new:
                new_me_val = None
                new_me_time = 1000
            if el_new:
                new_el_val = None
                new_el_time = 1000
            pressure_copy = curr_pressure_sum
            new_curr, new_me, new_el = self.adjust_times(curr_time, new_me_time, new_el_time)
            if new_curr < self.time_limit - 1:
                pressure_result = self.dfs_max_double(new_curr, new_me_val, new_me, new_el_val, new_el, open_set)
                pressure_copy += pressure_result[0]
                result_open = opened.copy()
                result_open.update(pressure_result[1])
                pressures.append((pressure_copy, result_open))
        pressures.sort(key=lambda x: x[0])
        print(pressures[-1])
        return pressures[-1]

    @staticmethod
    def adjust_times(curr_time, me_time, el_time):
        time_to_sub = me_time
        if el_time < me_time:
            time_to_sub = el_time
        return curr_time + time_to_sub, me_time - time_to_sub, el_time - time_to_sub
