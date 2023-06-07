import math
from copy import copy
from time import time
from _socket import gethostname
from matplotlib import pyplot as plt
from termcolor import colored
from operator import countOf
from scipy.interpolate import InterpolatedUnivariateSpline

import analyse
from counts import *
from config import *
from fake import get_whole_frame_range
from misc import is_in, delete_indices, dictionary_of_m_overlaps_of_n_intervals, get_overlap, range_len, to_vect, \
    calculate_cosine_similarity, flatten, has_strict_overlap, margin_range, has_dot_overlap
from trace import Trace
from primal_traces_logic import get_traces_from_range
from traces_logic import swap_two_overlapping_traces, merge_two_traces_with_gap, merge_two_overlapping_traces, \
    compute_whole_frame_range, get_video_whole_frame_range, partition_frame_range_by_number_of_traces, \
    reverse_partition_frame_range_by_number_of_traces, check_to_merge_two_overlapping_traces, \
    merge_multiple_pairs_of_overlapping_traces, ask_to_merge_two_traces
from video import show_video
from visualise import scatter_detection, show_plot_locations, show_overlap_distances


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
                    print(colored(f"It seems the traces {trace1_index}({trace1.trace_id}), {trace2_index}({trace2.trace_id}) are swapped on frame {dictionary[overlapping_pair_of_traces][0] + index}", "yellow"))
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


