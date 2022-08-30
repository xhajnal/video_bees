import csv
from time import time

from _socket import gethostname
from termcolor import colored
from config import get_bee_max_step_len, get_distance_from_calculated_arena
from misc import delete_indices


def single_trace_checker(traces, silent=False, debug=False):
    """ Checks a single trace.

    :arg traces: (list): a list of Traces
    :arg silent (bool) if True no output is shown
    :arg debug (bool) if True extensive output is shown
    :returns traces: (list): a list of Traces
    """
    print(colored("SINGLE TRACE CHECKER", "blue"))
    start_time = time()
    traces_with_zero_len_in_xy = []
    number_of_traces = len(traces)
    for index, trace in enumerate(traces):
        if not silent:
            print(colored(f"{trace}", "blue"))
        if trace.trace_length == 0:
            if not silent:
                print(colored("This trace has length of 0 in x,y. Gonna delete trace of this agent!", "red"))  ## this can be FP
            traces_with_zero_len_in_xy.append(index)
        if trace.max_step_len > get_bee_max_step_len():
            if not silent:
                print(colored(f"This agent has moved {trace.max_step_len} in a single step on frame {trace.max_step_len_frame_number}, you might consider fixing it!", "yellow"))
        # if not silent:
        #     print()

    # DELETING TRACES WITH 0 LEN in XY
    traces = delete_indices(traces_with_zero_len_in_xy, traces)
    print(colored(f"Returning {len(traces)} traces, {number_of_traces - len(traces)} deleted. It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "yellow"))
    return traces


def check_inside_of_arena(traces, silent=False, debug=False):
    """ Checks all traces whether each is inside the arena.

    :arg traces: (list): a list of Traces
    :arg silent (bool) if True no output is shown
    :arg debug (bool) if True extensive output is shown
    :returns traces: (list): a list of Traces
    """
    print(colored("SINGLE TRACE INSIDE ARENA CHECKER", "blue"))
    start_time = time()
    number_of_traces = len(traces)

    all_locations = []
    for trace in traces:
        all_locations.extend(trace.locations)

    min_x = 999999999999999999
    min_y = 999999999999999999
    max_x = -9
    max_y = -9

    for location in all_locations:
        if location[0] < min_x:
            min_x = location[0]
        if location[1] < min_y:
            min_y = location[1]
        if location[0] > max_x:
            max_x = location[0]
        if location[1] > max_y:
            max_y = location[1]

    if debug:
        print(f"min max values min_x {min_x} min_y {min_y},  max_x {max_x} max_y {max_y}")

    diam_x = max_x - min_x
    diam_y = max_y - min_y

    if debug:
        print(f"diameter x {diam_x}, diameter y {diam_y}")

    diam = max(diam_x, diam_y)

    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2

    if debug:
        print(f"the center values are mid_x {mid_x} mid_y {mid_y}")

    traces_to_be_deleted = []

    for index, trace in enumerate(traces):
        for location in trace.locations:
            if (location[0] - mid_x)**2 + (location[1] - mid_y)**2 > (diam/2 + get_distance_from_calculated_arena())**2:
                traces_to_be_deleted.append(index)
                print(colored(f"checking trace {trace.trace_id} location {location} seems to be outside of the arena! Gonna delete this trace!", "red"))
                break

    delete_indices(traces_to_be_deleted, traces, debug=debug)
    print(colored(f"Returning {len(traces)} traces, {number_of_traces - len(traces)} deleted. It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "yellow"))
    return traces


def dummy_collision_finder(csv_file, size):
    """ Parses  a loopy csv file nn/ai. It prints the frame numbers where the additional agents.
    The print includes agent's id.
    Returns a list of frames where an additional agent was found.

    :arg csv_file: (file): input file
    :arg size: (int): expected number of agents
    :returns: frame_numbers_of_collided_agents: list of frames where an additional agent was found
    """
    print(colored("DUMMY COLLISION FINDER", "blue"))
    reader = csv.DictReader(csv_file)
    i = 0
    frame_numbers_of_collided_agents = []

    for row in reader:
        # print(row['oid'])
        if int(row['oid']) > size - 1:
            print("A new fake agents appears on frame number", row['frame_number'], "iteration number", i, "with oid",
                  row['oid'])
            frame_numbers_of_collided_agents.append(row['frame_number'])
            size = size + 1
        i = i + 1

    return frame_numbers_of_collided_agents
