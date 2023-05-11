import copy
import math
import sys
from _socket import gethostname
from pathlib import Path
from time import time

import numpy as np
from termcolor import colored
from ast import literal_eval as make_tuple

from config import get_max_trace_gap_to_interpolate_distance, get_max_step_distance_to_merge_overlapping_traces, \
    get_min_step_distance_to_merge_overlapping_traces, get_max_overlap_len_to_merge_traces, \
    get_minimal_movement_per_frame
from dave_io import load_decisions, save_decisions
from misc import get_gap, is_in, has_overlap, is_before, merge_dictionary, get_overlap, has_dot_overlap, margin_range, \
    delete_indices, range_len
from primal_traces_logic import get_traces_from_range
from trace import Trace
from video import show_video
from visualise import show_overlap_distances, show_plot_locations, scatter_detection


# TODO add tests
def compare_two_traces(trace1, trace2, trace1_index, trace2_index, allow_inside=False, silent=False, debug=False, show_all_plots=None):
    """ Compares two traces.

    :arg trace1: (Trace): first trace to be compared
    :arg trace2: (Trace): second trace to be compared
    :arg trace1_index: (int): auxiliary information of index in list of traces of the first trace
    :arg trace2_index: (int): auxiliary information of index in list of traces of the second trace
    :arg silent: (bool): if True minimal output is shown
    :arg debug: (bool): if True extensive output is shown
    :arg show_all_plots: (bool or None): if True show all the plots
    """
    assert isinstance(trace1, Trace)
    assert isinstance(trace2, Trace)

    if show_all_plots is None:
        show_all_plots = False
        show = False
    else:
        show = True

    if not silent:
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

    if not allow_inside:
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


## TODO maybe merge with compare_two_traces
def compare_two_traces_with_shift(trace1, trace2, trace1_index, trace2_index, shift_up_to=10, allow_inside=False, silent=False, debug=False, show_all_plots=None):
    """ Compares two traces with a shift.

    :arg trace1: (Trace): first trace to be compared
    :arg trace2: (Trace): second trace to be compared
    :arg trace1_index: (int): auxiliary information of index in list of traces of the first trace
    :arg trace2_index: (int): auxiliary information of index in list of traces of the second trace
    :arg shift_up_to: (int): maximal shift value
    :arg allow_inside: (bool): whether to compare nested traces
    :arg silent: (bool): if True minimal output is shown
    :arg debug: (bool): if True extensive output is shown
    :arg show_all_plots: (bool or None): if True show all the plots
    """
    assert isinstance(trace1, Trace)
    assert isinstance(trace2, Trace)

    if show_all_plots is None:
        show_all_plots = False
        show = False
    else:
        show = True

    if not silent:
        print(colored(f"COMPARE TWO TRACES WITH SHIFT - {trace1_index}({trace1.trace_id}),{trace2_index}({trace2.trace_id})", "blue"))
    start_time = time()

    if show_all_plots:
        show_plot_locations([trace1, trace2])
        scatter_detection([trace1, trace2], subtitle=False)

    if not silent:
        print("trace1.frame_range", list(trace1.frame_range))
        print("trace2.frame_range", list(trace2.frame_range))

    overlapping_range = get_overlap(trace1.frame_range, trace2.frame_range)

    if not silent:
        print("overlapping_range", overlapping_range)

    if overlapping_range is False:
        if not silent:
            # print(colored(f"There is no overlap of trace {trace1.trace_id} and trace {trace2.trace_id}"))
            print(colored(f"There is no overlap of trace {trace1_index} and trace {trace2_index}"))
        return None

    if not allow_inside:
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

    distances = []
    first_trace_overlapping_frames = []
    for shift in range(0, shift_up_to):
        # Check whether the shift is within the ranges of the trace1
        if shift > 0 and None in distances[-1]:
            break

        inter_index = 0
        # x = range(overlapping_range[0], overlapping_range[1] + 1)
        x = []
        distances.append([])
        for index in range(start_index1, end_index1+1):
            if debug:
                print(f"trace 1 frame n. {trace1.frames_list[index-shift]}")
                print(f"trace 2 frame n. {trace1.frames_list[index]}")
            first_trace_overlapping_frames.append(index)
            if debug:
                print("index1", index)
            try:
                index2 = range(start_index2, end_index2+1)[inter_index]
            except IndexError as err:
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
            try:
                assert index - shift >= 0
                position1 = trace1.locations[index - shift]
                position2 = trace2.locations[index2]
                if debug:
                    print("shift", shift)
                    print("position1", position1)
                    print("position2", position2)
                    print()
                distance = math.dist(position1, position2)
            except AssertionError:
                distance = None

            if debug:
                print("distance of the positions", distance)
                print()
            distances[shift].append(distance)
            x.append(trace1.frames_list[index])
            if distance is None:
                break

        if show:
            show_overlap_distances(x, trace1, trace2, distances, start_index1, end_index2, silent=silent, debug=debug)

    min_dist_shift = 0
    min_dist = sum(distances[0])/len(distances[0])
    for shift_index, distancess in enumerate(distances):
        if None in distancess:
            pass
        else:
            curr_dist = sum(distances[shift_index])/len(distances[shift_index])
            if curr_dist < min_dist:
                min_dist_shift = shift_index
                min_dist = curr_dist

    if debug:
        print(colored(f"Comparing two traces done. It took {gethostname()} {round(time() - start_time, 3)} seconds.", "yellow"))
    if not silent:
        print(colored(f"The overlap of the traces is {end_index2 - start_index2 + 1} frames long and its TOTAL distance is {round(sum(distances[0]), 3)} point wise.", "yellow"))

    return distances[0], distances[min_dist_shift], min_dist_shift


