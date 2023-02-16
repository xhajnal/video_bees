import copy
import math
import sys

import numpy as np
from termcolor import colored
from ast import literal_eval as make_tuple

from config import get_max_trace_gap_to_interpolate_distance
from misc import get_gap, is_in, has_overlap, is_before, merge_dictionary, get_overlap, has_dot_overlap
from trace import Trace
from video import show_video


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


def get_traces_from_range(traces, interval, are_inside=False, strict=True):
    """ Returns the traces, indices with frame range in given range

    :arg traces: (list): a list of Traces
    :arg interval: (tuple): range to pick traces
    :arg are_inside: (bool): whether trace is whole inside the interval
    :arg strict: (bool): whether single point overlaps are excluded
    :return: list of traces in the given range
    """
    traces_in_range = []
    trace_indices_in_range = []
    for index, trace in enumerate(traces):
        assert isinstance(trace, Trace)
        if are_inside:
            if is_in(trace.frame_range, interval):
                traces_in_range.append(trace)
                trace_indices_in_range.append(index)
        else:
            if has_dot_overlap(trace.frame_range, interval, strict):
                traces_in_range.append(trace)
                trace_indices_in_range.append(index)

    return traces_in_range, trace_indices_in_range


def get_gaps_of_traces(traces, get_all_gaps=False, debug=False):
    # TODO make tests
    """ Returns a dictionary of pairs of traces indices -> range of their gap.
    Including only gaps which do not contain a whole traces - hence only shortest gaps.

    :arg traces: (list): a list of Traces
    :arg get_all_gaps: (bool) if True returns all gaps
    :arg debug: (bool): if True extensive output is shown
    :return: dictionary of pairs of traces indices -> range of their gap.
    """
    pairs_of_gaps = {}
    for index1, trace1 in enumerate(traces):
        for index2, trace2 in enumerate(traces):
            if index1 < index2:
                assert isinstance(trace1, Trace)
                assert isinstance(trace2, Trace)
                # print("    index1", index1, trace1.frame_range)
                # print("    index2", index2, trace2.frame_range)
                a = get_gap(trace1.frame_range, trace2.frame_range)
                # print("    gap", a)
                if a is not False:
                    pairs_of_gaps[(index1, index2)] = a

    if debug:
        print("pairs_of_gaps", pairs_of_gaps)
    pairs_to_delete = []

    for pair in pairs_of_gaps.keys():
        for index, trace in enumerate(traces):
            if index in pair:
                continue
            if get_all_gaps:
                if is_in(trace.frame_range, pairs_of_gaps[pair]):
                    pairs_to_delete.append(pair)
                    break
            else:
                if has_overlap(trace.frame_range, pairs_of_gaps[pair]):
                    pairs_to_delete.append(pair)
                    break

    for pair in pairs_to_delete:
        del pairs_of_gaps[pair]

    return pairs_of_gaps


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


def merge_two_overlapping_traces(trace1: Trace, trace2: Trace, trace1_index, trace2_index,  silent=False, debug=False):
    # TODO make tests
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

    # Decide whether to keep overlap of trace1 or trace2
    index1_overlap_start = trace1.frames_list.index(overlap[0])
    index2_overlap_end = trace2.frames_list.index(overlap[1])

    if debug:
        print("index1_overlap_start", index1_overlap_start)
        print("index2_overlap_end", index2_overlap_end)

    dist1 = math.dist(trace1.locations[index1_overlap_start - 1], trace2.locations[0])
    dist2 = math.dist(trace1.locations[-1], trace2.locations[index2_overlap_end + 1])

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


def ask_to_delete_a_trace(traces, input_video, possible_options, video_params=False):
    """ Creates a user dialogue to ask whether to delete a certain trace while showing video of the trace

    :arg traces: (list): a list of Traces
    :arg input_video: (str or bool): if set, path to the input video
    :arg possible_options: (list or tuple): list of option to pick from
    :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
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
            traces_indices_to_be_removed.extend(traces_to_delete)

    return traces_indices_to_be_removed


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
