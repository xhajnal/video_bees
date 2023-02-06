import math
from time import time
from _socket import gethostname
from matplotlib import pyplot as plt
from termcolor import colored
from operator import countOf
from scipy.interpolate import InterpolatedUnivariateSpline

from config import *
from fake import get_whole_frame_range
from misc import is_in, delete_indices, dictionary_of_m_overlaps_of_n_intervals, get_index_of_shortest_range, \
    get_overlap, range_len, to_vect, calculate_cosine_similarity, has_overlap, flatten
from trace import Trace
from traces_logic import swap_two_overlapping_traces, merge_two_traces_with_gap, merge_two_overlapping_traces, \
    compute_whole_frame_range, get_video_whole_frame_range
from video import show_video
from visualise import scatter_detection, show_plot_locations, show_overlap_distances


global all_overlaps_count
all_overlaps_count = 0

global all_overlaps_deleted
all_overlaps_deleted = 0


def get_all_overlaps_count():
    return all_overlaps_count


def get_all_overlaps_deleted():
    return all_overlaps_deleted


def track_swapping_loop(traces, automatically_swap=False, input_video=False, silent=False, debug=False, video_params=False):
    """ Calls track_swapping until no swap is available

        :arg traces: (list): list of Traces
        :arg whole_frame_range: [int, int]: frame range of the whole video (with margins)
        :arg automatically_swap: (bool): if True swaps without asking
        :arg input_video: (str or bool): if set, path to the input video
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :arg video_params: (bool or tuple): i if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
    """
    # whole_frame_range = get_whole_frame_range()

    start_time = time()
    keep_looking = True
    number_of_swaps = 0

    while keep_looking:
        keep_looking = track_swapping(traces, automatically_swap=automatically_swap, input_video=input_video, silent=silent, debug=debug, video_params=video_params)
        if keep_looking:
            number_of_swaps = number_of_swaps + 1

    if number_of_swaps == 0:
        print(colored(f"There were no traces considerable of swapping. It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
    else:
        print(colored(f"In total, we swapped {number_of_swaps} pairs of traces. It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
    return number_of_swaps


def track_swapping(traces, automatically_swap=False, input_video=False, silent=False, debug=False, video_params=False):
    """ Tracks the possible swapping traces of two bees in the run.

        :arg traces: (list): list of Traces
        :arg whole_frame_range: [int, int]: frame range of the whole video (with margins)
        :arg automatically_swap: (bool or list of int): if True swaps all without asking, if list it contains frames to autopass
        :arg input_video: (str or bool): if set, path to the input video
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :arg video_params: (bool or tuple): i if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
        :return: traces: (list): list of trimmed Traces
    """
    print(colored("TRACE SWAPPING OF TWO BEES", "blue"))

    # Obtained variables
    # whole_frame_range = get_whole_frame_range()

    # Check
    if len(traces) < 2:
        print(colored("There is only one/no trace, skipping this analysis.\n", "yellow"))
        return

    # obtain overlaps of pairs of traces - pair of indices -> frame range
    dictionary = dictionary_of_m_overlaps_of_n_intervals(2, list(map(lambda x: x.frame_range, traces)), skip_whole_in=False)
    if debug:
        print("overlapping pairs:", dictionary)

    # for each overlap, check frame by frame distance, if below 100 look at the movement vectors
    for overlapping_pair_of_traces in dictionary.keys():
        # Get traces info
        trace1_index = overlapping_pair_of_traces[0]
        trace2_index = overlapping_pair_of_traces[1]
        trace1 = traces[trace1_index]
        trace2 = traces[trace2_index]

        # get locations of the first pair
        first_trace_locations = trace1.get_locations_from_frame_range(dictionary[overlapping_pair_of_traces])
        # get locations of the second pair
        second_trace_locations = trace2.get_locations_from_frame_range(dictionary[overlapping_pair_of_traces])

        # maybe use in future to store distances of points of the two traces
        # distances = []

        for index in range(2, len(first_trace_locations)):
            dist = math.dist(first_trace_locations[index], second_trace_locations[index])
            # distances.append(dist)
            if dist < get_maximal_distance_to_check_for_trace_swapping():
                if debug:
                    print(f"In pair {trace1_index}({trace1.trace_id}), {trace2_index}({trace2.trace_id}), on frame {dictionary[overlapping_pair_of_traces][0]+index}, the distance is {dist}")
                vector1 = to_vect(first_trace_locations[index-2], first_trace_locations[index-1])
                vector2 = to_vect(second_trace_locations[index-2], second_trace_locations[index-1])
                vector1_next = to_vect(first_trace_locations[index-1], first_trace_locations[index])
                vector2_next = to_vect(second_trace_locations[index-1], second_trace_locations[index])
                if calculate_cosine_similarity(vector1, vector2_next) > calculate_cosine_similarity(vector1, vector1_next) \
                        and calculate_cosine_similarity(vector2, vector1_next) > calculate_cosine_similarity(vector2, vector2_next) \
                        and math.dist(first_trace_locations[index-1], first_trace_locations[index]) > math.dist(first_trace_locations[index-1], second_trace_locations[index]):
                    print(colored(f"It seems the traces {trace1_index}({trace1.trace_id}), {trace2_index}({trace2.trace_id}) are swapped on frame {dictionary[overlapping_pair_of_traces][0] + index}","yellow"))
                    print(f"first_trace_location {first_trace_locations[index]}")
                    print(f"second_trace_location {second_trace_locations[index]}")
                    print(f"cosine_similarity(vector1, vector2_next) > cosine_similarity(vector1, vector1_next): {calculate_cosine_similarity(vector1, vector2_next)} > {calculate_cosine_similarity(vector1, vector1_next)}")
                    print(f"cosine_similarity(vector2, vector1_next) > cosine_similarity(vector2, vector2_next): {calculate_cosine_similarity(vector2, vector1_next)} > {calculate_cosine_similarity(vector2, vector2_next)}")
                    print(f"dist(trace1.location_before, trace1.this_location) > dist(trace1.location_before, TRACE2.this_point): {math.dist(first_trace_locations[index-1], first_trace_locations[index])} > {math.dist(first_trace_locations[index-1], second_trace_locations[index])}")

                    if automatically_swap is True:
                        answer = "6"
                    elif isinstance(automatically_swap, list) and dictionary[overlapping_pair_of_traces][0] + index in automatically_swap:
                        answer = "6"
                    else:
                        scatter_detection([trace1, trace2],
                                          get_video_whole_frame_range([trace1, trace2]),
                                          subtitle="Traces to be swapped.")
                        show_plot_locations([trace1, trace2], whole_frame_range=[0, 0],
                                            from_to_frame=[dictionary[overlapping_pair_of_traces][0] + index - 30,
                                                           dictionary[overlapping_pair_of_traces][0] + index + 30],
                                            show_middle_point=True,
                                            subtitle=f"Traces to be swapped on frame {dictionary[overlapping_pair_of_traces][0] + index}. +-30frames")
                        # show_video(input_video, traces=(), frame_range=(), video_speed=0.1, wait=False, points=(), video_params=True)
                        show_video(input_video, traces=[trace1, trace2], frame_range=[dictionary[overlapping_pair_of_traces][0] + index - 30, dictionary[overlapping_pair_of_traces][0] + index + 30],
                                   video_speed=0.1, wait=True, video_params=video_params)

                        to_show_longer_video = input("Do you want to see longer video? (yes or no):")
                        if "y" in to_show_longer_video.lower():
                            show_video(input_video, traces=[trace1, trace2], frame_range=[trace1.frame_range[0]-15, trace2.frame_range[1]+15],
                                       video_speed=0.1, wait=True, video_params=video_params)

                        answer = input("Is this right? (yes or no)")
                    if any(answer.lower() == f for f in ["yes", 'y', '1', 'ye', '6']):
                        print(colored(f"Swapping the traces {trace1_index}({trace1.trace_id}), {trace2_index}({trace2.trace_id}) on frame {dictionary[overlapping_pair_of_traces][0] + index}\n ", "blue"))
                        a, b = swap_two_overlapping_traces(trace1, trace2, dictionary[overlapping_pair_of_traces][0]+index, silent=silent, debug=debug)
                        traces[trace1_index], traces[trace2_index] = a, b
                        return True
                else:
                    if calculate_cosine_similarity(vector1, vector2_next) > calculate_cosine_similarity(vector1, vector1_next):
                        if debug:
                            print(colored(f"vector2_next {vector2_next} is more similar to vector1 {vector1} than to vector1_next {vector1_next}", "yellow"))
                    if calculate_cosine_similarity(vector2, vector1_next) > calculate_cosine_similarity(vector2, vector2_next):
                        if debug:
                            print(colored(f"vector1_next {vector1_next} is more similar to vector2 {vector2} than to vector2_next {vector2_next}", "yellow"))
                    if math.dist(first_trace_locations[index-1], first_trace_locations[index]) > math.dist(first_trace_locations[index-1], second_trace_locations[index]):
                        if debug:
                            print(colored(f"trace 1 previous point {first_trace_locations[index-1]} is closer to next point of trace2 {second_trace_locations[index]} than to next point of this trace {first_trace_locations[index]}", "yellow"))
    if not silent:
        print(colored("We haven't found any possible swap this time.", "yellow"))
    return False


## DEPRECATED
# def trim_out_additional_agents_over_long_traces3(traces, population_size, silent=False, debug=False):
#     """ Trims out additional appearance of an agent when long traces are over here.
#
#         :arg traces: (list): list of Traces
#         :arg population_size: (int): expected number of agents
#         :arg silent: (bool): if True minimal output is shown
#         :arg debug: (bool): if True extensive output is shown
#         :returns: traces: (list): list of trimmed Traces
#     """
#     print(colored("TRIM OUT ADDITIONAL AGENTS OVER A LONG TRACES 3", "blue"))
#     ranges = []
#     for index1, trace in enumerate(traces):
#         assert isinstance(trace, Trace)
#         trace.check_trace_consistency()
#         ranges.append(trace.frame_range)
#     ranges = sorted(ranges)
#     dictionary = dictionary_of_m_overlaps_of_n_intervals(population_size + 1, ranges, skip_whole_in=False, debug=debug)
#
#     indices_of_intervals_to_be_deleted = []
#
#     for overlap in dictionary.keys():
#         if debug:
#             print(colored(f"Currently checking overlapping indices: {overlap}", "blue"))
#         overlapping_ranges = []
#         for interval_index in overlap:
#             overlapping_ranges.append(ranges[interval_index])
#
#         shortest_index = overlap[get_index_of_shortest_range(overlapping_ranges)]
#         if debug:
#             print(colored(f" Index_of_shortest_range: {shortest_index}", "blue"))
#         shortest_range = ranges[shortest_index]
#
#         to_be_deleted = True
#         for rangee in overlapping_ranges:
#             if debug:
#                 print(colored(f" Checking whether range index {shortest_index}, {shortest_range}, is in {rangee}", "blue"))
#             if not is_in(shortest_range, rangee):
#                 to_be_deleted = False
#
#         if to_be_deleted:
#             if debug:
#                 print(colored(f"Will delete range index {shortest_index}, {shortest_range}", "yellow"))
#             indices_of_intervals_to_be_deleted.append(shortest_index)
#
#     if debug:
#         print(colored(f"Indices_of_intervals_to_be_deleted: {indices_of_intervals_to_be_deleted}", "red"))
#     traces = delete_indices(indices_of_intervals_to_be_deleted, traces)
#
#     return traces


# TODO add tests
def trim_out_additional_agents_over_long_traces2(traces, overlap_dictionary, population_size, silent=False, debug=False):
    """ Trims out additional appearance of an agent when long traces are over here.

        :arg traces: (list): list of Traces
        :arg overlap_dictionary: (dict): dictionary_of_m_overlaps_of_n_intervals
        :arg population_size: (int): expected number of agents
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :returns: traces: (list): list of trimmed Traces
    """
    print(colored("TRIM OUT ADDITIONAL AGENTS OVER A LONG TRACES", "blue"))
    start_time = time()
    ranges = []
    for index1, trace in enumerate(traces):
        assert isinstance(trace, Trace)
        trace.check_trace_consistency()
        ranges.append(trace.frame_range)
    # rangees = copy(ranges)
    # ranges = sorted(ranges)

    # assert ranges == rangees

    dict_start_time = time()

    if overlap_dictionary is None:
        dictionary = dictionary_of_m_overlaps_of_n_intervals(population_size + 1, ranges, skip_whole_in=False, debug=False)
    else:
        assert isinstance(overlap_dictionary, dict)
        try:
            ## check that the dictionary is of m overlaps
            if len(list(overlap_dictionary.keys())[0]) != population_size + 1:
                raise Exception("Given dictionary is not of m overlaps.")
        except IndexError:
            pass
        dictionary = overlap_dictionary

    print(colored(f"Creation of the dictionary of m overlaps over n intervals took {round(time() - dict_start_time, 3)} seconds.", "yellow"))
    # print(dictionary)

    indices_of_intervals_to_be_deleted = []
    keys_to_be_deleted = []

    for overlap in dictionary.keys():
        if debug:
            print(colored(f" Currently checking overlapping indices: {overlap}", "blue"))
        overlapping_ranges = []
        for interval_index in overlap:
            try:
                overlapping_ranges.append(ranges[interval_index])
            except IndexError as err:
                raise err

        index_of_shortest_range = overlap[get_index_of_shortest_range(overlapping_ranges)]
        if debug:
            print(colored(f" Index_of_shortest_range: {index_of_shortest_range}", "blue"))
        shortest_range = ranges[index_of_shortest_range]
        if debug:
            print(colored(f" Shortest_range: {shortest_range}", "blue"))

        ## NEW
        if shortest_range == dictionary[overlap]:
            if debug:
                print(colored(f" Will delete range index {index_of_shortest_range}, {shortest_range}", "yellow"))
            indices_of_intervals_to_be_deleted.append(index_of_shortest_range)
            keys_to_be_deleted.append(overlap)

        ## DEPRECATED
        # to_be_deleted = True
        # for rangee in overlapping_ranges:
        #     if debug:
        #         print(colored(f" Checking whether range index {index_of_shortest_range}, {shortest_range}, is in {rangee}", "blue"))
        #     if not is_in(shortest_range, rangee):
        #         to_be_deleted = False
        #
        # if to_be_deleted:
        #     if debug:
        #         print(colored(f"Will delete range index {index_of_shortest_range}, {shortest_range}", "yellow"))
        #     indices_of_intervals_to_be_deleted.append(index_of_shortest_range)
        #     keys_to_be_deleted.append(overlap)

    if debug:
        print(colored(f" Indices_of_intervals_to_be_deleted: {indices_of_intervals_to_be_deleted}", "red"))
    traces = delete_indices(indices_of_intervals_to_be_deleted, traces)
    if debug:
        print(colored(f" keys_to_be_deleted: {keys_to_be_deleted}", "red"))
    for key in keys_to_be_deleted:
        del dictionary[key]

    print(colored(f"trim_out_additional_agents_over_long_traces2 analysis done. It took {gethostname()} {round(time() - start_time, 3)} seconds.", "yellow"))
    print(colored(f"Returning {len(traces)} traces, {len(indices_of_intervals_to_be_deleted)} shorter than in previous iteration. \n", "green"))
    ## TODO fix to return traces, dictionary
    return traces, None


# DEPRECATED
# def trim_out_additional_agents_over_long_traces_old(traces, population_size, silent=False, debug=False):
#     """ Trims out additional appearance of an agent when long traces are over here.
#
#         :arg traces: (list): list of Traces
#         :arg population_size: (int): expected number of agents
#         :arg silent: (bool): if True minimal output is shown
#         :arg debug: (bool): if True extensive output is shown
#         :returns: traces: (list): list of trimmed Traces
#     """
#     print(colored("TRIM OUT ADDITIONAL AGENTS OVER A LONG TRACES OLD", "blue"))
#     start_time = time()
#     # Obtain the ranges with the population_size of frame more than 100 where all the agents are being tracked
#     ranges = []
#     for index1, trace in enumerate(traces):
#         assert isinstance(trace, Trace)
#         trace.check_trace_consistency()
#         ranges.append(trace.frame_range)
#     ranges = sorted(ranges)
#
#     if population_size == 2:
#         ## CHECKING WHETHER THERE ARE TWO OVERLAPPING TRACES
#         at_least_two_overlaps = []
#         for index1, range1 in enumerate(ranges[:-1]):
#             current_overlaps = []
#             if debug:
#                 print()
#             for index2, range2 in enumerate(ranges):
#                 if index1 == index2:  # Skip the same index
#                     continue
#
#                 if range2[1] <= range1[0]:  # Skip the traces which end before start of this
#                     continue
#
#                 if range2[0] >= range1[1]:  # Beginning of the further intervals is behind the end of current one
#                     # We go through the set of overlapping intervals
#                     if debug:
#                         print("current interval:", range1)
#                         print("The set of overlapping intervals:", current_overlaps)
#                     i = -1
#                     min_range = 0
#                     # We search for the longest overlapping interval
#                     for index3, range3 in enumerate(current_overlaps):
#                         if len(range3) > min_range:
#                             i = index3
#                             min_range = len(range3)
#                     if i == -1:
#                         if debug:
#                             print("there was no overlapping interval")
#                         at_least_two_overlaps.append([])
#                     else:
#                         if debug:
#                             print("picking the longest interval:", current_overlaps[i])
#                         at_least_two_overlaps.append(current_overlaps[i])
#                     # Skipping the intervals which starts further than this interval
#                     break
#                 else:
#                     # Check whether the beginning of the two intervals are overlapping
#                     if max(range1[0], range2[0]) > min(range1[1], range2[1]):
#                         print(colored(range1, "red"))
#                         print(colored(range2, "red"))
#                         print("range1[1]", range1[1])
#                         print("range2[0]", range2[0])
#                         print(range2[0] >= range1[1])
#                     # Add the overlap to the list
#                     current_overlaps.append([max(range1[0], range2[0]), min(range1[1], range2[1])])
#                     continue
#         if debug:
#             print(at_least_two_overlaps)
#         # Selecting indices to be deleted
#         indices_to_be_deleted = []
#         for index1, range1 in enumerate(at_least_two_overlaps):
#             if index1 in indices_to_be_deleted:
#                 continue
#             for index2, range2 in enumerate(at_least_two_overlaps):
#                 if index2 in indices_to_be_deleted:
#                     continue
#                 if index1 == index2:
#                     continue
#                 # Start of the second interval is beyond end of first, we move on
#                 if range2[0] > range1[1]:
#                     break
#                 # Range2 is in Range1
#                 if range2[0] >= range1[0] and range2[1] <= range1[1]:
#                     if debug:
#                         print(f"range index {index2} with value {range2} is in range index {index1} with value {range1}")
#                     indices_to_be_deleted.append(index2)
#         # Remove duplicates in the list of overlapping traces
#         if debug:
#             print()
#             print(indices_to_be_deleted)
#         at_least_two_overlaps = delete_indices(indices_to_be_deleted, at_least_two_overlaps)
#     elif population_size == 1:
#         at_least_two_overlaps = []
#         for index1, range1 in enumerate(ranges):
#             at_least_two_overlaps.append(range1)
#     else:
#         raise NotImplemented("I`m sorry Dave, I`m afraid I cannot do that.")
#
#     # Remove intervals which are redundantly overlapping - being over at_least_two_overlaps
#     if debug:
#         print()
#         print(at_least_two_overlaps)
#     traces_indices_to_be_deleted = []
#     for index, tracee in enumerate(traces):
#         for overlap_range in at_least_two_overlaps:
#             if is_in(tracee.frame_range, overlap_range, strict=True):
#                 traces_indices_to_be_deleted.append(index)
#     traces_indices_to_be_deleted = list(reversed(sorted(list(set(traces_indices_to_be_deleted)))))
#     for index in traces_indices_to_be_deleted:
#         del traces[index]
#
#     for trace in traces:
#         trace.check_trace_consistency()
#
#     print(colored(
#         f"trim_out_additional_agents_over_long_traces analysis done. It took {gethostname()} {round(time() - start_time, 3)} seconds.",
#         "yellow"))
#     print(colored(f"Returning {len(traces)} traces, {len(traces_indices_to_be_deleted)} shorter than in previous iteration.", "green"))
#     print()
#     return traces


# TODO add tests
def put_gaping_traces_together(traces, population_size, allow_force_merge=True, silent=False, debug=False):
    """ Puts gaping traces together iff all the agents but one is being tracked.

        :arg traces: (list): list of traces
        :arg population_size: (int): expected number of agents
        :arg allow_force_merge: (bool): iff True force merge is allow
        :arg silent: (bool): iff True minimal output is shown
        :arg debug: (bool): iff True extensive output is shown
        :returns: traces: (list): list of concatenated Traces
    """
    print(colored("PUT GAPING TRACES TOGETHER", "blue"))
    start_time = time()

    # Check
    if len(traces) < 2:
        print(colored("There is only one/no trace, skipping this analysis.\n", "yellow"))
        return traces

    # Code
    reappearance = track_reappearance(traces, show=False)
    if debug:
        print(len(traces))
        print(len(reappearance))

    trace_indices_to_merge = []

    video_range = compute_whole_frame_range(traces)
    if debug:
        print(video_range)

    # Going through the video, searching frames (from start to end)
    step_to = video_range[0]
    do_skip = False
    while step_to <= video_range[1]:  # we are within the video range
        next_steps_to = []  # list of end of ranges to go to
        indices_in_between = []  # list of indices within selected window
        for trace_index, trace in enumerate(traces):
            if trace_index in trace_indices_to_merge:  # skipping the traces which we are gonna merge
                continue
            assert isinstance(trace, Trace)
            if trace.frame_range[0] <= step_to < trace.frame_range[1]:  # if the window is inside of trace frame range
                if debug:
                    # print(colored(f"adding trace {index} ({trace.trace_id}) of {trace.frame_range} to in between", "yellow"))
                    print(colored(f"adding trace {trace_index} of {trace.frame_range} to 'in between'", "yellow"))
                next_steps_to.append(trace.frame_range[1])
                indices_in_between.append(trace_index)
            else:
                if debug:
                    # print(colored(f"skipping trace {index} ({trace.trace_id}) of {trace.frame_range}", "red"))
                    print(colored(f"skipping trace {trace_index} of {trace.frame_range}", "red"))
                continue
        if debug:
            print(colored(f"finished first cycle with next_steps_to:{next_steps_to}", "blue"))

        try:
            next_step_to = min(next_steps_to)
            if debug:
                print("next_steps_to: ", next_steps_to)
        except ValueError:
            if debug:
                print(f"Fixing empty next_steps_to while step_to: {step_to} and next_step_to:{next_step_to}")
            traces_after = 0
            for index3, trace3 in enumerate(traces):
                assert isinstance(trace3, Trace)
                # if trace3.frame_range[0] < step_to:
                if trace3.frame_range[0] < next_step_to:
                    continue
                else:
                    traces_after = traces_after + 1
                    next_step_to = trace3.frame_range[0]
                    next_steps_to.append(next_step_to)
                    step_to = next_step_to
                    if debug:
                        print(f"FIXED next_step_to: {next_step_to}")
                    do_skip = True
                    break
            if traces_after == 0:
                do_skip = True

        if do_skip:
            do_skip = False
            if traces_after == 0:
                break
            else:
                continue

        to_merge = next_steps_to.index(next_step_to)
        index_to_go = indices_in_between[to_merge]
        if debug:
            print("CHECKING")
            print("next_steps_to", next_steps_to)
            print("indices_in_between", indices_in_between)
            print("index_to_go", index_to_go)

        if len(next_steps_to) == population_size:
            # Look for a mergeable trace
            if not silent:
                print(colored(f"Gonna have a look for a second mergeable trace from frame {step_to} till {next_step_to}.", "blue"))
            step_to = next_step_to
            for index2, trace2 in enumerate(traces):
                assert isinstance(trace2, Trace)
                if index2 in trace_indices_to_merge:
                    continue
                if trace2.frame_range[0] < step_to:
                    if debug:
                        # print(colored(f"skipping trace {index2} with id {trace2.trace_id} which starts in {trace2.frame_range[0]}", "green"))
                        print(colored(f"skipping trace {index2} which starts in {trace2.frame_range[0]}", "green"))
                    continue

                trace1 = traces[index_to_go]

                # COMPUTE DISTANCES AND REST
                dist_of_traces_in_frames = trace2.frame_range[0] - trace1.frame_range[-1]
                dist_of_traces_in_xy = math.dist(trace1.locations[-1], trace2.locations[0])

                # EXTRAPOLATE TRACE
                try:
                    last_50_frames = trace1.frames_list[-50:]  # last 50 frames
                    x = list(map(lambda x: x[0], trace1.locations[-50:]))  # last 50 locations x,y respectively
                    y = list(map(lambda y: y[1], trace1.locations[-50:]))
                    splt_x = InterpolatedUnivariateSpline(last_50_frames, x, ext=0)  # extrapolator
                    splt_y = InterpolatedUnivariateSpline(last_50_frames, y, ext=0)

                    extrapolated_point = [splt_x(trace1.frames_list[-1] + dist_of_traces_in_frames),
                                          splt_y(trace1.frames_list[-1] + dist_of_traces_in_frames)]
                    dist_of_trace2_and_extrapolation = math.dist(extrapolated_point, trace2.locations[0])
                except:
                    extrapolated_point = None
                    dist_of_trace2_and_extrapolation = -999999

                # COMPUTE WHETHER THE TWO TRACES ARE "ALIGNED"
                to_merge = True
                reason = ""

                # Check for force_merge
                gap_range = [trace1.frame_range[1], trace2.frame_range[0]]
                if allow_force_merge:
                    force_merge = True
                    for trace in traces:
                        if trace.trace_id == trace1.trace_id or trace.trace_id == trace2.trace_id:
                            continue
                        if has_overlap(gap_range, [trace.frame_range[0] - get_force_merge_vicinity_distance(), trace.frame_range[1] + get_force_merge_vicinity_distance()]):
                            force_merge = False
                            break
                    if force_merge and not silent:
                        print(colored("USING FORCED GAP MERGE", "magenta"))
                else:
                    force_merge = False

                if not force_merge:
                    # the gap is wider than max_trace_gap
                    if trace2.frame_range[0] - step_to > get_max_trace_gap():
                        to_merge = False
                        reason = f"gap too long (> {get_max_trace_gap()})"
                    # length of the second trace is longer than a given number (100)
                    if force_merge and trace2.frame_range_len < get_min_trace_length_to_merge():
                        to_merge = False
                        reason = f"2nd trace too short (< {get_min_trace_length_to_merge()})"
                    # CHECK FOR DISTANCE OF TRACES IN X,Y
                    # if the distance of traces in frames is high
                    if to_merge:
                        if dist_of_traces_in_frames > get_max_trace_gap()/10:
                            if dist_of_traces_in_xy > get_bee_max_step_len()*3:
                                reason = f"long gap too distant (> {get_bee_max_step_len() * 3})"
                                # print(f" hell, we do not merge traces {index} with id {trace1.trace_id} and {index2} with id {trace2.trace_id} as LONG gap has big xy distance ({dist_of_traces_in_xy} > {get_bee_max_step_len()*3}).")
                                # print(f" hell, we do not merge traces {index}({trace1.trace_id}) and {index2}({trace2.trace_id}) as LONG gap has big xy distance ({dist_of_traces_in_xy} > {get_bee_max_step_len() * 3}).")
                                to_merge = False
                        else:
                            if dist_of_traces_in_xy > dist_of_traces_in_frames * get_bee_max_step_len_per_frame():
                                reason = f"short gap too distant (> {dist_of_traces_in_frames * get_bee_max_step_len_per_frame()})"
                                # print(f" hell2, we do not merge traces {index} with id {trace1.trace_id} and {index2} with id {trace2.trace_id} as SHORT gap has big xy distance ({dist_of_traces_in_xy} > {dist_of_traces_in_frames * get_bee_max_step_len_per_frame()} ).")
                                # print(f" hell2, we do not merge traces {index}({trace1.trace_id}) and {index2}({trace2.trace_id}) as SHORT gap has big xy distance ({dist_of_traces_in_xy} > {dist_of_traces_in_frames * get_bee_max_step_len_per_frame()} ).")
                                to_merge = False

                if trace2.frame_range[0] - trace1.frame_range[-1] == 0:  # fix distance of zero len gap
                    distance_per_frame = None
                else:
                    distance_per_frame = dist_of_traces_in_xy / (trace2.frame_range[0] - trace1.frame_range[-1])

                msg = f"{'' if to_merge else 'NOT '}MERGING GAPING TRACES {'' if to_merge else '('+reason+') '}{index_to_go}({trace1.trace_id}) {trace1.frame_range} " \
                      f"of {trace1.frame_range_len} frames and " \
                      f"trace {index2}({trace2.trace_id}) {trace2.frame_range} of " \
                      f"{int(trace2.frame_range_len)} frames| " \
                      f"{dist_of_traces_in_frames} frames apart, x,y-distance {round(dist_of_traces_in_xy, 3)} which is " \
                      f"{round(distance_per_frame, 3) if distance_per_frame is not None else None}/frame. " \
                      f"Last point position: {trace1.locations[-1]} " \
                      f"the extrapolated point is {extrapolated_point} " \
                      f"the distance of extrapolated point to the second trace {round(dist_of_trace2_and_extrapolation, 3)} "
                if not silent:
                    print(colored(msg, "yellow" if to_merge else "red"))

                if to_merge:
                    # print(colored(f"Merging gaping traces {index}({trace1.trace_id}) and {index2}({trace2.trace_id})", "yellow"))
                    trace = merge_two_traces_with_gap(trace1, trace2)
                    if debug:
                        print(trace)
                    trace_indices_to_merge.append(index2)
                    step_to = trace.frame_range[1]
                elif "gap too long" in reason:
                    if not silent:
                        print(colored("SKIPPING OTHER TRACES - as they have even longer gap", "red"))
                    break
        else:
            step_to = next_step_to
        if debug:
            print(colored(f"jumping to step {step_to}", "blue"))

    if debug:
        print(f"Will delete the following traces as we have merged them: {trace_indices_to_merge}")
    traces = delete_indices(trace_indices_to_merge, traces)

    print(colored(f"GAPING TRACES analysis done. It took {gethostname()} {round(time() - start_time, 3)} seconds.", "yellow"))
    print(colored(f"Returning {len(traces)} traces, {len(trace_indices_to_merge)} shorter than in previous iteration.", "green"))
    print()
    return traces


# TODO add tests
def track_reappearance(traces, show=True, debug=False):
    """ Tracks the time it takes for an agent to appear when one is lost (end of a trace)

    :arg traces: (list): a list of Traces
    :arg show: (bool): a flag whether to show the plot
    :arg debug: (bool): if True extensive output is shown

    :returns: time_to_reappear (list): list of times for an agent to reappear after end of a trace
    """
    if debug:
        print(colored("TRACE REAPPEARANCE", "blue"))

    # Check
    if len(traces) < 2:
        print(colored("There is only one/no trace, skipping this analysis.\n", "yellow"))
        return

    frames_of_loss = []
    for trace in traces:
        frames_of_loss.append(trace.frame_range[1])

    frames_of_loss = list(sorted(frames_of_loss))
    if debug:
        print("frames_of_loss", frames_of_loss)

    # for trace in traces:
    #     print(trace.frame_range[0])

    frames_of_reappearance = []
    for frame in frames_of_loss:
        for trace in traces:
            if trace.frame_range[0] < frame:
                continue
            else:
                frames_of_reappearance.append(trace.frame_range[0])
                break
    if debug:
        print("frames_of_reappearance", frames_of_reappearance)

    time_to_reappear = list(map(lambda x, y: y - x, frames_of_loss, frames_of_reappearance))
    if debug:
        print("time_to_reappear", time_to_reappear)

    if show:
        plt.hist(time_to_reappear, bins=20)
        plt.xlabel('Number of frames')
        plt.ylabel('Count')
        plt.title(f'Histogram of times to reappear.')
        plt.show()

    print()
    return time_to_reappear


## CROSS-TRACE ANALYSIS
# TODO add tests
def cross_trace_analyse(traces, silent=False, debug=False):
    """ Checks traces against each other.

    :arg traces: (list): a list of Traces
    :arg silent: (bool): if True minimal output is shown
    :arg debug: (bool): if True extensive output is shown
    """
    print(colored("CROSS-TRACE ANALYSIS", "blue"))
    start_time = time()
    for index, trace1 in enumerate(traces):
        for index2, trace2 in enumerate(traces):
            if index >= index2:
                continue
            if abs(trace1.frame_range[1] - trace2.frame_range[0]) < 100:
                # print(traces[index][str(trace1.frame_range[1])][1])
                # print(traces[index2][str(trace2.frame_range[0])][1])
                point_distance = math.dist(list(map(float, (trace1.locations[-1]))),
                                           list(map(float, (trace2.locations[0]))))
                message = f"The beginning of trace {index}({trace1.trace_id}) is close to end of trace {index2}({trace2.trace_id}) " \
                          f"by {abs(trace1.frame_range[1] - trace2.frame_range[0])} frames while the x,y distance is " \
                          f"{round(point_distance,3)}. Consider joining them."
                if not silent:
                    if index2 == index + 1:
                        if point_distance < 10:
                            print(colored(message, "blue"))
                        else:
                            print(colored(message, "yellow"))
                    else:
                        print(message)
    print(colored(f"Cross_trace analysis done. "
                  f"It took {gethostname()} {round(time() - start_time, 3)} seconds.", "green"))
    print()


# TODO add tests
def merge_overlapping_traces(traces, population_size, allow_force_merge=True, guided=False, input_video=False, silent=False, debug=False, show=False, video_params=False):
    """ Puts traces together such that all the agents but one is being tracked.

        :arg traces: (list): list of traces
        :arg whole_frame_range: [int, int]: frame range of the whole video (with margins)
        :arg population_size: (int): expected number of agents
        :arg allow_force_merge: (bool): iff True force merge is allow
        :arg guided: (bool): if True, user guided version would be run, this stops the whole analysis until a response is given
        :arg input_video: (str or bool): if set, path to the input video
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :arg show: (bool): if True plots are shown
        :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
        :returns: traces: (list): list of concatenated Traces
    """
    print(colored("MERGE OVERLAPPING TRACES", "blue"))
    start_time = time()
    starting_number_of_traces = len(traces)

    whole_frame_range = get_whole_frame_range()
    count_one = [-9]  # indices of traces which have only one occurrence
    number_of_traces = -9
    force_merge = False

    while len(count_one) >= 1 or number_of_traces != len(traces):
        number_of_traces = len(traces)
        # Check whether there are at least 2 traces
        if len(traces) <= 1:
            if len(traces) == 1:
                print(colored("Cannot merge a single trace. Skipping the rest of this analysis.\n", "yellow"))
                return
            if len(traces) == 0:
                print(colored("Cannot merge no trace. Skipping the rest of this analysis.\n", "yellow"))
                return
        # Find overlapping pairs
        dictionary = dictionary_of_m_overlaps_of_n_intervals(2, list(map(lambda x: x.frame_range, traces)), skip_whole_in=True)
        # print("dictionary", dictionary)
        if dictionary == {}:
            print(colored("Cannot merge any trace as there is no partial overlap of two traces.", "yellow"))
            print(colored(f"Returning {len(traces)} traces, {starting_number_of_traces - len(traces)} merged. "
                          f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
            return
        # Flag whether to try another pair of overlapping intervals
        go_next = True
        while go_next:
            if debug:
                print("dictionary", dictionary)
                for trace_index, trace in enumerate(traces):
                    print(f"trace {trace_index} ({trace.trace_id}) of frame range {trace.frame_range}")
                print()
            # Flattened indices of overlapping pairs of traces
            keys = flatten(tuple(dictionary.keys()))

            # Count occurrences of trace indices in overlapping pairs
            counts = {}
            for item in set(keys):
                counts[item] = countOf(keys, item)
            if debug:
                print("keys", keys)
                print("counts", counts)

            # Find traces with single occurrence (within the pairs of overlapping traces)
            count_one = []
            for key in counts.keys():
                # Check there is no interval with 3 or more overlaps - hence cannot easily merge
                # if counts[key] >= 3:
                #     raise Exception("I`m sorry Dave, I`m afraid I cannot do that.")
                if counts[key] == 1:
                    count_one.append(key)
            if debug:
                print("count_one", count_one)

            if len(count_one) == 0:
                print(colored("Cannot merge more traces. No trace with a single overlap found.", "red"))
                # print("dictionary", dictionary)
                for trace_index, trace in enumerate(traces):
                    if debug:
                        print(f"trace {trace_index} of range {trace.frame_range}")
                print(colored(f"Returning {len(traces)} traces, {starting_number_of_traces - len(traces)} merged. "
                              f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
                return

            # Pick the smallest index
            pick_key = min(count_one)

            if debug:
                print("pick_key", pick_key)

            # Find the pair of the smallest index which has a single overlap
            for key in dictionary.keys():
                if pick_key in key:
                    pick_key2 = key
                    if debug:
                        print("pick_key2", pick_key2)
                    break
            trace1 = traces[pick_key2[0]]
            trace2 = traces[pick_key2[1]]
            overlap_range = dictionary[pick_key2]

            global all_overlaps_count
            all_overlaps_count = all_overlaps_count + 1

            # if the picked traces are overlapping in whole range of one of the traces we delete it from the dictionary and move on
            if is_in(trace1.frame_range, trace2.frame_range) or is_in(trace2.frame_range, trace1.frame_range):
                global all_overlaps_deleted
                all_overlaps_deleted = all_overlaps_deleted + 1
                if debug:
                    print("trace1.frame_range", trace1.frame_range)
                    print("trace2.frame_range", trace2.frame_range)

                    print("Will delete ", dictionary[pick_key2])
                    print(dictionary)
                del dictionary[pick_key2]
                if debug:
                    print(dictionary)
                    print()
                go_next = True
                continue

            # Compare the two traces
            if show:
                showw = False
            else:
                showw = None

            # Check the distances of overlap for a big difference
            distances = compare_two_traces(trace1, trace2, pick_key2[0], pick_key2[1], silent=silent, debug=debug, show_all_plots=None if force_merge else showw)

            # Get frame_range
            picked_frame_range = dictionary[pick_key2]

            if allow_force_merge:
                # check whether there is overlap of overlaps
                there_is_overlap = False
                for key in dictionary.keys():
                    if key == pick_key2:
                        continue
                    searched_overlap = dictionary[key]
                    if has_overlap(picked_frame_range, [searched_overlap[0] - get_force_merge_vicinity_distance(), searched_overlap[1] + get_force_merge_vicinity_distance()]):
                        there_is_overlap = True
                        break
                if not there_is_overlap:
                    if not silent:
                        print(colored("USING FORCED OVERLAP MERGE", "magenta"))
                    force_merge = True
            else:
                force_merge = False

            #  Save the id of the merged trace before it is removed
            trace2_id = trace2.trace_id

            if guided:
                pass

            ## COMPUTE THE THRESHOLDS OF TRACES PROXIMITY
            if distances is not None:
                maximal_dist_check = all(list(map(lambda x: x < get_max_step_distance_to_merge_overlapping_traces(), distances)))
                minimal_dist_check = any(list(map(lambda x: x < get_min_step_distance_to_merge_overlapping_traces(), distances)))
            else:
                maximal_dist_check = False
                minimal_dist_check = False

            ## ACTUAL DECISION WHETHER TO MERGE
            if force_merge or (maximal_dist_check and minimal_dist_check):
                # Merge these two traces
                to_merge = True
                print()
                print(colored(f"len distances {len(distances)}", "blue"))
                print(colored(f"distances {distances}", "blue"))
                print(colored(f"max distance {max(distances)}", "blue"))
                print(colored(f"min distance {min(distances)}", "blue"))
                # show_video(input_video, traces=[trace1, trace2], frame_range=margin_range(overlap_range, 15),
                #            video_speed=0.03, wait=True, video_params=video_params)

                merge_two_overlapping_traces(trace1, trace2, pick_key2[0], pick_key2[1], silent=silent, debug=debug)
                #
                # Remove the merged trace
                if debug:
                    # print(colored(f"Will delete trace {trace2_id}.", "blue"))
                    print(colored(f"Will delete trace {pick_key2[1]}({trace2_id}).", "blue"))
                    print()
                traces = delete_indices([pick_key2[1]], traces)
                # Show scatter plot of traces having two traces merged
                go_next = False
            else:
                # NOT Merge these two traces
                go_next = True
                to_merge = False
                force_merge = False

                if minimal_dist_check and not maximal_dist_check:
                    reason = f"single huge point distance ({len(distances)} {round(max(distances))} > {get_max_step_distance_to_merge_overlapping_traces()})"
                elif maximal_dist_check and not minimal_dist_check:
                    reason = f"all big point distance ({len(distances)} {round(min(distances))} > {get_min_step_distance_to_merge_overlapping_traces()})"
                else:
                    reason = f" both, single huge point distance and all big point distance ({len(distances)} {round(max(distances))} > {get_max_step_distance_to_merge_overlapping_traces()} & {round(min(distances))} > {get_min_step_distance_to_merge_overlapping_traces()})"

                # the distance of the traces is greater than the given threshold, we move on
                del dictionary[pick_key2]

            if not silent:
                msg = f"{'' if to_merge else 'NOT '}MERGING THE OVERLAPPING TRACES {'' if to_merge else '(' + reason + ') '}"
                print(colored(msg, "yellow") if to_merge else colored(msg, "red"))
                print()

            if show:
                try:
                    scatter_detection(traces, subtitle=f"after merging overlapping traces {pick_key2[0]} of id {trace1.trace_id} and {pick_key2[1]} of id {trace2_id}.")
                except UnboundLocalError:
                    pass

    print(colored(f"Returning {len(traces)} traces, {starting_number_of_traces - len(traces)} merged. "
                  f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
    return


# TODO add tests
def compare_two_traces(trace1, trace2, trace1_index, trace2_index, silent=False, debug=False, show_all_plots=False):
    """ Compares two traces.

    :arg trace1: (Trace): first trace to be compared
    :arg trace2: (Trace): second trace to be compared
    :arg trace1_index: (int): auxiliary information of index in list of traces of the first trace
    :arg trace2_index: (int): auxiliary information of index in list of traces of the second trace
    :arg silent: (bool): if True minimal output is shown
    :arg debug: (bool): if True extensive output is shown
    :arg show_all_plots: (bool): if True show all the plots
    """
    assert isinstance(trace1, Trace)
    assert isinstance(trace2, Trace)

    if show_all_plots is None:
        show_all_plots = False
        show = False
    else:
        show = True

    if not silent:
        # print(colored(f"COMPARE TWO TRACES - {trace1.trace_id},{trace2.trace_id}", "blue"))
        print(colored(f"COMPARE TWO TRACES - {trace1_index}({trace1.trace_id}),{trace2_index}({trace2.trace_id})", "blue"))
    start_time = time()

    if show_all_plots:
        show_plot_locations([trace1, trace2])
        scatter_detection([trace1, trace2], subtitle=False)

    if not silent:
        print("trace1.frame_range", list(trace1.frame_range))
        print("trace2.frame_range", list(trace2.frame_range))

    overlapping_range = get_overlap(trace1.frame_range, trace2.frame_range)
    # x = range(overlapping_range[0], overlapping_range[1] + 1)
    x = []
    if not silent:
        print("overlapping_range", overlapping_range)

    if overlapping_range is False:
        if not silent:
            # print(colored(f"There is no overlap of trace {trace1.trace_id} and trace {trace2.trace_id}"))
            print(colored(f"There is no overlap of trace {trace1_index} and trace {trace2_index}"))
        return None

    if range_len(overlapping_range) >= range_len(trace1.frame_range):
        raise NotImplemented("Cannot merge nested ranges!")
    if range_len(overlapping_range) >= range_len(trace2.frame_range):
        raise NotImplemented("Cannot merge nested ranges!")

    start_index1 = trace1.frames_list.index(overlapping_range[0])
    end_index1 = trace1.frames_list.index(overlapping_range[1])
    start_index2 = trace2.frames_list.index(overlapping_range[0])
    end_index2 = trace2.frames_list.index(overlapping_range[1])
    if debug:
        print("start_index1", start_index1)
        print("end_index1", end_index1)
        print("start_index2", start_index2)
        print("end_index2", end_index2)
        print()
    if debug:
        print("Showing the overlap frame by frame:")
    inter_index = 0
    distances = []
    first_trace_overlapping_frames = []
    for index in range(start_index1, end_index1+1):
        if debug:
            print(f"frame n. {trace1.frames_list[index]}")
        first_trace_overlapping_frames.append(index)
        if debug:
            print("index1", index)
        try:
            index2 = range(start_index2, end_index2+1)[inter_index]
        except IndexError as err:
            # item = trace1.frames_list[start_index1]
            # for item2 in trace1.frames_list[start_index1+1: end_index1]:
            #     if item2 - item != 1:
            #         print(item)
            #         print(item2)
            #         raise Exception("Dave!")
            #     item = item2
            # item = trace2.frames_list[start_index1]
            # for item2 in trace2.frames_list[start_index2 + 1: end_index2]:
            #     if item2 - item != 1:
            #         raise Exception("Dave!")
            #     item = item2
            print("start_index1", start_index1)
            print("end_index1", end_index1)
            print("start_index2", start_index2)
            print("end_index2", end_index2)
            print("inter_index", inter_index)
            print(str(trace2))
            raise err
        if debug:
            print("index2", index2)
        inter_index = inter_index + 1
        position1 = trace1.locations[index]
        position2 = trace2.locations[index2]
        if debug:
            print("position1", position1)
            print("position2", position2)
        distance = math.dist(position1, position2)
        if debug:
            print("distance of the positions", distance)
            print()
        distances.append(distance)
        x.append(trace1.frames_list[index])

    if show:
        show_overlap_distances(x, trace1, trace2, distances, start_index1, end_index2, silent=silent, debug=debug)

    if debug:
        print(colored(f"Comparing two traces done. It took {gethostname()} {round(time() - start_time, 3)} seconds.", "yellow"))
    if not silent:
        print(colored(f"The overlap of the traces is {end_index2 - start_index2 + 1} frames long and its TOTAL distance is {round(sum(distances), 3)} point wise.", "yellow"))

    return distances