def partition_frame_range_by_number_of_traces(traces):
    """ Partitions the frame range into intervals based on number of traces in this interval
    Returns a map interval -> number of traces in the interval

    :arg traces: (list): list of Traces
    """
    # Get the starts and ends:
    starts = []
    ends = []
    for trace in traces:
        starts.append(trace.frame_range[0])
        ends.append(trace.frame_range[1])

    # Sort them
    starts = sorted(starts)
    # print(starts)
    ends = sorted(ends)
    # print(ends)

    # Initialise
    current_left = 0
    current_count = 0
    interval_to_traces_count = {}

    # Manage beginning:
    if starts[0] != 0:
        interval_to_traces_count[(0, starts[0])] = 0
        current_left = starts[0]

    # while there is a start or end
    # while len(starts) + len(ends) > 0:
    while len(ends) > 1:
        plus = 0
        try:
            while starts[0] == current_left:
                del starts[0]
                plus = plus + 1
        except IndexError:
            pass

        minus = 0
        try:
            while ends[0] == current_left:
                del ends[0]
                minus = minus + 1
        except IndexError:
            pass

        try:
            start = starts[0]
        except IndexError:
            start = sys.maxsize

        try:
            end = ends[0]
        except IndexError:
            end = sys.maxsize

        right = min(start, end)

        interval_to_traces_count[(current_left, right)] = current_count + plus - minus
        current_count = current_count + plus - minus

        # print(current_left)
        current_left = right

    return interval_to_traces_count


def reverse_partition_frame_range_by_number_of_traces(traces_or_interval_to_count):
    """ Returns a map number -> intervals with given number of traces inside this interval

        :arg traces_or_interval_to_count: (dict or list): interval_to_count OR list of Traces
    """
    if isinstance(traces_or_interval_to_count, list):
        interval_to_count = partition_frame_range_by_number_of_traces(traces_or_interval_to_count)
    else:
        interval_to_count = traces_or_interval_to_count

    assert isinstance(interval_to_count, dict)
    traces_count_to_intervals = {}

    for key in list(interval_to_count.keys()):
        value = interval_to_count[key]
        if value in traces_count_to_intervals.keys():
            traces_count_to_intervals[value].append(key)
        else:
            traces_count_to_intervals[value] = [key]

    # print(count_to_intervals)
    return traces_count_to_intervals


def merge_two_traces_with_gap(trace1: Trace, trace2: Trace, silent=False, debug=False):
    """ Puts two traces together.

    :arg trace1: (Trace): a Trace to be merged with the following trace
    :arg trace2: (Trace): a Trace to be merged with the following trace
    :arg silent: (bool): if True minimal output is shown
    :arg debug: (bool): if True extensive output is shown

    :returns: trace1: (Trace): merged trace of two given traces
    """
    # Check
    assert isinstance(trace1, Trace)
    assert isinstance(trace2, Trace)

    if debug:
        print("trace1.trace_id", trace1.trace_id)
        print("trace2.trace_id", trace2.trace_id)

    if has_overlap(trace1.frame_range, trace2.frame_range):
        raise Exception("The two traces have an overlap. We cannot merge them. Try other merge function.")

    ## MERGE
    # set trace id
    trace1.trace_id = min(trace1.trace_id, trace2.trace_id)

    # swapping traces if trace2 is before trace1
    if is_before(trace2.frame_range, trace1.frame_range):
        spam = trace2
        trace2 = trace1
        trace1 = spam
        del spam

    ## Calculate the gap
    # gap range is the range of the gap not including the border points of traces
    gap_range = [trace1.frame_range[-1]+1, trace2.frame_range[0]-1]

    # gap population_size in frames
    frame_gap_size = trace2.frames_list[0] - trace1.frames_list[-1] - 1
    # gap population_size in xy (last and first point)
    merge_step = math.dist(trace1.locations[-1], trace2.locations[0])

    # trace len is sum of both plus the gap
    trace1.trace_length = trace1.trace_length + merge_step + trace2.trace_length

    # list of frame, not to be confused with number_of_frames_tracked is list of all frames including the gap
    for frame in range(gap_range[0], gap_range[1]+1):
        trace1.frames_list.append(frame)
        # add the gap to the gap frames
        trace1.gap_frames.append(frame)
    trace1.frames_list.extend(trace2.frames_list)

    # Based on the gap population_size
    if frame_gap_size <= get_max_trace_gap_to_interpolate_distance():
        # set a point of location of the gap as linear interpolation of two bordering points
        if debug:
            print("frame_gap_size", frame_gap_size)
            print(trace1.locations[-1], trace2.locations[0])
        in_middle_points = np.linspace(trace1.locations[-1], trace2.locations[0], num=frame_gap_size+1, endpoint=False)
        # in_middle_points = list(map(lambda x: [int(x[0]), int(x[1])], in_middle_points))
        # cutting the first point and changing to float
        in_middle_points = list(map(lambda x: [float(x[0]), float(x[1])], in_middle_points))[1:]
        trace1.locations.extend(in_middle_points)

    else:
        in_middle_point = [-1, -1]

        # fill the gap location as the chosen point
        for frame in range(frame_gap_size):
            trace1.locations.append(in_middle_point)

    ## DEPRECATED
    # set a point of location of the gap as a point in the middle between the border points
    # in_middle_point = [abs(trace2.locations[0][0] + trace1.locations[-1][0])/2, abs(trace2.locations[0][1] + trace1.locations[-1][1])/2]
    # # fill the gap location as the chosen point
    # for frame in range(frame_gap_size - 1):
    #     trace1.locations.append(in_middle_point)

    # extend the locations with locations of trace2
    trace1.locations.extend(trace2.locations)

    # frame range is simply leftmost and rightmost frame of the two traces, remember they are sorted
    trace1.frame_range = [trace1.frame_range[0], trace2.frame_range[1]]

    # frame_range_len is the len from new boundary to another
    trace1.frame_range_len = int(float(trace1.frame_range[-1]) - float(trace1.frame_range[0])) + 1

    # print("trace1.max_step_len", trace1.max_step_len)
    # print("trace2.max_step_len", trace2.max_step_len)

    if trace1.max_step_len < trace2.max_step_len:
        trace1.max_step_len_step_index = trace2.max_step_len_step_index
        trace1.max_step_len_line = trace2.max_step_len_line
        trace1.max_step_len_frame_number = trace2.max_step_len_frame_number

    trace1.max_step_len = max(trace1.max_step_len, trace2.max_step_len)

    # TODO fix this by adding the the steps of the gap
    trace1.trace_lengths = merge_dictionary(trace1.trace_lengths, trace2.trace_lengths)

    # print(trace1.trace_lengths)
    if round(merge_step, 6) in trace1.trace_lengths.keys():
        trace1.trace_lengths[round(merge_step, 6)] = trace1.trace_lengths[round(merge_step, 6)] + 1
    else:
        trace1.trace_lengths[round(merge_step, 6)] = 1
    # print(trace1.trace_lengths)

    return trace1


