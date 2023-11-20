from ..helpers import read_problem, print_to_display, exception_handler
import os
import re


resources_priority = ["geode", "obsidian", "clay", "ore"]
path_to_dir = os.path.dirname(__file__)
test_file = path_to_dir + "\\test_prints.txt"
input_file = path_to_dir + "\\prints.txt"


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        blueprints = get_all_blueprints(test_file)
        q_level_sum = get_quality_level_sum(blueprints, 24)
        assert q_level_sum == 33
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # This seems ridiculous
    # I think the winning combo is that at the start of every minute
    # We check what the best robot we can make is and make that
    # ore < clay < obsidian < geodes
    # Thankfully every robot is made with the same two ingredients, just varying quantities
    # This would be more complicated (and I'm sure this is what part two will encompass) if we can make more than one
    # robot per minute
    # If we can make more than one robot per minute, I don't know if we can assume this same combination will work
    # The process flow per minute is:
    # Minute start
    # See if you have enough resources in inventory to build a robot, queue for robot build
    # add resource robots mined resources to inventory
    # add newly built robot to robot inventory
    # end minute
    # We need to fix the algorithm
    # The algo will hold out on building a robot IF
    # The more expensive resource of the next robot is met
    # So new minute algo:
    # MINUTE START
    # from order of robot priority:
    # has it now: queue for creation, will have it next cycle: do not make a new robot
    # Okay, there is no algo for finding the optimal way to make robots...
    # We have to BFS this I think
    # Branching every time there is a decision to make a robot or not
    # I am now sad
    # TODO get rid of the false assumptions, max geode number is typically not indicative
    # TODO get a do not build list based on max resource required for building, have it persist?
    # TODO always check if you can build a geode bot first in every depth and just have it build it if you can
    blueprints = get_all_blueprints(input_file)
    q_level = get_quality_level_sum(blueprints, 24)
    print_to_display(f"The resulting sum of quality levels is {str(q_level)}", bold=True)
    print("\n\n")


class Inventory:
    def __init__(self, ore: int, clay: int, obsidian: int, geode: int):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode

    def add_item(self, item_type: str, quantity: int):
        setattr(self, item_type, getattr(self, item_type) + quantity)

    def add_inventory(self, other):
        self.ore += other.ore
        self.clay += other.clay
        self.obsidian += other.obsidian
        self.geode += other.geode

    def sub_inventory(self, other):
        self.ore -= other.ore
        self.clay -= other.clay
        self.obsidian -= other.obsidian
        self.geode -= other.geode

    def in_inventory(self, other):  # compares two inventories together, returns false if self is insufficient
        for resource in resources_priority:
            if getattr(other, resource) > getattr(self, resource):
                return False
        return True

    def __str__(self):
        inv_string = f"Ore: {self.ore}, Clay: {self.clay}, Obsidian: {self.obsidian}, Geode: {self.geode}"
        return inv_string

    def __repr__(self):
        return self.__str__()

    def make_copy(self):
        return Inventory(self.ore, self.clay, self.obsidian, self.geode)

    def __eq__(self, other):
        equality = self.ore == other.ore
        equality = equality and self.clay == other.clay
        equality = equality and self.obsidian == other.obsidian
        equality = equality and self.geode == other.geode
        return equality

    def __ne__(self, other):
        ne = self.ore != other.ore
        ne = ne or self.clay != other.clay
        ne = ne or self.obsidian != other.obsidian
        ne = ne or self.geode != other.geode
        return ne

    def __hash__(self):
        object_id = f"ore{self.ore}"
        object_id += f"clay{self.clay}"
        object_id += f"obsidian{self.obsidian}"
        object_id += f"geode{self.geode}"
        return hash(object_id)


