from misc import has_overlap, get_gap, is_in
from trace import Trace


def get_gaps_of_traces(traces):
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

    print("pairs_of_gaps", pairs_of_gaps)
    pairs_to_delete = []

    for pair in pairs_of_gaps.keys():
        for index, trace in enumerate(traces):
            if index in pair:
                continue
            if is_in(trace.frame_range, pairs_of_gaps[pair]):
                pairs_to_delete.append(pair)
                break

    for pair in pairs_to_delete:
        del pairs_of_gaps[pair]

    return pairs_of_gaps