def check_to_merge_two_overlapping_traces(traces, trace1: Trace, trace2: Trace, trace1_index, trace2_index, overlap_range,
                                          shift=False, show=False, silent=False, debug=False, input_video=False, video_params=False):
    """ Check whether to merge given two overlapping traces or not.

    :arg traces: (list): list of traces
    :arg trace1: (Trace): a Trace to be merged with the following trace
    :arg trace2: (Trace): a Trace to be merged with the following trace
    :arg trace1_index: (int): auxiliary information of index in list of traces of the first trace
    :arg trace2_index: (int): auxiliary information of index in list of traces of the second
    :arg overlap_range: (pair of ints): range of the overlap
    :arg shift: (False ir int): if False, no shift is used, else shift upto the given value is used to compare the traces
    :arg show: (bool): flag whether to show the plots and video of the overlap
    :arg silent: (bool): if True minimal output is shown
    :arg debug: (bool): if True extensive output is shown
    :arg input_video: (str or bool): if set, path to the input video
    :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
    :returns: to _merge: (bool): flag whether to merge the traces or not
    """

    if is_in(trace1.frame_range, trace2.frame_range) or is_in(trace2.frame_range, trace1.frame_range):
        if debug:
            print(colored(f"Traces {trace1_index}({trace1.trace_id}) and {trace2_index}({trace2.trace_id}) are inside one another. NOT MERGING.", "yellow"))
        return None, None

    # Check the distances of overlap for a big difference
    if shift is False or shift == 0:
        distances = compare_two_traces(trace1, trace2, trace1_index, trace2_index, silent=silent, debug=debug, show_all_plots=None)
        shift = None
    else:
        not_shifted_distances, distances, shift = compare_two_traces_with_shift(trace1, trace2, trace1_index, trace2_index, shift_up_to=shift, silent=silent, debug=debug, show_all_plots=None)

    maximal_dist_check = all(list(map(lambda x: x < get_max_step_distance_to_merge_overlapping_traces(), distances)))
    # old_maximal_dist_check = all(list(map(lambda x: x < 120, distances)))
    minimal_dist_check = any(list(map(lambda x: x < get_min_step_distance_to_merge_overlapping_traces(), distances)))
    # old_minimal_dist_check = any(list(map(lambda x: x < 50, distances)))
    overlap_len_check = len(distances) <= get_max_overlap_len_to_merge_traces()

    trace1_avg_distance_per_frame_in_overlap = trace1.calculate_path_len_from_range(overlap_range) / len(distances)
    trace2_avg_distance_per_frame_in_overlap = trace2.calculate_path_len_from_range(overlap_range) / len(distances)

    overlap_movement_check = trace1_avg_distance_per_frame_in_overlap > get_minimal_movement_per_frame() and \
                             trace2_avg_distance_per_frame_in_overlap > get_minimal_movement_per_frame()

    # TO MERGE CHECK
    if maximal_dist_check and minimal_dist_check and overlap_len_check and overlap_movement_check:
        # if shift:
        #     maximal_dist_check = all(
        #         list(map(lambda x: x < get_max_step_distance_to_merge_overlapping_traces(), not_shifted_distances)))
        #     minimal_dist_check = any(
        #         list(map(lambda x: x < get_min_step_distance_to_merge_overlapping_traces(), not_shifted_distances)))
        #
        # if shift and sum(distances) < sum(not_shifted_distances) and not (maximal_dist_check and minimal_dist_check):

        print()
        # print(overlap_range)
        # print(trace1.frames_list)
        # print(trace1.locations)
        # print(trace1.get_locations_from_frame_range(overlap_range))

        from analyse import curr_csv_file_path
        print(f"{Path(curr_csv_file_path).stem} {len(distances)}, {math.trunc(max(distances))}, {math.trunc(min(distances))}")

        print(colored(f"len distances {len(distances)}", "blue"))
        print(colored(f"distances {distances[25:]}", "blue"))
        print(colored(f"max distance {max(distances)}", "blue"))
        print(colored(f"min distance {min(distances)}", "blue"))
        print(colored(f"path lens per frame {trace1.calculate_path_len_from_range(overlap_range) / len(distances)},"
                      f" {trace2.calculate_path_len_from_range(overlap_range) / len(distances)}", "blue"))

        if shift:
            print(colored(f"  shift {shift}", "blue"))
            print(colored(f"  distances {not_shifted_distances[25:]}", "blue"))
            print(colored(f"  max distance {max(not_shifted_distances)}", "blue"))
            print(colored(f"  min distance {min(not_shifted_distances)}", "blue"))

        ## TO ASK USER
        decision = ask_to_merge_two_traces(traces, [trace1, trace2], input_video, video_params=video_params, silent=silent)

        if debug:
            if decision:
                print(colored(f"Will merge overlapping traces {trace1_index}({trace1.trace_id}) and {trace2_index}({trace2.trace_id}).", "blue"))
            else:
                print(colored(f"Will NOT merge overlapping traces {trace1_index}({trace1.trace_id}) and {trace2_index}({trace2.trace_id}).", "blue"))
        return decision, shift
    else:
        if debug:
            # print(colored(f"Will NOT merge overlapping traces {trace1_index}({trace1.trace_id}) and {trace2_index}({trace2.trace_id}).", "yellow"))
            if not maximal_dist_check:
                reason = f"single huge point distance ({round(max(distances))} > {get_max_step_distance_to_merge_overlapping_traces()})"
            elif not minimal_dist_check:
                reason = f"all big point distance ({round(min(distances))} > {get_min_step_distance_to_merge_overlapping_traces()})"
            elif not overlap_movement_check:
                reason = f"both traces during the overlap too stationary ({trace1_avg_distance_per_frame_in_overlap}, {trace2_avg_distance_per_frame_in_overlap} > {get_minimal_movement_per_frame()})"
            else:
                raise NotImplemented("Reason not implemented yet.")

            print(colored(f"NOT MERGING THE OVERLAPPING TRACES as {reason}", "yellow"))
            print()

        return False, None


