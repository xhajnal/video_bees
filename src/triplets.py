from time import time
from _socket import gethostname
from termcolor import colored
from operator import countOf

from config import *
from cross_traces import compare_two_traces
from misc import is_in, delete_indices, dictionary_of_m_overlaps_of_n_intervals, flatten
from trace import Trace

from traces_logic import merge_two_overlapping_traces
from visualise import scatter_detection, show_plot_locations, show_overlaps


def merge_overlapping_triplets_of_traces(traces, whole_frame_range, population_size, guided=False,  silent=False, debug=False, show=False):
    """ Puts traces together such that all the agents but one is being tracked.

        :arg traces (list) list of traces
        :arg whole_frame_range: [int, int]: frame range of the whole video
        :arg population_size (int) expected number of agents
        :arg guided: (bool): if True, user guided version would be run, this stops the whole analysis until a response is given
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :arg show: (bool): if True plots are shown
        :returns: traces: (list): list of concatenated Traces
    """
    print(colored("MERGE OVERLAPPING TRIPLETS OF TRACES", "blue"))
    start_time = time()
    starting_number_of_traces = len(traces)

    count_two = [-9]  # indices of traces which have exactly two occurrences
    number_of_traces = -9
    force_merge = False

    while len(count_two) >= 1 or number_of_traces != len(traces):
        number_of_traces = len(traces)
        # Check whether there are at least 2 traces
        if len(traces) <= 2:
            if len(traces) == 2:
                print(colored("There is no triplet in pair of traces. Skipping the rest of this analysis.\n", "yellow"))
                return
            if len(traces) == 1:
                print(colored("Cannot merge a single trace. Skipping the rest of this analysis.\n", "yellow"))
                return
            if len(traces) == 0:
                print(colored("Cannot merge no trace. Skipping the rest of this analysis.\n", "yellow"))
                return

        # Find overlapping pairs
        dictionary = dictionary_of_m_overlaps_of_n_intervals(3, list(map(lambda x: x.frame_range, traces)), skip_whole_in=True)

        # print("dictionary", dictionary)
        if dictionary == {}:
            print(colored("Cannot merge any trace as there is no partial overlap of three traces.", "red"))
            print(colored(f"Returning {len(traces)} traces, {starting_number_of_traces - len(traces)} merged. "
                          f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "yellow"))
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
            count_two = []
            for key in counts.keys():
                # Check there is no interval with 3 or more overlaps - hence cannot easily merge
                # if counts[key] >= 3:
                #     raise Exception("I`m sorry Dave, I`m afraid I cannot do that.")
                if counts[key] == 1:
                    count_two.append(key)
            if debug:
                print("count_two", count_two)

            if len(count_two) == 0:
                print(colored("Cannot merge more traces. No triplet of overlapping traces.", "red"))
                if debug:
                    for trace_index, trace in enumerate(traces):
                        print(f"trace {trace_index} of range {trace.frame_range}")
                print(colored(f"Returning {len(traces)} traces, {starting_number_of_traces - len(traces)} merged. "
                              f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "yellow"))
                return

            # Pick the smallest index
            pick_key = min(count_two)

            if debug:
                print("pick_key", pick_key)

            # Find the triplet of the smallest index which has two overlaps
            for key in dictionary.keys():
                if pick_key in key:  # the triplet has the smallest index
                    pick_key2 = key
                    if debug:
                        print("pick_key2", pick_key2)
                    break

            trace1 = traces[pick_key2[0]]
            assert isinstance(trace1, Trace)
            trace2 = traces[pick_key2[1]]
            assert isinstance(trace2, Trace)
            trace3 = traces[pick_key2[2]]
            assert isinstance(trace3, Trace)

            # if the picked traces are overlapping in whole range of one of the traces we delete it from the dictionary and move on
            if is_in(trace1.frame_range, trace2.frame_range) or is_in(trace2.frame_range, trace1.frame_range) or \
                    is_in(trace2.frame_range, trace3.frame_range) or is_in(trace3.frame_range, trace2.frame_range) or \
                    is_in(trace1.frame_range, trace3.frame_range) or is_in(trace3.frame_range, trace1.frame_range):
                if debug:
                    print("trace1.frame_range", trace1.frame_range)
                    print("trace2.frame_range", trace2.frame_range)
                    print("trace3.frame_range", trace3.frame_range)
                    print("Gonna delete ", dictionary[pick_key2])
                    print(dictionary)
                del dictionary[pick_key2]
                if debug:
                    print(dictionary)
                    print()
                go_next = True
                continue

            if not guided:
                ## Find the trace with min len
                trace_lengths = [trace1.frame_range_len, trace2.frame_range_len, trace3.frame_range_len]
                min_len = min(trace_lengths)
                min_len_index = trace_lengths.index(min_len)
                trace_index_to_omit = min_len_index
            else:
                ## Version where these three traces would be shown so that user can handpick which to delete
                print(colored(f"We have found a triplet of overlapping traces {pick_key2[0]}({trace1.trace_id}),{pick_key2[1]}({trace2.trace_id}),{pick_key2[2]}({trace3.trace_id}. Please select a pair to merge.", "blue"))
                ## scatter plot of the triplet
                scatter_detection([trace1, trace2, trace3], whole_frame_range, subtitle=f"Triplet {pick_key2[0]}({trace1.trace_id}),{pick_key2[1]}({trace2.trace_id}),{pick_key2[2]}({trace3.trace_id}).")
                ## show position
                show_plot_locations([trace1, trace2, trace3], whole_frame_range, subtitle=f"Triplet {pick_key2[0]}({trace1.trace_id}),{pick_key2[1]}({trace2.trace_id}),{pick_key2[2]}({trace3.trace_id}).")
                ## show the overlap
                show_overlaps([trace1, trace2, trace3], whole_frame_range, subtitle=f"Triplet {pick_key2[0]}({trace1.trace_id}),{pick_key2[1]}({trace2.trace_id}),{pick_key2[2]}({trace3.trace_id}).")
                ## show frames of the video
                ## TODO

                # Ask for the index of the first trace to be merged and verify it
                first_trace_to_merge = input("Write an index of one of the traces to be merged (number before the bracket):")
                try:
                    first_trace_to_merge = int(first_trace_to_merge)
                except ValueError:
                    print(colored("Not selected any trace to be merged. Skipping this triplet.", "red"))
                    continue
                if first_trace_to_merge not in pick_key2:
                    print(colored("Selected trace not in the triplet. Skipping it.", "red"))
                    continue

                # Ask for the index of the second trace to be merged and verify it
                second_trace_to_merge = input("Write an index of the other trace to be merged (number before the bracket):")
                try:
                    second_trace_to_merge = int(second_trace_to_merge)
                except ValueError:
                    print(colored("Not selected any trace to be merged. Skipping this triplet.", "red"))
                    continue
                if second_trace_to_merge not in pick_key2:
                    print(colored("Selected trace not in the triplet. Skipping it.", "red"))
                    continue

                # Find the trace which is not to be merged (the one not picked)
                for trace_index in pick_key2:
                    if trace_index != first_trace_to_merge and trace_index != second_trace_to_merge:
                        trace_index_to_omit = trace_index

            ## Obtain the pair of traces and their indices
            duplet = [trace1, trace2, trace3]
            duplet_indices = list(pick_key2)
            del duplet[trace_index_to_omit]
            del duplet_indices[trace_index_to_omit]
            trace1 = duplet[0]
            trace2 = duplet[1]
            del duplet

            ## TODO the following code is copied, we might merge it to a single one
            # Compare the two traces
            if show:
                showw = False
            else:
                showw = None

            # Check the distances of overlap for a big difference
            distances = compare_two_traces(trace1, trace2, duplet_indices[0], duplet_indices[1],
                                           silent=silent, debug=debug, show_all_plots=None if force_merge else showw)

            #  Save the id of the merged trace before it is removed
            trace2_id = trace2.trace_id
            if distances is not None and any(
                    list(map(lambda x: x > get_max_step_distance_to_merge_overlapping_traces(), distances))):
                go_next = True
                to_merge = False
                reason = f"single huge distance (>{get_max_step_distance_to_merge_overlapping_traces()})"

                # the distance of the traces is greater than the given threshold, we move on
                del dictionary[pick_key2]
            else:
                # Merge these two traces
                to_merge = True
                merge_two_overlapping_traces(trace1, trace2, duplet_indices[0], duplet_indices[1],
                                             silent=silent, debug=debug)
                #
                # Remove the merged trace
                if debug:
                    # print(colored(f"Gonna delete trace {trace2_id}.", "blue"))
                    print(colored(f"Gonna delete trace {duplet_indices[1]}({trace2_id}).", "blue"))
                    print()
                traces = delete_indices([duplet_indices[1]], traces)
                # Show scatter plot of traces having two traces merged
                go_next = False

            if not silent:
                msg = f"{'' if to_merge else 'NOT '}MERGING OVERLAPPING TRACES {'' if to_merge else '(' + reason + ') '}"
                print(colored(msg, "yellow") if to_merge else colored(msg, "red"))

            if show:
                try:
                    scatter_detection(traces, whole_frame_range,
                                      subtitle=f"after merging overlapping traces {duplet_indices[0]} of id {trace1.trace_id} and {duplet_indices[1]} of id {trace2_id}.")
                except UnboundLocalError:
                    pass

    print(colored(f"Returning {len(traces)} traces, {starting_number_of_traces - len(traces)} merged. "
                  f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "yellow"))
    return traces
