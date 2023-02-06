import copy
import csv
import math
from time import time
import numpy as np
from _socket import gethostname
from termcolor import colored

from fake import get_real_whole_frame_range, get_whole_frame_range
from config import get_bee_max_step_len, get_distance_from_calculated_arena
from misc import delete_indices, has_overlap
from trace import Trace
from traces_logic import compute_arena, compute_whole_frame_range


def remove_full_traces(traces, removed_traces, population_size, silent=False, debug=False):
    """ Removes traces of full range

        :arg traces: (list): a list of Traces
        :arg removed_traces: (list): a list of already removed Traces
        :arg real_whole_frame_range: [int, int]: real frame range of the whole video (without margins)
        :arg population_size: (int): population population_size of original traces
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :returns traces: (list): a list of truncated Traces
        :returns traces: (list): a list of old Traces
        :returns new_population_size: (int): population population_size of new traces
        """
    try:
        real_whole_frame_range = get_real_whole_frame_range()
    except:
        real_whole_frame_range = compute_whole_frame_range(traces)

    indices_to_be_deleted = []

    print(colored("REMOVING TRACES OF FULL RANGE", "blue"))
    deleted = 0
    for index, trace in enumerate(traces):
        if trace.check_whether_is_done(real_whole_frame_range):
            # print(colored(f"Removing trace {trace.trace_id}", "blue"))
            print(colored(f"Removing trace {index}({trace.trace_id}))", "blue"))
            removed_traces.append(traces[index])
            indices_to_be_deleted.append(index)
            deleted = deleted + 1

    delete_indices(indices_to_be_deleted, traces)

    print()
    return traces, removed_traces, population_size - deleted