def merge_multiple_pairs_of_overlapping_traces(traces, pairs_of_traces_indices, silent=False, debug=False):
    """ Automatically merges given pairs of traces of given indices.

    :arg traces: (list): list of traces
    :arg traces: (list of ints): list of trace indices to be merged
    :arg silent: (bool): if True minimal output is shown
    :arg debug: (bool): if True extensive output is shown
    """
    indices_to_delete = []
    pairs_of_traces_indices = list(set(pairs_of_traces_indices))

    for index, pair in enumerate(pairs_of_traces_indices):
        trace1_index = pair[0]
        trace2_index = pair[1]
        trace1 = traces[pair[0]]
        trace2 = traces[pair[1]]

        merge_two_overlapping_traces(trace1, trace2, trace1_index, trace2_index, silent=silent, debug=debug)
        indices_to_delete.append(trace2_index)

        # Change the indices of the deleted trace
        for index2, pair2 in enumerate(pairs_of_traces_indices):
            if pair2[0] == trace2_index:
                pairs_of_traces_indices[index2] = (trace1_index, pair2[1])
            if pair2[1] == trace2_index:
                pairs_of_traces_indices[index2] = (pair2[0], trace1_index)

    ## DELETE THE MERGED TRACES:
    for index in list(reversed(sorted(indices_to_delete))):
        delete_indices([index], traces)