class Blueprint:
    def __init__(self, raw_text: str):
        self.ore_robot = None
        self.clay_robot = None
        self.obsidian_robot = None
        self.geode_robot = None
        self.raw_text = raw_text.strip()
        self.robot_re = re.compile(r"(?<=Each ).+(?= costs)")
        self.ingredients_re = re.compile(r"(?<=costs ).+")
        self.robot_limit = None
        self.get_recipes()
        self.get_robot_limit()

    def get_recipes(self):
        robots = self.raw_text.split(". ")
        for robot in robots:
            robot_type = self.robot_re.search(robot).group()
            robot_type = robot_type.replace(" ", "_")
            ingredients = self.ingredients_re.search(robot).group()
            ingredients = ingredients.strip(".")
            ingredient_list = ingredients.split(" and ")
            curr_req = Inventory(0, 0, 0, 0)
            for ingredient in ingredient_list:
                num, resource = ingredient.split()
                curr_req.add_item(resource, int(num))
            setattr(self, robot_type, curr_req)

    def get_robot_limit(self):
        maxes = Inventory(0, 0, 0, 0)
        all_recipes = [
            self.ore_robot,
            self.clay_robot,
            self.obsidian_robot,
            self.geode_robot]
        for recipe in all_recipes:
            for resource in resources_priority:
                if getattr(maxes, resource) < getattr(recipe, resource):
                    setattr(maxes, resource, getattr(recipe, resource))
        self.robot_limit = maxes

    def __str__(self):
        blueprint_str = "Blueprint Recipes\n"
        blueprint_str += f"An ore robot costs - {self.ore_robot}\n"
        blueprint_str += f"A clay robot costs - {self.clay_robot}\n"
        blueprint_str += f"An obsidian robot costs - {self.obsidian_robot}\n"
        blueprint_str += f"A geode robot costs - {self.geode_robot}\n"
        return blueprint_str

    def __repr__(self):
        return self.__str__()


def get_all_blueprints(file_name):
    all_prints = []
    with open(file_name, "r") as file:
        for line in file:
            all_prints.append(Blueprint(line))
    return all_prints


def get_inventory_for_blueprint(blueprint: Blueprint, minutes: int):
    robots = Inventory(1, 0, 0, 0)
    inventory = Inventory(0, 0, 0, 0)
    for minute in range(minutes):
        add_robot = get_robot_to_build(blueprint, inventory, robots)
        inventory.add_inventory(robots)
        if add_robot:
            inventory.sub_inventory(getattr(blueprint, add_robot + "_robot"))
            robots.add_item(add_robot, 1)
        print(f"Minute {minute + 1}:\nInventory\n{inventory}\n", f"Robots\n{robots}\n")
    return inventory


def get_robot_to_build(blueprint: Blueprint, inventory: Inventory, robots: Inventory):
    add_robot = None
    next_inventory = inventory.make_copy()
    next_inventory.add_inventory(robots)
    for resource in resources_priority:
        robot_name = resource + "_robot"
        robot_cost = getattr(blueprint, robot_name).make_copy()
        if inventory.in_inventory(robot_cost):
            add_robot = resource
            break
        robot_cost.ore = 0
        if next_inventory.in_inventory(robot_cost):
            break
    return add_robot


def optimal_blueprint(blueprint: Blueprint, minutes: int, depth_list: list, visited: set):
    print(f"Minute: {minutes}")
    print(f"Depth length: {len(depth_list)}")
    if minutes == 0:
        pair_index = return_most_geodes_index(depth_list)
        return depth_list[pair_index]
    new_depth = []
    for pair in depth_list:
        inventory, robots = pair.inventory, pair.robots
        build_list = get_all_robots_to_make(blueprint, inventory, robots)
        next_inventory = inventory.make_copy()
        next_inventory.add_inventory(robots)
        if build_list == ["geode"]:
            inventory_copy = next_inventory.make_copy()
            robot_copy = robots.make_copy()
            inventory_copy.sub_inventory(blueprint.geode_robot)
            robot_copy.add_item("geode", 1)
            new_pair = InvRobotPair(inventory_copy, robot_copy)
            if new_pair not in visited:
                visited.add(new_pair)
                new_depth.append(new_pair)
            continue
        new_pair = InvRobotPair(next_inventory, robots)
        if new_pair not in visited:
            visited.add(new_pair)
            new_depth.append(InvRobotPair(next_inventory, robots))
        else:
            continue
        for build in build_list:
            inventory_copy = next_inventory.make_copy()
            robot_copy = robots.make_copy()
            inventory_copy.sub_inventory(getattr(blueprint, build + "_robot"))
            robot_copy.add_item(build, 1)
            new_pair = InvRobotPair(inventory_copy, robot_copy)
            if new_pair not in visited:
                visited.add(new_pair)
                new_depth.append(new_pair)
    return optimal_blueprint(blueprint, minutes - 1, new_depth, visited)