def single_trace_checker(traces, min_trace_range_len=False, vicinity=False, silent=False, debug=False):
    """ Checks a single trace.

    :arg traces: (list): a list of Traces
    :arg min_range_len: (int): minimal length of trace in frames
    :arg vicinity: (int): number of frames a short trace has to be far from another short trace to be removed, set False for no check
    :arg silent: (bool): if True minimal output is shown
    :arg debug: (bool): if True extensive output is shown
    :returns traces: (list): a list of Traces
    """
    print(colored("SINGLE TRACE CHECKER", "blue"))
    start_time = time()
    traces_with_zero_len_in_xy = []
    removed_short_traces = []
    removed_short_traces_indices = []
    number_of_traces = len(traces)

    for index, trace in enumerate(traces):
        if not silent:
            print(colored(f"trace index:{index} {trace}", "blue"))
        if trace.trace_length == 0:
            if not silent:
                print(colored("Trace length of 0 in x,y. Will delete trace of this agent!", "red"))  ## this can be FP
            traces_with_zero_len_in_xy.append(index)
        if min_trace_range_len is not False:
            if trace.frame_range_len < min_trace_range_len:
                removed_short_traces.append(trace)
                removed_short_traces_indices.append(index)
                if not silent:
                    print(colored(f"Trace length in frames {trace.frame_range_len}<{min_trace_range_len}. Will delete trace of this agent!", "red"))  ## this can be FP
        if trace.max_step_len > get_bee_max_step_len():
            if not silent:
                print(colored(f"This agent has moved {trace.max_step_len} in a single step on frame {trace.max_step_len_frame_number}, you might consider fixing it!", "yellow"))
        # if not silent:
        #     print()

    # DELETING TRACES WITH 0 LEN in XY and WITH FRAME RANGE < min_range_len
    # Not include short traces near other short traces
    if vicinity is not False:
        not_to_be_deleted_indices = []
        frame_ranges_of_removed_traces = []
        for trace in removed_short_traces:
            frame_ranges_of_removed_traces.append(trace.frame_range)

        for index, frame_range1 in enumerate(frame_ranges_of_removed_traces):
            for index2, frame_range2 in enumerate(frame_ranges_of_removed_traces):
                if index == index2:
                    continue
                if has_overlap([frame_range1[0]-vicinity, frame_range1[1]+vicinity], frame_range2):
                    not_to_be_deleted_indices.append(index)
                    break

        delete_indices(not_to_be_deleted_indices, removed_short_traces_indices)
        delete_indices(not_to_be_deleted_indices, removed_short_traces)
        # for index in not_to_be_deleted_indices:
        #     del removed_short_traces_indices[index]
        #     del removed_short_traces[index]

    # Actually delete the races
    traces = delete_indices(traces_with_zero_len_in_xy + removed_short_traces_indices, traces)

    print(colored(f"Returning {len(traces)} traces, {number_of_traces - len(traces)} deleted. "
                  f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
    return traces, removed_short_traces


## BEE SPECIFIC
# TODO add tests
def check_inside_of_arena(traces, silent=False, debug=False):
    """ Checks all traces whether each is inside the arena.

    Specificity: the ARENA is ROUND, all the individuals SHOULD BE INSIDE IT ALL THE TIME

    :arg traces: (list): a list of Traces
    :arg silent: (bool): if True minimal output is shown
    :arg debug: (bool): if True extensive output is shown
    :returns traces: (list): a list of Traces
    """
    print(colored("SINGLE TRACE INSIDE ARENA CHECKER", "blue"))
    start_time = time()
    number_of_traces = len(traces)

    ## COMPUTE THE ARENA SIZE
    center, diam = compute_arena(traces, debug)
    mid_x, mid_y = center

    ## CHECK FOR THE BEES OUTSIDE OF THE COMPUTED ARENA
    traces_to_be_deleted = []
    for index, trace in enumerate(traces):
        for location in trace.locations:
            if (location[0] - mid_x)**2 + (location[1] - mid_y)**2 > (diam/2 + get_distance_from_calculated_arena())**2:
                traces_to_be_deleted.append(index)
                # print(colored(f"checking trace {trace.trace_id} location {location} seems to be outside of the arena! Will delete this trace!", "red"))
                if not silent:
                    print(colored(f"checking trace {index}({trace.trace_id}) of {trace.frame_range_len} frames: location {location} seems to be outside of the arena! Will delete this trace!", "red"))
                break

    delete_indices(traces_to_be_deleted, traces, debug=debug)
    print(colored(f"Returning {len(traces)} traces, {number_of_traces - len(traces)} deleted. "
                  f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
    return traces


# TODO add tests
def simple_additional_bee_finder(csv_file, population_size):
    """ Parses a loopy csv file _nn.csv
    It prints the frame numbers where the additional agents.
    The print includes agent's id.
    Returns a list of frames where an additional agent was found.

    :arg csv_file: (file): input file
    :arg population_size: (int): expected number of agents
    :returns: frame_numbers_of_additional_agents: list of frames where an additional agent was found
    """
    print(colored("SIMPLE COLLISION FINDER", "blue"))
    reader = csv.DictReader(csv_file)
    i = 0
    frame_numbers_of_additional_agents = []

    for row in reader:
        # print(row['oid'])
        if int(row['oid']) > population_size - 1:
            print("A new fake agents appears on frame number", row['frame_number'], "iteration number", i, "with oid", row['oid'])
            frame_numbers_of_additional_agents.append(row['frame_number'])
            population_size = population_size + 1
        i = i + 1

    return frame_numbers_of_additional_agents


## TODO add to config - probably only cosmetic to the trace (should not alter the further analysis that much)
# TODO add tests
def track_jump_back_and_forth(trace, trace_index, show_plots=False, silent=False, debug=False):
    """ Tracks when the tracking of the bee jumped at some place and then back quickly.

    :arg trace: (Trace): a Trace to check
    :arg trace_index: (int): print auxiliary information of index in list of traces of the trace
    :arg whole_frame_range: [int, int]: frame range of the whole video (with margins)
    :arg show_plots: (bool): a flag whether to show the jump in a plot
    :arg silent: (bool): if True minimal output is shown
    :arg debug: (bool): if True extensive output is shown
    """
    assert isinstance(trace, Trace)
    whole_frame_range = get_whole_frame_range()
    # if not silent:
    #     print(colored(f"TRACE JUMP BACK AND FORTH CHECKER with trace {trace_index}({trace.trace_id})", "blue"))
    start_time = time()

    number_of_jump_detected = 0

    # define surrounding in frames to find a jump
    frame_width = 5

    # define length of the jump
    jump_len = 50

    # define surrounding to jump back
    jump_back_dist = 10

    location_index = 0
    while location_index < len(trace.locations)-1:
        potential_jump_detected = False
        for location_index2 in range(location_index + 1, location_index+frame_width+1):
            try:
                a = trace.locations[location_index2]
            except IndexError:
                break
            if not potential_jump_detected and math.dist(trace.locations[location_index], trace.locations[location_index2]) >= jump_len:
                potential_jump_detected = True
                jump_to_index = location_index2
            if potential_jump_detected:
                if math.dist(trace.locations[location_index], trace.locations[location_index2]) <= jump_back_dist:
                    # A jump found
                    number_of_jump_detected = number_of_jump_detected + 1
                    if not silent:
                        print(f" Jump back and forth detected trace {trace_index}({trace.trace_id}),"
                              f" with start frame {trace.frames_list[location_index]}, while jump to"
                              f" frame {trace.frames_list[jump_to_index]}"
                              f" with distance {math.dist(trace.locations[location_index], trace.locations[jump_to_index])}"
                              f" and jumping back to frame {trace.frames_list[location_index2]} with distance to start"
                              f" {math.dist(trace.locations[location_index], trace.locations[location_index2])}")

                    # Show the jump in plot
                    if show_plots and debug:
                        trace.show_trace_in_xy(from_to_frame=[trace.frames_list[location_index]-2, trace.frames_list[location_index2]+2], show=True, subtitle=f" jump to {trace.frames_list[jump_to_index]}")

                    # Smoothen the jump
                    spam = np.linspace(trace.locations[location_index], trace.locations[location_index2], num=location_index2 - location_index + 1, endpoint=True)
                    for index_index, location_index in enumerate(range(location_index, location_index2+1)):
                        trace.locations[location_index] = spam[index_index]

                    # if show_plots:
                    #     trace.show_trace_in_xy(whole_frame_range, from_to_frame=[trace.frames_list[index]-2, trace.frames_list[index2]+2], show=True, subtitle=f" Smoothened jump to {trace.frames_list[jump_to_index]}")

                    # Move forth in frames
                    location_index = location_index2
                    potential_jump_detected = False
        location_index = location_index + 1

    # print(colored(f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "yellow"))
    return number_of_jump_detected