# TODO make tests
def merge_two_overlapping_traces(trace1: Trace, trace2: Trace, trace1_index, trace2_index, silent=False, debug=False):
    """ Puts two overlapping traces together.

    :arg trace1: (Trace): a Trace to be merged with the following trace
    :arg trace2: (Trace): a Trace to be merged with the following trace
    :arg trace1_index: (int): auxiliary information of index in list of traces of the first trace
    :arg trace2_index: (int): auxiliary information of index in list of traces of the second trace
    :arg silent: (bool): if True minimal output is shown
    :arg debug: (bool): if True extensive output is shown

    :returns: trace1: (Trace): merged trace of two given traces
    """
    # CHECK validity
    assert isinstance(trace1, Trace)
    assert isinstance(trace2, Trace)
    if not has_overlap(trace1.frame_range, trace2.frame_range):
        raise Exception("The two traces have no overlap. Try using function 'merge_two_traces_with_gap' instead.")
    else:
        overlap = get_overlap(trace1.frame_range, trace2.frame_range)
        if debug:
            print("trace1.frame_range", trace1.frame_range)
            print("trace1.frames_list", trace1.frames_list)
            print()
            print("trace2.frame_range", trace2.frame_range)
            print("trace2.frames_list", trace2.frames_list)
            print("overlap", overlap)

    # Decide whether to keep overlap of trace1 or trace2
    index1_overlap_start = trace1.get_frame_list().index(overlap[0])
    index2_overlap_end = trace2.get_frame_list().index(overlap[1])

    if debug:
        print("index1_overlap_start", index1_overlap_start)
        print("index2_overlap_end", index2_overlap_end)

    dist1 = math.dist(trace1.locations[index1_overlap_start - 1], trace2.locations[0])

    try:
        dist2 = math.dist(trace1.locations[-1], trace2.locations[index2_overlap_end + 1])
    except IndexError:
        pass

    if debug:
        print("dist1", dist1)
        print("dist2", dist2)

    trace1.frame_range = [trace1.frame_range[0], trace2.frame_range[1]]

    if dist1 < dist2:
        # Cutting trace1
        if not silent:
            print(colored(f"Cutting FIRST trace of the pair {trace1_index} of id {trace1.trace_id}.", "green"))
        # trim
        trace1.frames_list = trace1.frames_list[:index1_overlap_start]
        trace1.locations = trace1.locations[:index1_overlap_start]
    else:
        # Cutting trace2
        # trim
        if not silent:
            print(colored(f"Cutting SECOND trace of the pair {trace2_index} of id {trace2.trace_id}.", "green"))
        trace2.frames_list = trace2.frames_list[index2_overlap_end + 1:]
        trace2.locations = trace2.locations[index2_overlap_end + 1:]

    # Append frame list and locations
    trace1.frames_list.extend(trace2.frames_list)
    trace1.locations.extend(trace2.locations)

    # recalculate attributes
    trace1.frame_range_len = len(trace1.frames_list)

    if debug:
        print("trace1.frame_range", trace1.frame_range)
        # print("trace1.frames_tracked", trace1.frames_tracked)
        print("length trace1.frames_tracked", len(trace1.frames_list))
        # print("trace1.locations", trace1.locations)
        print("length trace1.locations", len(trace1.locations))

    # Add overlapping frames to the trace
    for frame in range(overlap[0], overlap[1]+1):
        trace1.overlap_frames.append(frame)
    trace1.overlap_frames = list(sorted(trace1.overlap_frames))

    # compute max step attributes
    trace1.recalculate_trace_lengths(recalculate_length=True, recalculate_lengths=True, recalculate_max_step_len=True)

    return trace1


def swap_two_overlapping_traces(trace1: Trace, trace2: Trace, frame_of_swap, silent=False, debug=False):
    """ Puts two overlapping traces together.

    :arg trace1: (Trace): a Trace to be merged with the following trace
    :arg trace2: (Trace): a Trace to be merged with the following trace
    :arg frame_of_swap: (int): frame number to swap the traces
    :arg silent: (bool): if True minimal output is shown
    :arg debug: (bool): if True extensive output is shown

    :returns: trace1: (Trace): merged trace of two given traces
    """
    # CHECK
    assert isinstance(trace1, Trace)
    assert isinstance(trace2, Trace)
    if not has_overlap(trace1.frame_range, trace2.frame_range):
        raise Exception("The two traces have no overlap. We cannot swap those.")

    # Swap frame_range
    spam = copy.copy(trace1.frame_range)
    trace1.frame_range = [trace1.frame_range[0], trace2.frame_range[1]]
    trace2.frame_range = [trace2.frame_range[0], spam[1]]

    # Swap frame_range_len
    trace1.frame_range_len = int(trace1.frame_range[1] - trace1.frame_range[0])
    trace2.frame_range_len = int(trace2.frame_range[1] - trace2.frame_range[0])

    # Get frame_list index of swap of first trace
    frame_list_index_1 = trace1.frames_list.index(frame_of_swap)
    if debug:
        print("frame_list_index_1", frame_list_index_1)
    # get frame_list index of swap of second trace
    frame_list_index_2 = trace2.frames_list.index(frame_of_swap)
    if debug:
        print("frame_list_index_2", frame_list_index_2)

    # Swap frame lists
    spam = trace1.frames_list[frame_list_index_1:]
    trace1.frames_list = trace1.frames_list[:frame_list_index_1]
    if debug:
        print("trace1.frames_list", trace1.frames_list)
    egg = trace2.frames_list[frame_list_index_2:]
    trace2.frames_list = trace2.frames_list[:frame_list_index_2]

    trace1.frames_list.extend(egg)
    if debug:
        print("trace1.frames_list", trace1.frames_list)
    trace2.frames_list.extend(spam)

    # Swap locations
    spam = trace1.locations[frame_list_index_1:]
    trace1.locations = trace1.locations[:frame_list_index_1]
    egg = trace2.locations[frame_list_index_2:]
    trace2.locations = trace2.locations[:frame_list_index_2]

    trace1.locations.extend(egg)
    trace2.locations.extend(spam)

    # Swap gap frames
    before_1 = []
    after_1 = []
    for index, gap_frame in enumerate(trace1.gap_frames):
        if gap_frame < frame_of_swap:
            before_1.append(frame_of_swap)
        else:
            after_1.append(frame_of_swap)
    before_2 = []
    after_2 = []
    for index, gap_frame in enumerate(trace2.gap_frames):
        if gap_frame < frame_of_swap:
            before_2.append(frame_of_swap)
        else:
            after_2.append(frame_of_swap)

    before_1.extend(after_2)
    before_2.extend(after_1)
    trace1.gap_frames = before_1
    trace2.gap_frames = before_2

    # Swap overlapping frames
    before_1 = []
    after_1 = []
    for index, gap_frame in enumerate(trace1.overlap_frames):
        if gap_frame < frame_of_swap:
            before_1.append(frame_of_swap)
        else:
            after_1.append(frame_of_swap)
    before_2 = []
    after_2 = []
    for index, gap_frame in enumerate(trace2.overlap_frames):
        if gap_frame < frame_of_swap:
            before_2.append(frame_of_swap)
        else:
            after_2.append(frame_of_swap)

    before_1.extend(after_2)
    before_2.extend(after_1)
    trace1.overlap_frames = before_1
    trace2.overlap_frames = before_2

    # Compute trace_length(s)
    # precondition: Swap locations
    trace1.recalculate_trace_lengths(recalculate_length=True, recalculate_lengths=True, recalculate_max_step_len=True)
    trace2.recalculate_trace_lengths(recalculate_length=True, recalculate_lengths=True, recalculate_max_step_len=True)

    return trace1, trace2


