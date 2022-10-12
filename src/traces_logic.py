import copy

from misc import get_gap, is_in, has_overlap
from trace import Trace


def get_gaps_of_traces(traces, get_all_gaps=False, debug=False):
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


def swap_two_overlapping_traces(trace1: Trace, trace2: Trace, frame_of_swap, silent=False, debug=False):
    """ Puts two overlapping traces together.

    :arg trace1: (Trace): a Trace to be merged with the following trace
    :arg trace2: (Trace): a Trace to be merged with the following trace
    :arg frame_of_swap: (int): frame number to swap the traces
    :arg silent (bool) if True no output is shown
    :arg debug (bool) if True extensive output is shown

    :returns: trace1: (Trace): merged trace of two given traces
    """
    ## TODO delete this

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

    if debug:
        print()
    #
    # # Recalculate max attributes
    # # precondition: Compute trace_length(s)
    # max_step_len_1 = trace1.max_step_len
    # new_max_step_len_1 = max(trace1.trace_lengths.keys())
    #
    # max_step_len_2 = trace2.max_step_len
    # new_max_step_len_2 = max(trace2.trace_lengths.keys())
    #
    # if debug:
    #     print("new_max_step_len_1", new_max_step_len_1)
    #
    # # old attributes holds for trace1 (max1 is before swap)
    # if new_max_step_len_1 == max_step_len_1:
    #     if debug:
    #         print("max1 is before swap")
    # # trace2 attributes holds for trace1 (max1 is after swap)
    # elif new_max_step_len_1 == max_step_len_2 and trace2.max_step_len_frame_number > frame_of_swap:
    #     if debug:
    #         print("max1 is after swap")
    #     trace1.max_step_len = new_max_step_len_2
    #     trace1.max_step_len_step_index = trace2.max_step_len_step_index
    #     trace1.max_step_len_line = trace2.max_step_len_line
    #     trace1.max_step_len_frame_number = trace2.max_step_len_frame_number
    #
    # # old attributes DOES NOT hold for trace1
    # else:
    #     if debug:
    #         print("max1 is within swap")
    #     trace1.max_step_len = max(trace1.trace_lengths.keys())
    #     ## TODO recalculate the rest
    #     trace1.max_step_len_step_index = None
    #     trace1.max_step_len_line = None
    #     trace1.max_step_len_frame_number = None
    # if debug:
    #     pass
    # print("trace1.max_step_len", trace1.max_step_len)
    # print("trace1.max_step_len_step_index", trace1.max_step_len_step_index)
    # print("trace1.max_step_len_line", trace1.max_step_len_line)
    # print("trace1.max_step_len_frame_number", trace1.max_step_len_frame_number)
    #
    # ## TRACE2
    # # old attributes holds for trace1 (max2 is before swap)
    # if new_max_step_len_2 == max_step_len_2:
    #     pass
    # # trace2 attributes holds for trace1 (max2 is after swap)
    # elif new_max_step_len_2 == max_step_len_1 and trace1.max_step_len_frame_number > frame_of_swap:
    #     trace2.max_step_len = new_max_step_len_1
    #     trace2.max_step_len_step_index = trace1.max_step_len_step_index
    #     trace2.max_step_len_line = trace1.max_step_len_line
    #     trace2.max_step_len_frame_number = trace1.max_step_len_frame_number
    # # old attributes DOES NOT hold for trace2
    # else:
    #     trace2.max_step_len = max(trace2.trace_lengths.keys())
    #     ## TODO recalculate the rest
    #     trace1.max_step_len_step_index = None
    #     trace1.max_step_len_line = None
    #     trace1.max_step_len_frame_number = None