def get_optimal_inv_blueprint(blueprint: Blueprint, minutes: int, depth_list: list, visited: set):
    # depth_list is a list of lists
    # each list within is a pair of inventory and number of robots for that given minute
    # Let's create a check to see if a branch already exists and then continue
    # Depth list is now a list of InvRobotPair
    print(f"Minute: {minutes}")
    print(f"Depth length: {len(depth_list)}")
    if minutes == 0:
        pair_index = return_most_geodes_index(depth_list)
        return depth_list[pair_index]
    new_depth = []  # Need to change this to a set
    for pair in depth_list:  # already changed this for pair
        inventory, robots = pair.inventory, pair.robots
        next_inventory = inventory.make_copy()
        next_inventory.add_inventory(robots)
        next_pair = InvRobotPair(next_inventory, robots)
        if next_pair in visited:
            continue
        if next_inventory.geode > max_geodes:
            max_geodes = next_inventory.geode
        elif next_inventory.geode < max_geodes:
            continue
        new_depth.append(next_pair)
        visited.add(next_pair)
        robots_to_make = get_all_robots_to_make(blueprint, inventory)
        for robot in robots_to_make:
            next_inventory_copy = next_inventory.make_copy()
            next_inventory_copy.sub_inventory(getattr(blueprint, robot + "_robot"))
            robots_copy = robots.make_copy()
            robots_copy.add_item(robot, 1)
            new_pair = InvRobotPair(next_inventory_copy, robots_copy)
            if new_pair in visited:
                continue
            new_depth.append(new_pair)
            visited.add(new_pair)
    # Take out pairs in new_depth that don't have max_geodes
    for i in range(len(new_depth) - 1, -1, -1):  # This is the forbidden jutsu iteration
        inventory, robots = new_depth[i].inventory, new_depth[i].robots
        if inventory.geode < max_geodes:
            del new_depth[i]
    return get_optimal_inv_blueprint(blueprint, minutes - 1, new_depth, visited)


def get_all_robots_to_make(blueprint: Blueprint, inventory: Inventory, robots: Inventory):
    # Returns list of all possible robots that can be made from inventory
    robots_to_make = []
    robo_limit = blueprint.robot_limit
    for resource in resources_priority:
        if getattr(robo_limit, resource) <= getattr(robots, resource) and resource != "geode":
            continue
        if inventory.in_inventory(getattr(blueprint, resource + "_robot")):
            robots_to_make.append(resource)
            if resource == "geode":
                break
    return robots_to_make


def return_most_geodes_index(pair_list: list):
    most_geodes = 0
    most_geodes_index = 0
    for i in range(len(pair_list)):
        inventory, robots = pair_list[i].inventory, pair_list[i].robots
        if inventory.geode > most_geodes:
            most_geodes = inventory.geode
            most_geodes_index = i
    return most_geodes_index


class InvRobotPair:
    def __init__(self, inventory: Inventory, robots: Inventory):
        self.inventory = inventory
        self.robots = robots

    def __hash__(self):
        object_id = f"ore{self.inventory.ore}ore{self.robots.ore}"
        object_id += f"clay{self.inventory.clay}clay{self.robots.clay}"
        object_id += f"obsidian{self.inventory.obsidian}obsidian{self.robots.obsidian}"
        object_id += f"geode{self.inventory.geode}geode{self.robots.geode}"
        return hash(object_id)

    def __eq__(self, other):
        return self.inventory == other.inventory and self.robots == other.robots

    def __ne__(self, other):
        return self.inventory != other.inventory or self.robots != other.robots


def get_quality_level_sum(blueprint_list: list, time_limit: int):
    q_level = 0
    for i in range(len(blueprint_list)):
        print(f"Blueprint {i + 1}")
        blueprint = blueprint_list[i]
        visited = set()
        first_pair = InvRobotPair(Inventory(0, 0, 0, 0), Inventory(1, 0, 0, 0))
        visited.add(first_pair)
        result_pair = optimal_blueprint(blueprint, time_limit, [first_pair], visited)
        q_level += result_pair.inventory.geode * (i + 1)
    return q_level