# TODO make tests
def ask_to_merge_two_traces(all_traces, selected_traces, input_video, video_params=False, silent=False):
    """ Creates a user dialogue to ask whether to merge selected pair of traces while showing video of the traces

        :arg all_traces: (list): a list of all Traces (to be shown in the video)
        :arg selected_traces: (list): two selected traces
        :arg input_video: (str or bool): if set, path to the input video
        :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
    """
    assert len(selected_traces) == 2
    trace1, trace2 = selected_traces

    overlap_range = get_overlap(trace1.frame_range, trace2.frame_range)

    # Look whether there is not an answer already
    decisions = load_decisions()
    try:
        ## Decision to merge already made and found
        decision = decisions[("merge_overlapping_pair", trace1.trace_id, trace2.trace_id, tuple(overlap_range))]
        if not silent:
            print(colored(f" Decision loaded: {decision} to merge overlapping pair of ids - {trace1.trace_id, trace2.trace_id}", "blue"))
        return decision

    except KeyError:
        # Compute which part of the traces to show
        show_range = get_overlap(trace1.frame_range, trace2.frame_range)
        # if the two traces got no overlap
        if show_range is False:
            # use the gap instead
            show_range = (trace1.frame_range[1], trace2.frame_range[0])

        traces_to_show = order_traces(all_traces, [trace1, trace2], selected_range=margin_range(show_range, 15))

        show_video(input_video=input_video, traces=traces_to_show, frame_range=margin_range(show_range, 15),
                   video_speed=0.02, wait=True, video_params=video_params, fix_x_first_colors=2)

        # to_show_longer_video = input("Do you want to see longer video? (yes or no):")
        to_merge_by_user = input("Merge these traces? (yes or no) (press l to see a longer video before, f to see full and both traces):")
        if "l" in to_merge_by_user.lower():
            selected_range = (max(show_range[0] - 100, trace1.frame_range[0] - 15), min(show_range[1] + 100, trace2.frame_range[1] + 15))
            traces_to_show = order_traces(all_traces, [trace1, trace2], selected_range=selected_range)
            show_video(input_video=input_video, traces=traces_to_show,
                       frame_range=(trace1.frame_range[0] - 15, trace2.frame_range[1] + 15),
                       video_speed=0.02, wait=True, video_params=video_params, fix_x_first_colors=2)
            to_merge_by_user = input("Merge these traces now? (yes or no)")
        elif "f" in to_merge_by_user.lower():
            traces_to_show = order_traces(all_traces, [trace1, trace2], selected_range=(trace1.frame_range[0] - 15, trace2.frame_range[1] + 15))
            show_video(input_video=input_video, traces=traces_to_show,
                       frame_range=(trace1.frame_range[0] - 15, trace2.frame_range[1] + 15),
                       video_speed=0.02, wait=True, video_params=video_params, fix_x_first_colors=2)
            to_merge_by_user = input("Merge these traces now? (yes or no)")

        if "n" in to_merge_by_user.lower():
            decisions[("merge_overlapping_pair", trace1.trace_id, trace2.trace_id, tuple(overlap_range))] = False
            save_decisions(decisions, silent=silent)
            return False
        elif "y" in to_merge_by_user.lower():
            decisions[("merge_overlapping_pair", trace1.trace_id, trace2.trace_id, tuple(overlap_range))] = True
            save_decisions(decisions, silent=silent)
            return True
        else:
            if not silent:
                print("Not merging, not saving.")
            return False

        # # if the answer was neither yes nor no
        # return ask_to_merge_two_traces(all_traces, selected_traces, input_video, video_params=video_params)