def trim_out_additional_agents_over_long_traces_by_partition_with_build_fallback(traces, population_size, silent=False, debug=False):
    """ Trims out additional appearance of an agent over a longer trace.
        This version is using partition_frame_range_by_number_of_traces.
        Fallbacks the False negative cases of trimming to be solved with iterative build of overlaps of the traces
        within the given partition.

        :arg traces: (list): list of traces
        :arg whole_frame_range: [int, int]: frame range of the whole video (with margins)
        :arg population_size: (int): expected number of agents
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :returns: traces: (list): list of concatenated Traces
    """
    print(colored("TRIM OUT ADDITIONAL AGENTS OVER A LONG TRACES (partition with fallback - iterative build of overlaps)", "blue"))
    start_time = time()

    starting_number_of_traces = len(traces)
    trace_indices_to_delete = []
    ids_of_traces_to_be_deleted = []

    # Compute frame range partition by number of traces for each segment
    interval_to_traces_count = partition_frame_range_by_number_of_traces(traces)
    traces_count_to_intervals = reverse_partition_frame_range_by_number_of_traces(interval_to_traces_count)
    # Obtain number of traces for segment bigger than population_size
    counts_higher_than_pop_size = list(filter(lambda x: x > population_size, list(traces_count_to_intervals.keys())))

    if debug:
        print("interval_to_traces_count", interval_to_traces_count)
        print("traces_count_to_intervals", traces_count_to_intervals)
        print("traces_count_to_intervals keys", traces_count_to_intervals.keys())
        print("counts_higher_than_pop_size", counts_higher_than_pop_size)

    # For each count > population_size
    for count in sorted(counts_higher_than_pop_size):
        intervals = copy(traces_count_to_intervals[count])
        # For each segment
        for interval_index, interval in enumerate(intervals):
            # Obtain trace indices of the traces in the segment
            traces_subset, traces_subset_indices = get_traces_from_range(traces, interval, fully_inside=False, strict=True)

            if debug:
                # print("segment/interval_index", interval_index)
                print("segment/interval", interval)
                print("group_of_traces - indices", traces_subset_indices)

            to_delete_in_this_segment = []
            for trace_index in traces_subset_indices:
                if is_in(traces[trace_index].frame_range, interval):
                    to_delete_in_this_segment.append(trace_index)
                    if debug:
                        print(colored(f"Adding trace n. {trace_index} id {traces[trace_index].trace_id} of frame range {traces[trace_index].frame_range} to be deleted.", "yellow"))
                    # # TODO can delete this after test
                    # if tuple(traces[trace_index].frame_range) != tuple(interval):
                    #     raise Exception(f"A trace is {traces[trace_index].trace_id} of range {traces[trace_index].frame_range} which is supposed to have frame range {interval} has only its subinterval.")

            to_fix = True
            if len(to_delete_in_this_segment) > count-population_size:
                print(f"There are {count} traces present in this segment {interval}, while {len(to_delete_in_this_segment)} whole inside: {to_delete_in_this_segment}. Not deleting any.")
                # TODO add a guided fix
                to_delete_in_this_segment = []
                to_fix = False

            # FIX False negative cases - FALLBACK
            if to_fix and to_delete_in_this_segment == []:
                subset_intervals = list(map(lambda x: x.frame_range, traces_subset))
                dictionary = dictionary_of_m_overlaps_of_n_intervals(population_size + 1, subset_intervals,
                                                                     strict=True, skip_whole_in=False, debug=False)
                to_delete_indices_in_fallback = []
                for overlap in dictionary.values():
                    # if debug:
                    #     print(f"FALLBACK overlap {overlap}")
                    for index, trace in enumerate(traces_subset):
                        # if debug:
                        #     print(f"FALLBACK trace {traces_subset_indices[index]} of frame range {traces[traces_subset_indices[index]].frame_range}")
                        ## Skip trace already added to be deleted
                        if traces_subset_indices[index] in to_delete_indices_in_fallback:
                            continue
                        if is_in(trace.frame_range, overlap):
                            # add this trace to be deleted
                            to_delete_indices_in_fallback.append(traces_subset_indices[index])
                            # to_delete_in_this_cycle.append(traces_subset_indices[index])
                            if debug:
                                print(colored(f"FALLBACK, Adding trace n. {traces_subset_indices[index]} id {traces[traces_subset_indices[index]].trace_id} of frame range {traces[trace_index].frame_range} to be deleted.", "yellow"))

                # to_delete_indices_in_fallback = set(to_delete_indices_in_fallback)
                if len(to_delete_indices_in_fallback) <= count - population_size:
                    ## TODO Delete this after test
                    # for index in to_delete_indices_in_fallback:
                    #     if index in trace_indices_to_delete:
                    #         print(colored("AAARGH", "magenta"))
                    trace_indices_to_delete.extend(to_delete_indices_in_fallback)
                    # del to_delete_indices_in_fallback
                elif debug:
                    print(colored(f"FALLBACK, NOT REMOVING INDICES {to_delete_indices_in_fallback} - TOO MANY OF THE TRACES TO BE DELETED .", "red"))

            trace_indices_to_delete.extend(to_delete_in_this_segment)
            ids_of_traces_to_be_deleted.extend(list(map(lambda x: traces[x].trace_id, to_delete_in_this_segment)))

            ## TODO have a look over here
            # # Fix the structures
            # interval_to_traces_count[interval] = interval_to_traces_count[interval] - 1
            # for index, spam in traces_count_to_intervals[count]:
            #     if spam == interval:
            #         del traces_count_to_intervals[count][index]
            # try:
            #     traces_count_to_intervals[count-1].append(interval)
            # except KeyError:
            #     traces_count_to_intervals[count - 1] = [interval]
            #
            # if debug:
            #     print(colored(interval_to_traces_count, "red"))
            #     print()
            #     print(colored(traces_count_to_intervals, "red"))
            #     print()

    if debug:
        print(colored(f"trace_indices_to_delete {trace_indices_to_delete}", "blue"))
    delete_indices(trace_indices_to_delete, traces)

    print(colored(f"trim_out_additional_agents_over_long_traces using partition with build up overlaps fallback analysis done. It took {gethostname()} {round(time() - start_time, 3)} seconds.", "yellow"))
    print(colored(f"Returning {len(traces)} traces, {len(trace_indices_to_delete)} shorter than in previous iteration. \n", "green"))
    return traces, ids_of_traces_to_be_deleted


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

    merged_trace_indices_to_delete = []
    trace_ids_to_delete = []

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
            if trace_index in merged_trace_indices_to_delete:  # skipping the traces which we are gonna merge
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
                if index3 in merged_trace_indices_to_delete:
                    continue

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
                if index2 in merged_trace_indices_to_delete:
                    continue

                assert isinstance(trace2, Trace)
                if index2 in merged_trace_indices_to_delete:
                    continue
                if trace2.frame_range[0] < step_to:
                    if debug:
                        # print(colored(f"skipping trace {index2} with id {trace2.trace_id} which starts in {trace2.frame_range[0]}", "green"))
                        print(colored(f"skipping trace {index2} which starts in {trace2.frame_range[0]}", "green"))
                    continue

                trace1 = traces[index_to_go]

                if trace1.trace_id == 0 or trace2.trace_id == 0:
                    pass

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
                except Exception:
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
                        if has_strict_overlap(gap_range, [trace.frame_range[0] - get_force_merge_vicinity_distance(), trace.frame_range[1] + get_force_merge_vicinity_distance()]):
                            force_merge = False
                            break
                    if force_merge and not silent:
                        print(colored("USING FORCED GAP MERGE", "magenta"))
                else:
                    force_merge = False

                const = 1.2

                if not force_merge:
                    # the gap is wider than max_trace_gap (50 set as default)
                    if trace2.frame_range[0] - step_to > get_max_trace_gap():
                        to_merge = False
                        reason = f"gap too long (> {get_max_trace_gap()})"
                    # length of the second trace is longer than a given number (100 set as default)
                    if force_merge and trace2.frame_range_len < get_min_trace_length_to_merge():
                        to_merge = False
                        reason = f"2nd trace too short (< {get_min_trace_length_to_merge()})"
                    # CHECK FOR DISTANCE OF TRACES IN X,Y
                    # if the distance of traces in frames is high
                    if to_merge:

                        if trace1.trace_id == 0 or trace2.trace_id == 0:
                            pass

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

                ## Check for FalseNegatives
                if trace2.frame_range[0] - step_to < get_max_trace_gap() * const and trace2.frame_range_len > get_min_trace_length_to_merge() / const:
                    print(f"max_trace_gap: {trace2.frame_range[0] - step_to} < {get_max_trace_gap() * const}")
                    print(
                        f"min_trace_length_to_merge: {trace2.frame_range_len} > {get_min_trace_length_to_merge() / const}")
                    to_merge, spam = ask_to_merge_two_traces(traces, [trace1, trace2], analyse.video_file,
                                                             video_params=analyse.video_params, silent=silent, gaping=True, trace_ids_to_skip=trace_ids_to_delete)

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
                    ### Check for FalsePositives
                    to_merge_by_user = None

                    # to_merge_by_user = ask_to_merge_two_traces(traces, [trace1, trace2], analyse.video_file, video_params=analyse.video_params, silent=silent, gaping=True)
                    if to_merge_by_user is False:
                        break

                    # print(colored(f"Merging gaping traces {index}({trace1.trace_id}) and {index2}({trace2.trace_id})", "yellow"))
                    trace = merge_two_traces_with_gap(trace1, trace2, interpolate_gap=to_merge_by_user)
                    if debug:
                        print(trace)

                    print(colored(f"adding trace index {index2} with id {trace2.trace_id} to be deleted", "magenta"))
                    merged_trace_indices_to_delete.append(index2)
                    trace_ids_to_delete.append(trace2.trace_id)
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
        print(f"Will delete the following traces as we have merged them: {merged_trace_indices_to_delete}")
    delete_indices(merged_trace_indices_to_delete, traces)

    print(colored(f"GAPING TRACES analysis done. It took {gethostname()} {round(time() - start_time, 3)} seconds.", "yellow"))
    print(colored(f"Returning {len(traces)} traces, {len(merged_trace_indices_to_delete)} shorter than in previous iteration.", "green"))
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


