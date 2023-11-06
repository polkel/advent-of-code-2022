from ..helpers import read_problem, print_to_display, exception_handler
import os


input_file = "terminal_io.txt"
path_to_dir = os.path.dirname(__file__) + "\\"
input_path = path_to_dir + input_file
test_file = "test_terminal.txt"
test_path = path_to_dir + test_file


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        test_terminal = Terminal()
        with open(test_path, "r") as file:
            for line in file:
                test_terminal.process_command(line.rstrip())
        assert test_terminal.find_sum_of_dir_size(100000) == 95437
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # This problem seems pretty involved
    # Really ramped up from day 6
    # Let's create two classes
    # One is a terminal
    # One is a directory
    # Maybe the terminal will keep a list of all directories it finds?
    # If a directory's size is updated, it will also have to update the parent directory's size
    # Let's just start and see where this goes
    # We are going to assume right now that there are no files or directories changing
    # Also going to assume that we are only using 'cd' on directories already spotted with 'ls'
    terminal = Terminal()
    with open(input_path, "r") as file:
        for line in file:
            terminal.process_command(line.rstrip())
    result = terminal.find_sum_of_dir_size(100000)
    print_to_display(f"The sum of all directories that have a size of less than 100,000 is {str(result)}", bold=True)
    print("\n\n")


class File:
    def __init__(self, name: str, size: int):  # we might not really need this
        self.name = name
        self.size = size

    def __str__(self):
        return self.name, self.size


class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.child_names = set()
        self.file_names = set()
        self.files = []
        self.size = 0

    def __str__(self):
        return f"<name = {self.name}, size = {self.size}>"

    def __repr__(self):
        return self.__str__()

    def insert_file(self, file: File):
        # There may be multiple ls calls on the same directory, this should check if the file exists and add if not
        if not self.has_file(file.name):
            self.files.append(file)
            self.file_names.add(file.name)
            self.update_size(file.size)
            return True
        return False

    def insert_directory(self, directory):
        # Check if the directory already exists and only add if it's not there
        if not self.has_dir(directory.name):
            self.child_names.add(directory.name)
            self.children.append(directory)
            return True
        return False

    def update_size(self, file_size: int):
        self.size += file_size
        if self.parent is not None:
            self.parent.update_size(file_size)

    def has_file(self, file_name):
        return file_name in self.file_names

    def has_dir(self, dir_name):
        return dir_name in self.child_names

    def find_child(self, dir_name):
        for child in self.children:
            if dir_name == child.name:
                return child


class Terminal:
    def __init__(self):
        self.curr_dir = None  # I'm not sure if we actually have to track ls
        # any time there isn't a '$' as a first argument, it should be added to the curr_dir
        self.parent_dir = None
        self.all_dirs = []

    def process_command(self, command):
        command_args = command.split()
        if command_args[0] == "$" and command_args[1] == "cd":
            self.go_to_dir(command_args[2])
        elif command_args[0] != "$":
            self.add_to_dir(command)

    def go_to_dir(self, dir_name):  # cd will only work in these three conditions
        if self.curr_dir is None:
            self.curr_dir = Directory(dir_name)
            self.parent_dir = self.curr_dir
            self.all_dirs.append(self.curr_dir)
        elif self.curr_dir.has_dir(dir_name):
            self.curr_dir = self.curr_dir.find_child(dir_name)
        elif dir_name == "..":
            self.curr_dir = self.curr_dir.parent

    def add_to_dir(self, command):
        size, name = command.split()
        if size == "dir":
            dir_to_add = Directory(name, parent=self.curr_dir)
            result = self.curr_dir.insert_directory(dir_to_add)
            if result:  # will only add dir_to_add if it inserted properly
                self.all_dirs.append(dir_to_add)
        else:
            size = int(size)
            file = File(name, size)
            self.curr_dir.insert_file(file)

    def find_sum_of_dir_size(self, size_limit: int):
        size_sum = 0
        for directory in self.all_dirs:
            if directory.size <= size_limit:
                size_sum += directory.size
        return size_sum