def ask_to_delete_a_trace(traces, input_video, possible_options, video_params=False):
    """ Creates a user dialogue to ask whether to delete a certain trace while showing video of the trace

    :arg traces: (list): a list of Traces
    :arg input_video: (str or bool): if set, path to the input video
    :arg possible_options: (list or tuple): list of option to pick from
    :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)

    :returns traces_indices_to_be_removed: (list of ints): list of indices to be removed
    """
    traces_indices_to_be_removed = []
    to_delete_by_user = input("Are we going to delete any of the shown traces? (yes or no):")

    if "y" in to_delete_by_user.lower():
        traces_to_delete = input("Write an index of one or more (separate the indices by comma) of the traces to be deleted (number before the bracket):")
        try:
            traces_to_delete = [int(traces_to_delete)]
        except ValueError:
            try:
                traces_to_delete = make_tuple(traces_to_delete)
            except ValueError:
                print(colored("Not selected any trace to be deleted. Skipping this triplet.", "red"))

        for item in traces_to_delete:
            if item not in possible_options:
                print(colored("Choosing an option out of scope, I guess you made a typo, let's do this again.", "red"))
                return ask_to_delete_a_trace(traces, input_video, possible_options, video_params=False)

        to_show_the_trace = input(f"Before deleting, show the whole trace(s) {traces_to_delete} in respective video(s) (highlighted with blue color)? (yes or no):")
        if "y" in to_show_the_trace.lower():
            # show_video(input_video, traces=(), frame_range=(), video_speed=0.1, wait=False, points=(), video_params=True)
            for trace_index in traces_to_delete:
                show_video(input_video, traces=[traces[trace_index]], frame_range=traces[trace_index].frame_range, video_speed=0.02, wait=True, video_params=video_params)
            to_delete_the_trace = input(f"Delete this trace? (yes or no):")
            if "y" in to_delete_the_trace.lower():
                to_delete = True
            else:
                to_delete = False
        else:
            to_delete = True

        if to_delete:
            # Save the decisions
            decisions = load_decisions()
            for trace in traces_to_delete:
                decisions[("delete_trace", trace.trace_id, trace.get_hash())] = True
            save_decisions(decisions, silent=True)

            traces_indices_to_be_removed.extend(traces_to_delete)

    return traces_indices_to_be_removed


# TODO make test
def delete_traces_from_saved_decisions(traces):
    """ Deletes the traces which have been previously selected to be deleted.

    :arg traces: (list): a list of Traces
    """
    indices_to_delete = []

    decisions = load_decisions()
    delete_decisions = list(filter(lambda x: x[0] == "delete_trace", decisions))

    i = 0
    j = 0

    while i < len(delete_decisions):
        while j < len(traces):
            # if the trace.id to be deleted is further, move the traces index
            if delete_decisions[i][1] > traces[j].trace_id:
                j = j + 1
            # if the trace.id is equal to the one to be deleted
            elif delete_decisions[i][1] == traces[j].trace_id:
                if delete_decisions[i][2] == traces[j].get_hash():
                    indices_to_delete.append(j)
                i = i + 1

    delete_indices(indices_to_delete, traces)
    print(f"Just deleted the traces with the following indices {indices_to_delete} by loading the saved decisions.")
    return traces


def compute_arena(traces, debug=False):
    """ Computes the arena population_size - center and diameter

        :arg traces: (list): a list of Traces
        :arg debug: (bool): if True extensive output is shown
    """
    all_locations = []
    # Get all locations of all traces
    for trace in traces:
        all_locations.extend(trace.locations)

    min_x = 999999999999999999
    min_y = 999999999999999999
    max_x = -9
    max_y = -9

    # Compute the boundaries of the traces
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

    # Compute the aprox. diameter of the arena
    diam_x = max_x - min_x
    diam_y = max_y - min_y

    if debug:
        print(f"diameter x {diam_x}, diameter y {diam_y}")

    # Set the highest of the diameters as the arena
    diam = max(diam_x, diam_y)

    # Compute the center of the elipse
    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2

    if debug:
        print(f"the center values are mid_x {mid_x} mid_y {mid_y}")

    center = [mid_x, mid_y]

    return center, diam


def compute_whole_frame_range(traces):
    """ Returns frame range of the whole video.

        :arg traces: (list): list of Traces
    """
    frame_range = [sys.maxsize, -sys.maxsize]
    for trace in traces:
        if trace.frame_range[0] < frame_range[0]:
            frame_range[0] = trace.frame_range[0]
        if trace.frame_range[1] > frame_range[1]:
            frame_range[1] = trace.frame_range[1]
    return frame_range


def get_video_whole_frame_range(traces):
    """ Returns frame range of the whole video for visualisation - adding margins.

        :arg traces: (list): list of Traces
    """
    a = compute_whole_frame_range(traces)
    return [a[0] - 2000, a[1] + 2000]


def remove_shortest_trace_out_of_three(trace1, trace2, trace3, trace1_index, trace2_index, trace3_index):
    """ Removes the shortest trace from the given 3 traces.

        :arg trace1: (Trace): first trace
        :arg trace2: (Trace): second trace
        :arg trace3: (Trace): third trace
        :arg trace1_index: (int): first trace index
        :arg trace2_index: (int): second trace index
        :arg trace3_index: (int): third trace index

        :returns: traceI, traceII, traceI_index, traceII_index
    """
    trace_index_to_omit = get_index_shortest_trace_out_of_three(trace1, trace2, trace3)
    return remove_a_trace_out_of_three(trace1, trace2, trace3, trace1_index, trace2_index, trace3_index, trace_index_to_omit)


