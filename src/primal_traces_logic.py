from time import time
from _socket import gethostname
from termcolor import colored

from misc import is_in, get_strict_gap, has_dot_overlap, has_overlap
from trace import Trace


def get_gaps_of_traces(intervals, debug=False):
    """ Returns a dictionary of pairs of traces indices -> range of their gap.
    Including only gaps which do not contain a whole traces - hence only shortest gaps.

    :arg intervals: (list): a list of ranges
    :arg debug: (bool): if True extensive output is shown
    :return: dictionary of pairs of traces indices -> range of their gap.
    """
    start_time = time()

    pairs_of_gaps = {}

    i, j = 0, 0
    while i < len(intervals):
        j = i + 1
        while j < len(intervals):
            range1 = intervals[i]
            range2 = intervals[j]
            assert len(range1) == 2
            assert len(range2) == 2
            a = get_strict_gap(range1, range2)
            # print("    gap", a)
            if a is not False:
                pairs_of_gaps[(i, j)] = a
                break
            j = j + 1
        i = i + 1

    if debug:
        print("pairs_of_gaps", pairs_of_gaps)
        print(colored(f"In total, there are {len(pairs_of_gaps)} gaps. It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))

    return pairs_of_gaps


# TODO make tests
def get_gaps_of_traces_old(traces, get_all_gaps=False, debug=False):
    """ Returns a dictionary of pairs of traces indices -> range of their gap.
    Including only gaps which do not contain a whole traces - hence only shortest gaps.

    :arg traces: (list): a list of Traces
    :arg get_all_gaps: (bool) if True returns all gaps
    :arg debug: (bool): if True extensive output is shown
    :return: dictionary of pairs of traces indices -> range of their gap.
    """
    start_time = time()

    pairs_of_gaps = {}
    for index1, trace1 in enumerate(traces):
        for index2, trace2 in enumerate(traces):
            if index1 < index2:
                assert isinstance(trace1, Trace)
                assert isinstance(trace2, Trace)
                # print("    index1", index1, trace1.frame_range)
                # print("    index2", index2, trace2.frame_range)
                a = get_strict_gap(trace1.frame_range, trace2.frame_range)
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

    print(colored(f"In total, there are {len(pairs_of_gaps)} gaps. It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))

    return pairs_of_gaps


def get_traces_from_range(traces, interval, fully_inside=False, strict=True):
    """ Returns the traces, indices with frame range in given range

    :arg traces: (list): a list of Traces
    :arg interval: (tuple): range to pick traces
    :arg fully_inside: (bool): get only traces in the interval (with whole range)
    :arg strict: (bool): whether single point overlaps are excluded
    :return: list of traces in the given range, list of trace indices in the given range
    """
    traces_in_range = []
    trace_indices_in_range = []
    for index, trace in enumerate(traces):
        if trace is None:
            continue

        assert isinstance(trace, Trace)
        if fully_inside:
            if is_in(trace.frame_range, interval):
                traces_in_range.append(trace)
                trace_indices_in_range.append(index)
        else:
            if has_dot_overlap(trace.frame_range, interval, strict):
                traces_in_range.append(trace)
                trace_indices_in_range.append(index)

    return traces_in_range, trace_indices_in_range
