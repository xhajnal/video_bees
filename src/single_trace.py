import copy
import csv
import math
from time import time

import numpy as np
from _socket import gethostname
from termcolor import colored
from config import get_bee_max_step_len, get_distance_from_calculated_arena
from misc import delete_indices
from trace import Trace


def remove_full_traces(traces, real_whole_frame_range, population_size, silent=False, debug=False):
    """ Removes traces of full range

        :arg traces: (list): a list of Traces
        :arg real_whole_frame_range: [int, int]: frame range of the whole video
        :arg silent (bool) if True no output is shown
        :arg debug (bool) if True extensive output is shown
        :returns traces: (list): a list of truncated Traces
        :returns traces: (list): a list of old Traces
        :returns new_population_size: (int): population size of new traces
        """
    print(colored("REMOVING TRACES OF FULL RANGE", "blue"))
    deleted = 0
    old_traces = copy.copy(traces)
    for index, trace in enumerate(traces):
        if trace.frame_range == real_whole_frame_range:
            print(colored(f"Removing trace {trace.trace_id}", "blue"))
            del traces[index]
            deleted = deleted + 1

    print()
    return traces, old_traces, population_size - deleted


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


def track_jump_back_and_forth(trace, whole_frame_range, show_plots=False, silent=False, debug=False):
    """ Tracks when the tracking of the bee jumped at some place and then back quickly.

    :arg trace: (Trace): a Traces to check
    :arg whole_frame_range: [int, int]: frame range of the whole video
    :arg show_plots: (bool): a flag whether to show the jump in a plot
    :arg silent (bool) if True no output is shown
    :arg debug (bool) if True extensive output is shown
    """
    assert isinstance(trace, Trace)
    if not silent:
        print(colored(f"TRACE JUMP BACK AND FORTH CHECKER with trace {trace.trace_id}", "blue"))
    start_time = time()

    number_of_jump_detected = 0

    # define surrounding in frames to find a jump
    frame_width = 5

    # define length of the jump
    jump_len = 50

    # define surrounding to jump back
    jump_back_dist = 10

    index = 0
    while index < len(trace.locations)-1:
        potential_jump_detected = False
        for index2 in range(index + 1, index+frame_width+1):
            try:
                a = trace.locations[index2]
            except IndexError:
                break
            if not potential_jump_detected and math.dist(trace.locations[index], trace.locations[index2]) >= jump_len:
                potential_jump_detected = True
                jump_to_index = index2
            if potential_jump_detected:
                if math.dist(trace.locations[index], trace.locations[index2]) <= jump_back_dist:
                    # a jump found
                    number_of_jump_detected = number_of_jump_detected + 1
                    if not silent:
                        print(f" Jump back and forth detected, with start frame {trace.frames_list[index]}, while jump to"
                              f" frame {trace.frames_list[jump_to_index]}"
                              f" with distance {math.dist(trace.locations[index], trace.locations[jump_to_index])}"
                              f" and jumping back to frame {trace.frames_list[index2]} with distance to start"
                              f" {math.dist(trace.locations[index], trace.locations[index2])}")

                    # show jump in plot
                    if show_plots and not silent:
                        trace.show_trace_in_xy(whole_frame_range, from_to_frame=[trace.frames_list[index]-2, trace.frames_list[index2]+2], show=True, subtitle=f" jump to {trace.frames_list[jump_to_index]}")

                    # smoothen the jump
                    spam = np.linspace(trace.locations[index], trace.locations[index2], num=index2 - index + 1, endpoint=True)
                    for index_index, location_index in enumerate(range(index, index2+1)):
                        trace.locations[location_index] = spam[index_index]
                    # if show_plots:
                    #     trace.show_trace_in_xy(whole_frame_range, from_to_frame=[trace.frames_list[index]-2, trace.frames_list[index2]+2], show=True, subtitle=f" Smoothened jump to {trace.frames_list[jump_to_index]}")

                    # move forth in frames
                    index = index2
                    potential_jump_detected = False
        index = index + 1

    # print(colored(f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "yellow"))
    return number_of_jump_detected