def remove_a_trace_out_of_three(trace1, trace2, trace3, trace1_index, trace2_index, trace3_index, trace_index_to_omit):
    """ Removes a trace of the given trace_index to omit from the given 3 traces.

        :arg trace1: (Trace): first trace
        :arg trace2: (Trace): second trace
        :arg trace3: (Trace): third trace
        :arg trace1_index: (int): first trace index
        :arg trace2_index: (int): second trace index
        :arg trace3_index: (int): third trace index
        :arg trace_index_to_omit: (int): trace index of the trace to be omitted

        :returns: traceI, traceII, traceI_index, traceII_index
    """
    assert isinstance(trace1, Trace)
    assert isinstance(trace2, Trace)
    assert isinstance(trace3, Trace)

    duplet = [trace1, trace2, trace3]
    duplet_indices = [trace1_index, trace2_index, trace3_index]
    del duplet[trace_index_to_omit]
    del duplet_indices[trace_index_to_omit]
    trace1 = duplet[0]
    trace2 = duplet[1]
    del duplet
    trace1_index = duplet_indices[0]
    trace2_index = duplet_indices[1]

    return trace1, trace2, trace1_index, trace2_index


def get_index_shortest_trace_out_of_three(trace1, trace2, trace3):
    """ Returns the number of the shortest trace the given 3 traces.

        :arg trace1: (Trace): first trace
        :arg trace2: (Trace): second trace
        :arg trace3: (Trace): third trace

        :returns: number: (int) 1,2,3 based on whether trace1, trace2, or trace3 is the shortest
    """
    assert isinstance(trace1, Trace)
    assert isinstance(trace2, Trace)
    assert isinstance(trace3, Trace)

    ## Find the trace with min len
    trace_lengths = [trace1.frame_range_len, trace2.frame_range_len, trace3.frame_range_len]
    min_len = min(trace_lengths)
    min_len_index = trace_lengths.index(min_len)

    return min_len_index


def check_three_traces_insides(trace1, trace2, trace3):
    """ Checks whether there is a trace which is inside of another in whole range.

        :arg trace1: (Trace): first trace
        :arg trace2: (Trace): second trace
        :arg trace3: (Trace): third trace

        :returns: is_in: (bool): whether there is a trace which is inside of another in whole range
    """
    assert isinstance(trace1, Trace)
    assert isinstance(trace2, Trace)
    assert isinstance(trace3, Trace)

    return (is_in(trace1.frame_range, trace2.frame_range) or is_in(trace2.frame_range, trace1.frame_range) or
            is_in(trace2.frame_range, trace3.frame_range) or is_in(trace3.frame_range, trace2.frame_range) or
            is_in(trace1.frame_range, trace3.frame_range) or is_in(trace3.frame_range, trace1.frame_range))


def order_traces(all_traces, selected_traces, selected_range=None):
    """ Orders given selected traces to the beginning as given.
        Moreover, it returns only the list of

        EG. [trace1, trace2, trace3] [trace3] -> [trace3, trace1, trace2]

    :arg all_traces: (list of traces): list of traces to be ordered
    :arg selected_traces: (list of traces): list of traces to be up front
    :arg selected_range: (interval): only
    :returns: sorted_traces: (list of traces): list of ordered traces such that the selected traces are in the front of the list
    """
    ## Changed using this snippet
    # traces_to_show = get_traces_from_range(traces, margin_range(overlap_range, 15))[0]
    # spam = []
    # for index, trace in enumerate(traces_to_show):
    #     if trace.trace_id == trace1.trace_id or trace.trace_id == trace2.trace_id:
    #         continue
    #     else:
    #         spam.append(trace)
    # traces_to_show = [trace1, trace2, *spam]
    #
    # # if len(distances) == 52 and shift==6:
    # overlap_movement_check = trace1_avg_distance_per_frame_in_overlap < get_minimal_movement_per_frame() and \
    #                          trace2_avg_distance_per_frame_in_overlap < get_minimal_movement_per_frame()
    #
    # if overlap_movement_check:
    #     show_video(input_video, traces=traces_to_show, frame_range=margin_range(overlap_range, 50),
    #                video_speed=0.03, wait=True, video_params=video_params)

    if selected_range is not None:
        traces_to_order = get_traces_from_range(all_traces, selected_range)[0]
    else:
        traces_to_order = all_traces

    spam = []
    ids = list(map(lambda x: x.trace_id, selected_traces))
    for trace in traces_to_order:
        if trace.trace_id in ids:
            continue
        else:
            spam.append(trace)
    return [*selected_traces, *spam]


## TODO add tests
def is_there_full_overlap(list_of_intervals):
    """ Checks whether there is an interval which is inside of another in whole range.

        :arg list_of_intervals: (list of intervals): list of intervals to check

        :returns: is_in: (bool): whether there is an interval which is inside of another in whole range
    """
    # Sort intervals in increasing order
    list_of_intervals.sort()

    # In the sorted array, if end time of an interval is not more than that of
    # end of previous interval, then there is an overlap
    for i in range(1, len(list_of_intervals)):
        if list_of_intervals[i][1] <= list_of_intervals[i - 1][1]:
            return True

    # If we reach here, then is no overlap
    return False

