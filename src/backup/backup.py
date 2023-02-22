from _socket import gethostname
from copy import copy
from time import time
from termcolor import colored

from misc import dictionary_of_m_overlaps_of_n_intervals, get_index_of_shortest_range, is_in, delete_indices
from trace import Trace
from traces_logic import partition_frame_range_by_number_of_traces, reverse_partition_frame_range_by_number_of_traces, \
    get_traces_from_range


def trim_out_additional_agents_over_long_traces_by_partition(traces, population_size, silent=False, debug=False):
    """ Trims out additional appearance of an agent over a longer trace.
        This version is using partition_frame_range_by_number_of_traces

        :arg traces: (list): list of traces
        :arg whole_frame_range: [int, int]: frame range of the whole video (with margins)
        :arg population_size: (int): expected number of agents
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :returns: traces: (list): list of concatenated Traces
    """
    print(colored("TRIM OUT ADDITIONAL AGENTS OVER A LONG TRACES (partition)", "blue"))
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
            group_of_traces = get_traces_from_range(traces, interval, fully_inside=False, strict=True)[1]

            if debug:
                # print("segment/interval_index", interval_index)
                print("segment/interval", interval)
                print("group_of_traces - indices", group_of_traces)

            to_delete_in_this_cycle = []
            for trace_index in group_of_traces:
                ## TODO have look how this performs when used shorter trace instead of is_in
                if is_in(traces[trace_index].frame_range, interval):
                    to_delete_in_this_cycle.append(trace_index)
                    if debug:
                        print(colored(f"Adding trace n. {trace_index} id {traces[trace_index].trace_id} of frame range {traces[trace_index].frame_range} to be deleted.", "yellow"))
                    # TODO can delete this after test
                    if tuple(traces[trace_index].frame_range) != tuple(interval):
                        raise Exception(f"A trace is {traces[trace_index].trace_id} of range {traces[trace_index].frame_range} which is supposed to have frame range {interval} has only its subinterval.")

            # TODO can delete this after test
            if len(to_delete_in_this_cycle) > 1:
                print(f"More than 1 trace is in this {interval}: {to_delete_in_this_cycle}. Not deleting any.")
                # TODO add a guided fix
                to_delete_in_this_cycle = []

            trace_indices_to_delete.extend(to_delete_in_this_cycle)
            ids_of_traces_to_be_deleted.extend(list(map(lambda x: traces[x].trace_id, to_delete_in_this_cycle)))

            # Fix the structures
            interval_to_traces_count[interval] = interval_to_traces_count[interval] - 1
            for index, spam in traces_count_to_intervals[count]:
                if spam == interval:
                    del traces_count_to_intervals[count][index]
            try:
                traces_count_to_intervals[count-1].append(interval)
            except KeyError:
                traces_count_to_intervals[count - 1] = [interval]

            if debug:
                print(colored(interval_to_traces_count, "red"))
                print()
                print(colored(traces_count_to_intervals, "red"))
                print()

    if debug:
        print(colored(f"trace_indices_to_delete {trace_indices_to_delete}", "blue"))
    delete_indices(trace_indices_to_delete, traces)

    print(colored(f"trim_out_additional_agents_over_long_traces using partition analysis done. It took {gethostname()} {round(time() - start_time, 3)} seconds.", "yellow"))
    print(colored(f"Returning {len(traces)} traces, {len(trace_indices_to_delete)} shorter than in previous iteration. \n", "green"))
    return traces, ids_of_traces_to_be_deleted


def trim_out_additional_agents_over_long_traces_with_dict(traces, overlap_dictionary, population_size, silent=False, debug=False):
    """ Trims out additional appearance of an agent over a longer trace.
        This version is using dictionary_of_m_overlaps_of_n_intervals.

        :arg traces: (list): list of Traces
        :arg overlap_dictionary: (dict): dictionary_of_m_overlaps_of_n_intervals
        :arg population_size: (int): expected number of agents
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :returns: traces: (list): list of trimmed Traces
    """
    print(colored("TRIM OUT ADDITIONAL AGENTS OVER A LONG TRACES (iterative build of overlaps)", "blue"))
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
        dictionary = dictionary_of_m_overlaps_of_n_intervals(population_size + 1, ranges, strict=True, skip_whole_in=False, debug=False)
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
    if debug:
        print(dictionary)

    indices_of_intervals_to_be_deleted = []
    ids_of_traces_to_be_deleted = []
    keys_to_be_deleted = []

    for overlap in dictionary.keys():
        if debug:
            print(colored(f" Currently checking overlapping indices: {overlap}", "blue"))

        ## Check whether a trace in the overlap is not already gone
        skip_this_overlap = False
        for trace_index in overlap:
            if trace_index in indices_of_intervals_to_be_deleted:
                if debug:
                    print(colored(f" Trace with index {trace_index} is already gonna be deleted, skipping this pair.", "yellow"))
                skip_this_overlap = True

        if skip_this_overlap:
            continue

        ## Compute the ranges
        overlapping_ranges = []
        for interval_index in overlap:
            try:
                overlapping_ranges.append(ranges[interval_index])
            except IndexError as err:
                raise err

        # Get the index of the shortest range, skip if there are more shortest ranges
        spam = get_index_of_shortest_range(overlapping_ranges)
        if isinstance(spam, tuple):
            if debug:
                print(colored("There is no single shortest range!", "red"))
            continue
        index_of_shortest_range = overlap[spam]

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
            ids_of_traces_to_be_deleted.append(traces[index_of_shortest_range].trace_id)
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
    ## TODO fix to: return traces, dictionary
    return traces, None, ids_of_traces_to_be_deleted


# DEPRECATED
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
            # Obtain trace and trace indices of the traces in the segment
            traces_subset, traces_subset_indices = get_traces_from_range(traces, interval, fully_inside=False, strict=True)

            if debug:
                # print("segment/interval_index", interval_index)
                print("segment/interval", interval)
                print("group_of_traces - indices", traces_subset_indices)

            to_delete_in_this_segment = []
            for trace_index in traces_subset_indices:
                if is_in(traces[trace_index].frame_range, interval):
                    # ## TODO Delete this after test
                    # if trace_index in to_delete_in_this_segment:
                    #     print(colored("AAARGH", "magenta"))
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
                # else:
                #     print(colored("AAARGH", "magenta"))

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