def merge_alone_overlapping_traces_by_partition(traces, shift=False, silent=False, debug=False, do_count=False, input_video=False, video_params=False):
    """ Merges traces which have the only overlap at given time
        # Puts traces together such that all the agents but two are being tracked.

        :arg traces: (list): list of traces
        :arg shift: (False ir int): if False, no shift is used, else shift upto the given value is used to compare the traces
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :arg do_count: (bool): flag whether to count the numbers of events occurring
        :arg input_video: (str or bool): if set, path to the input video
        :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
        :returns: traces: (list): list of concatenated Traces
    """
    print(colored("MERGE ALONE OVERLAPPING TRACES", "blue"))
    start_time = time()

    starting_number_of_traces = len(traces)
    pairs_of_traces_indices_to_merge = []
    ids_of_traces_to_be_merged = []

    if do_count:
        set_single_run_seen_overlaps(0)
        set_single_run_allowed_overlaps_count(0)
        set_single_run_seen_overlaps_deleted(0)

    # Compute frame range partition by number of traces for each segment
    interval_to_traces_count = partition_frame_range_by_number_of_traces(traces)
    traces_count_to_intervals = reverse_partition_frame_range_by_number_of_traces(interval_to_traces_count)

    try:
        set_single_run_seen_overlaps(len(traces_count_to_intervals[2]))
    except KeyError:
        set_single_run_seen_overlaps(0)

    try:
        intervals = copy(traces_count_to_intervals[2])
    except KeyError:
        if debug:
            print("interval_to_traces_count", interval_to_traces_count)
            print("traces_count_to_intervals", traces_count_to_intervals)
            print("traces_count_to_intervals keys", traces_count_to_intervals.keys())
        print(colored(f"There is no segment with two traces, skipping the analysis."
                      f" It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
        return [], []

    if debug:
        print("interval_to_traces_count", interval_to_traces_count)
        print("traces_count_to_intervals", traces_count_to_intervals)
        print("traces_count_to_intervals keys", traces_count_to_intervals.keys())

        print("intervals with exactly two overlapping traces", traces_count_to_intervals[2])
        # print("counts_equal_two", counts_equal_two)

    for interval_index, interval in enumerate(intervals):
        # Obtain trace and trace indices of the traces in the segment
        traces_subset, traces_subset_indices = get_traces_from_range(traces, interval, fully_inside=False, strict=True)

        if debug:
            # print("segment/interval_index", interval_index)
            print("segment/interval", interval)
            print("group_of_traces - indices", traces_subset_indices)
            for trace in traces_subset:
                print(trace)

        assert len(traces_subset) == 2
        assert len(traces_subset_indices) == 2

        # Get names
        trace1 = traces_subset[0]
        trace2 = traces_subset[1]
        trace1_index = traces_subset_indices[0]
        trace2_index = traces_subset_indices[1]

        # Get the overlap
        overlap_range = get_overlap(trace1.frame_range, trace2.frame_range)

        to_merge, use_shift = check_to_merge_two_overlapping_traces(traces, trace1, trace2, trace1_index, trace2_index,
                                                                    overlap_range, shift=shift, show=False, silent=silent,
                                                                    debug=debug, input_video=input_video, video_params=video_params)

        if to_merge is None:
            # One trace is inside of another,
            set_single_run_seen_overlaps_deleted(get_single_run_seen_overlaps_deleted() + 1)
            continue
        elif to_merge is True:
            pairs_of_traces_indices_to_merge.append((trace1_index, trace2_index))
            ids_of_traces_to_be_merged.append((trace1.trace_id, trace2.trace_id))
        else:
            pass

    # ACTUALLY MERGE THE TRACES
    set_single_run_allowed_overlaps_count(len(pairs_of_traces_indices_to_merge))
    merge_multiple_pairs_of_overlapping_traces(traces, pairs_of_traces_indices_to_merge, silent=silent, debug=debug)

    print(colored(f"Returning {len(traces)} traces, {starting_number_of_traces - len(traces)} merged. "
                  f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
    return pairs_of_traces_indices_to_merge, ids_of_traces_to_be_merged


def merge_alone_overlapping_traces(traces, shift=False, allow_force_merge=True, guided=False, input_video=False, silent=False, debug=False, show=False, video_params=False, do_count=True, is_first_call=None):
    """ Merges traces with only a single overlap.
        # Puts traces together such that all the agents but one is being tracked.

        :arg traces: (list): list of traces
        :arg shift: (False ir int): if False, no shift is used, else shift upto the given value is used to compare the traces
        :arg whole_frame_range: [int, int]: frame range of the whole video (with margins)
        :arg allow_force_merge: (bool): iff True force merge is allow
        :arg guided: (bool): if True, user guided version would be run, this stops the whole analysis until a response is given
        :arg input_video: (str or bool): if set, path to the input video
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :arg show: (bool): if True plots are shown
        :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
        :arg do_count: (bool): flag whether to count the numbers of events occurring
        :returns: traces: (list): list of concatenated Traces
    """
    print(colored("MERGE OVERLAPPING TRACES - using build", "blue"))
    # Initiation
    start_time = time()
    starting_number_of_traces = len(traces)

    # with open("../auxiliary/shifted_traces_with_lower_distance.txt", "a") as file:
    #     file.write(f"csv_file_path; overlap_range; distances; shifted_distances; shift; distance proportion; \n")

    # whole_frame_range = get_whole_frame_range()
    count_one = [-9]  # indices of traces which have only one occurrence
    number_of_traces = -9

    merge_pairs = []

    # Do the counting
    seen_pairs = set()
    if is_first_call:
        set_single_run_overlaps_count(0)
    if do_count:
        set_single_run_seen_overlaps(0)
        set_single_run_allowed_overlaps_count(0)
        set_single_run_seen_overlaps_deleted(0)

    # Go while there is what to merge
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
        # Find all overlapping pairs
        dictionary = dictionary_of_m_overlaps_of_n_intervals(2, list(map(lambda x: x.frame_range, traces)), strict=True, skip_whole_in=True)

        ## Count the overlapping pairs
        if is_first_call:
            is_first_call = False
            set_single_run_overlaps_count(len(list(dictionary.keys())))

        # print("dictionary", dictionary)
        if dictionary == {}:
            print(colored("Cannot merge any trace as there is no partial overlap of two traces.", "yellow"))
            print(colored(f"Returning {len(traces)} traces, {starting_number_of_traces - len(traces)} merged. "
                          f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
            break

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

            # Find indices of traces with single occurrence (within the pairs of overlapping traces)
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
                go_next = False
                break

            # while count_one:
            # Pick the smallest index
            picked_trace_index = min(count_one)
            if debug:
                print("picked_trace_index", picked_trace_index)

            # Find the first pair having the picked key
            for key in dictionary.keys():
                if picked_trace_index in key:
                    picked_key = key
                    if debug:
                        print("pick_key2", picked_key)
                    break

            trace1 = traces[picked_key[0]]
            trace2 = traces[picked_key[1]]
            trace1_index = picked_key[0]
            trace2_index = picked_key[1]

            overlap_range = dictionary[picked_key]

            seen_pairs.add(picked_key)
            to_merge, use_shift = check_to_merge_two_overlapping_traces(traces, trace1, trace2, trace1_index, trace2_index,
                                                                        overlap_range, shift=shift, show=False,
                                                                        silent=silent, debug=debug, input_video=input_video,
                                                                        video_params=video_params)
            if allow_force_merge:
                force_merge = False
                # Check whether there is overlap of overlaps
                there_is_overlap = False
                for key in dictionary.keys():
                    if key == picked_key:
                        continue
                    searched_overlap = dictionary[key]
                    if has_strict_overlap(overlap_range, [searched_overlap[0] - get_force_merge_vicinity_distance(), searched_overlap[1] + get_force_merge_vicinity_distance()]):
                        there_is_overlap = True
                        break
                if not there_is_overlap:
                    if not silent:
                        print(colored("USING FORCED OVERLAP MERGE", "magenta"))
                    force_merge = True
            else:
                force_merge = False

            ## ACTUAL DECISION WHETHER TO MERGE
            if force_merge or to_merge:
                # Merge these two traces
                merge_two_overlapping_traces(trace1, trace2, trace1_index, trace2_index, silent=silent, debug=debug)

                # Count this
                set_single_run_allowed_overlaps_count(get_single_run_allowed_overlaps_count() + 1)

                # Remove the merged trace
                if debug:
                    # print(colored(f"Will delete trace {trace2_id}.", "blue"))
                    print(colored(f"Will delete trace {picked_key[1]}({trace2.trace_id}).", "blue"))
                    print()
                delete_indices([picked_key[1]], traces)
                go_next = False
            else:
                # NOT Merge these two traces
                go_next = True
                del dictionary[picked_key]

            if show:
                try:
                    scatter_detection(traces, subtitle=f"after merging overlapping traces {picked_key[0]} of id {trace1.trace_id} and {picked_key[1]} of id {trace2.trace_id}.")
                except UnboundLocalError:
                    pass

        do_count = False

    print(colored(f"Returning {len(traces)} traces, {starting_number_of_traces - len(traces)} merged. "
                  f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))

    set_single_run_seen_overlaps(len(seen_pairs))
    return


def merge_overlapping_traces_brutto(traces, shift=False, allow_force_merge=True, guided=False, input_video=False, silent=False, debug=False, show=False, video_params=False, do_count=True, is_first_call=None, alg=""):
    """ Merges traces with only a single overlap.
        # Puts traces together such that all the agents but one is being tracked.

        :arg traces: (list): list of traces
        :arg shift: (False ir int): if False, no shift is used, else shift upto the given value is used to compare the traces
        :arg whole_frame_range: [int, int]: frame range of the whole video (with margins)
        :arg alone: (bool): if alone, only traces with a single overlap will be taken into account
        :arg allow_force_merge: (bool): iff True force merge is allow
        :arg guided: (bool): if True, user guided version would be run, this stops the whole analysis until a response is given
        :arg input_video: (str or bool): if set, path to the input video
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :arg show: (bool): if True plots are shown
        :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
        :arg do_count: (bool): flag whether to count the numbers of events occurring
        :returns: traces: (list): list of concatenated Traces
    """
    print(colored("MERGE OVERLAPPING TRACES BRUTTO - using build", "blue"))
    start_time = time()
    starting_number_of_traces = len(traces)

    # with open("../auxiliary/shifted_traces_with_lower_distance.txt", "a") as file:
    #     file.write(f"csv_file_path; overlap_range; distances; shifted_distances; shift; distance proportion; \n")

    merge_pairs = []

    # Do the counting
    seen_pairs = set()
    if is_first_call:
        if alg == "mixed":
            set_this_file_overlaps_count(get_single_run_seen_overlaps())
        else:
            set_single_run_overlaps_count(0)
    if do_count is True:
        if alg != "mixed":
            set_single_run_seen_overlaps(0)
        set_single_run_allowed_overlaps_count(0)
        set_single_run_seen_overlaps_deleted(0)

    # Check whether there are at least 2 traces
    if len(traces) <= 1:
        if len(traces) == 1:
            print(colored("Cannot merge a single trace. Skipping the rest of this analysis.\n", "yellow"))
            return
        if len(traces) == 0:
            print(colored("Cannot merge no trace. Skipping the rest of this analysis.\n", "yellow"))
            return
    # Find all overlapping pairs
    dictionary = dictionary_of_m_overlaps_of_n_intervals(2, list(map(lambda x: x.frame_range, traces)), strict=True, skip_whole_in=True)
    if debug:
        print("dictionary", dictionary)

    ## Count the overlapping pairs
    if is_first_call:
        if alg != "mixed":
            set_single_run_overlaps_count(len(list(dictionary.keys())))

    if dictionary == {}:
        print(colored("Cannot merge any trace as there is no partial overlap of two traces.", "yellow"))
        print(colored(f"Returning {len(traces)} traces, {starting_number_of_traces - len(traces)} merged. "
                      f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
        return

    # Flag whether to try another pair of overlapping intervals
    for picked_key in dictionary.keys():
        trace1 = traces[picked_key[0]]
        trace2 = traces[picked_key[1]]
        trace1_index = picked_key[0]
        trace2_index = picked_key[1]

        overlap_range = tuple(dictionary[picked_key])

        seen_pairs.add(picked_key)
        ## ACTUAL DECISION WHETHER TO MERGE
        to_merge, use_shift = check_to_merge_two_overlapping_traces(traces, trace1, trace2, trace1_index, trace2_index,
                                                                    overlap_range, shift=shift, show=False,
                                                                    silent=silent, debug=debug, input_video=input_video,
                                                                    video_params=video_params)
        if allow_force_merge:
            force_merge = False
            # Check whether there is overlap of overlaps
            there_is_overlap = False
            for key in dictionary.keys():
                if key == picked_key:
                    continue
                searched_overlap = dictionary[key]
                if has_strict_overlap(overlap_range, [searched_overlap[0] - get_force_merge_vicinity_distance(), searched_overlap[1] + get_force_merge_vicinity_distance()]):
                    there_is_overlap = True
                    break
            if not there_is_overlap:
                if not silent:
                    print(colored("USING FORCED OVERLAP MERGE", "magenta"))
                force_merge = True
        else:
            force_merge = False

        # Manage the merge event
        if force_merge or to_merge:
            # Merge these two traces later
            merge_pairs.append((trace1_index, trace2_index))

        if show:
            try:
                scatter_detection(traces, subtitle=f"after merging overlapping traces {picked_key[0]} of id {trace1.trace_id} and {picked_key[1]} of id {trace2.trace_id}.")
            except UnboundLocalError:
                pass

    ## MANAGE THE OVERLAPPING PAIRS
    pairs_to_skip = set()
    for index, pair in enumerate(merge_pairs):
        complementary_pairs = []
        for other_index, other_pair in enumerate(merge_pairs):
            if index == other_index:
                continue
            if other_pair[0] in pair:
                complementary_pairs.append(other_pair)
            if other_pair[1] in pair:
                complementary_pairs.append(other_pair)

        for complementary_pair in complementary_pairs:
            # if there is an overlap of all three traces
            if dictionary_of_m_overlaps_of_n_intervals(3, list(map(lambda x: x.frame_range, list(
                    {traces[pair[0]], traces[pair[1]], traces[complementary_pair[0]], traces[complementary_pair[1]]}))), strict=True, skip_whole_in=True):
                pairs_to_skip.add(pair)
                pairs_to_skip.add(complementary_pair)
                if debug:
                    print(f"getting rid of these pairs: {pair}, {complementary_pair}")
            # if complementary_pair[0] in pair:
            #     if pair[0] == complementary_pair[0]:
            #         # ca cb
            #         if has_dot_overlap(traces[pair[1]].frame_range, traces[complementary_pair[1]].frame_range, strict=True):
            #             pairs_to_skip.add(pair)
            #             pairs_to_skip.add(complementary_pair)
            #             # raise Exception("a triplet of overlapping traces")
            #     else:
            #         # ac cb
            #         if has_dot_overlap(traces[pair[0]].frame_range, traces[complementary_pair[1]].frame_range, strict=True):
            #             pairs_to_skip.add(pair)
            #             pairs_to_skip.add(complementary_pair)
            #             # raise Exception("a triplet of overlapping traces")
            # else:
            #     # ca bc
            #     if pair[0] == complementary_pair[1]:
            #         if has_dot_overlap(traces[pair[1]].frame_range, traces[complementary_pair[0]].frame_range, strict=True):
            #             pairs_to_skip.add(pair)
            #             pairs_to_skip.add(complementary_pair)
            #             # raise Exception("a triplet of overlapping traces")
            #     else:
            #         # ac bc
            #         if has_dot_overlap(traces[pair[0]].frame_range, traces[complementary_pair[0]].frame_range, strict=True):
            #             pairs_to_skip.add(pair)
            #             pairs_to_skip.add(complementary_pair)
            #             # raise Exception("a triplet of overlapping traces")
    
    # Get rid of the overlapping triplets
    merge_cut_pairs = list(filter(lambda x: x not in pairs_to_skip, merge_pairs))
    if debug:
        print(f"getting rid of these pairs: {pairs_to_skip}")

    # Actually merge the pure pairs
    merge_multiple_pairs_of_overlapping_traces(traces, merge_cut_pairs, silent=silent, debug=debug)

    # Do the counting
    set_single_run_allowed_overlaps_count(len(merge_cut_pairs))
    set_single_run_seen_overlaps_deleted(len(merge_pairs) - len(merge_cut_pairs))
    if is_first_call and alg == "mixed":
        set_single_run_seen_overlaps(get_single_run_seen_overlaps() + len(seen_pairs))
    else:
        set_single_run_seen_overlaps(len(seen_pairs))

    print(colored(f"brut Returning {len(traces)} traces, {starting_number_of_traces - len(traces)} merged. "
                  f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
    return
