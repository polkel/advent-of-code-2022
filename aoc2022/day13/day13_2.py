from ..helpers import read_problem, print_to_display, exception_handler
from .day13_1 import test_file, input_file, create_list, compare_lists


def display_problem():
    read_problem(__file__)


def test_problem():
    try:
        packet_list = get_packet_list(test_file)
        start_div = [[2]]
        end_div = [[6]]
        assert find_packet_insertion(start_div, packet_list) == 10
        assert find_packet_insertion(end_div, packet_list) + 1 == 14
    except Exception as e:
        exception_handler(e)


def solve_problem():
    # I think we can take advantage of the key inherent to python's list.sort() function
    # I will have to modify what the compare_lists outputs, but should be fine
    # I don't want to implement a custom merge sort please don't make me do this
    # I think we just do a regular old insertion sort :)
    packet_list = get_packet_list(input_file)
    start_div = [[2]]
    end_div = [[6]]
    start_ind = find_packet_insertion(start_div, packet_list)
    end_ind = find_packet_insertion(end_div, packet_list) + 1
    decoder_key = start_ind * end_ind
    print_to_display(f"The decoder key for the distress signal is {str(decoder_key)}", bold=True)
    print("\n\n")


def get_packet_list(file_name):  # returns sorted list of packets
    with open(file_name, "r") as file:
        text = file.read()
    pairs = text.split("\n\n")
    all_packets = []
    for pair in pairs:
        pair1, pair2 = pair.split("\n")
        list1 = create_list(pair1)
        list2 = create_list(pair2)
        pair_order = [list1, list2]
        if compare_lists(list1, list2) == "disorder":
            pair_order = [list2, list1]
        if not all_packets:
            all_packets = pair_order
        else:
            curr_item = 0
            while curr_item < len(all_packets) and len(pair_order) != 0:
                if compare_lists(all_packets[curr_item], pair_order[0]) == "disorder":
                    all_packets.insert(curr_item, pair_order[0])
                    pair_order = pair_order[1:]
                curr_item += 1
            all_packets = all_packets + pair_order
    return all_packets


def find_packet_insertion(divider, packet_list):
    for ind, packet in enumerate(packet_list):
        if compare_lists(packet, divider) == "disorder":
            return ind + 1  # It's not zero based packet numbering
    return len(packet_list) + 1
