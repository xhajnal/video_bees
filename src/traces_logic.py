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
