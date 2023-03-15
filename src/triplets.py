from copy import copy
from time import time
from _socket import gethostname
from termcolor import colored
from operator import countOf

from counts import set_single_run_seen_overlaps, set_single_run_allowed_overlaps_count, \
    set_single_run_seen_overlaps_deleted, get_single_run_seen_overlaps_deleted, set_single_run_overlaps_count
from fake import get_whole_frame_range
from config import *
from misc import delete_indices, dictionary_of_m_overlaps_of_n_intervals, get_overlap, flatten, margin_range
from primal_traces_logic import get_traces_from_range
from trace import Trace

from traces_logic import merge_two_overlapping_traces, ask_to_delete_a_trace, \
    partition_frame_range_by_number_of_traces, reverse_partition_frame_range_by_number_of_traces, \
    check_to_merge_two_overlapping_traces, merge_multiple_pairs_of_overlapping_traces, \
    get_index_shortest_trace_out_of_three, remove_shortest_trace_out_of_three, remove_a_trace_out_of_three, \
    is_there_full_overlap
from video import show_video
from visualise import scatter_detection, show_plot_locations, show_overlaps


def merge_overlapping_triplets_of_traces(traces, shift=False, guided=False, input_video=False,  silent=False, debug=False, show=False, show_all_plots=False, video_params=False):
    """ Puts traces together such that all the agents but one is being tracked.

        :arg traces (list) list of traces
        :arg whole_frame_range: [int, int]: frame range of the whole video (with margins)
        :arg shift: (False ir int): if False, no shift is used, else shift upto the given value is used to compare the traces
        :arg guided: (bool): if True, user guided version would be run, this stops the whole analysis until a response is given
        :arg input_video: (str or bool): if set, path to the input video
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :arg show: (bool): if True plots are shown
        :arg show_all_plots: (bool): if True all plots are shown
        :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
        :returns: traces: (list): list of concatenated Traces
    """
    print(colored("MERGE OVERLAPPING TRIPLETS OF TRACES - by build", "blue"))
    # Initiation
    start_time = time()
    starting_number_of_traces = len(traces)
    # whole_frame_range = get_whole_frame_range()

    ## Internal variables
    count_two = [-9]  # indices of traces which have exactly two occurrences
    number_of_traces = -9
    force_merge = False
    traces_indices_to_be_removed = []

    # Internal/Output variables
    removed_traces = []
    skipped_triplets_indices = []

    if show is False:
        show_all_plots = False

    while len(count_two) >= 1 and number_of_traces != len(traces):
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
        if not guided:
            # not using strict version as having >3 traces overlap to be a single point
            dictionary = dictionary_of_m_overlaps_of_n_intervals(3, list(map(lambda x: x.frame_range, traces)), skip_whole_in=True)

        # Flag whether to try another pair of overlapping intervals
        go_next = True
        while go_next and len(traces) >= 3:
            # Find overlapping pairs
            if guided:
                dictionary = dictionary_of_m_overlaps_of_n_intervals(3, list(map(lambda x: x.frame_range, traces)), skip_whole_in=True)

            # print("dictionary", dictionary)
            if dictionary == {}:
                print(colored("Cannot merge any trace as there is no partial overlap of three traces.", "yellow"))
                print(colored(f"Returning {len(traces)} traces, {starting_number_of_traces - len(traces)} merged. "
                              f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
                return
            if not silent:
                print(f"triplets ({len(dictionary)}): {dictionary}")

            if debug:
                print("dictionary", dictionary)
                for trace_index, trace in enumerate(traces):
                    print(f"trace {trace_index} ({trace.trace_id}) of frame range {trace.frame_range}")
                print()

            ## Remove skipped keys
            for item in skipped_triplets_indices:
                try:
                    del dictionary[item]
                except:
                    pass

            # Flattened indices of overlapping pairs of traces
            keys = flatten(tuple(dictionary.keys()))

            # Count occurrences of trace indices in overlapping pairs
            counts = {}
            for item in set(keys):
                counts[item] = countOf(keys, item)
            if debug:
                print("keys", keys)
                print("counts", counts)

            # Find traces with single occurrence (within the tuples of overlapping traces)
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
                              f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
                return

            # Pick the smallest index
            pick_key = min(count_two)
            if debug:
                print("pick_key", pick_key)

            # Find the triplet of the smallest index which has two overlaps
            picked_key = None
            for key in dictionary.keys():
                # with the smallest index
                if pick_key in key:
                    picked_key = key
                    if debug:
                        print("picked_key", picked_key)
                    break
            if picked_key is None:
                go_next = False
                break

            # parse the traces from dict
            trace1_index = picked_key[0]
            trace1 = traces[trace1_index]
            trace2_index = picked_key[1]
            trace2 = traces[trace2_index]
            trace3_index = picked_key[2]
            trace3 = traces[trace2_index]

            triplet_overlap_range = dictionary[picked_key]
            user_merging = False
            to_merge = False

            if not guided:
                ## Omit the trace with min len
                trace_index_to_omit = get_index_shortest_trace_out_of_three(trace1, trace2, trace3)
            else:
                ## Version where these three traces would be shown so that user can handpick which to delete
                print(colored(f"We have found a triplet of overlapping traces {picked_key[0]}({trace1.trace_id}),{picked_key[1]}({trace2.trace_id}),{picked_key[2]}({trace3.trace_id}). Please select a pair to merge.", "blue"))

                ## Compute the ranges
                min_trace_range = min([trace1.frame_range[0], trace2.frame_range[0], trace3.frame_range[0]])
                max_trace_range = max([trace1.frame_range[1], trace2.frame_range[1], trace3.frame_range[1]])
                min_overlap_range = min(get_overlap(trace1.frame_range, trace2.frame_range)[0], get_overlap(trace2.frame_range, trace3.frame_range)[0])
                max_overlap_range = max(get_overlap(trace1.frame_range, trace2.frame_range)[1], get_overlap(trace2.frame_range, trace3.frame_range)[1])
                at_least_one_overlap_range_len = max_overlap_range - min_overlap_range + 1
                double_overlap_range = dictionary[picked_key]

                print(f"Range of at least one overlap: [{min_overlap_range}, {max_overlap_range}]")
                print(f"Range of double overlap: {double_overlap_range}")

                ## Show the plots and the video
                if show:
                    ## TODO maybe comment the following plot
                    # scatter_detection(traces, whole_frame_range)
                    scatter_detection([trace1, trace2, trace3], [min_trace_range - 200, max_trace_range + 200], show_trace_index=False, subtitle=f"Triplet {picked_key[0]}({trace1.trace_id}) blue, {picked_key[1]}({trace2.trace_id}) orange, {picked_key[2]}({trace3.trace_id}) green.")
                    # check that there are traces in frame range [min_trace_range - 200, max_trace_range + 200]
                    if (picked_key[0] > 0 and any(traces[f].frame_range[1] > min_trace_range - 200 for f in range(picked_key[0]))) or (picked_key[2] < len(traces)-1 and traces[picked_key[2]+1].frame_range[0] < max_trace_range + 200):
                        scatter_detection(traces, [min_trace_range - 200, max_trace_range + 200], from_to_frame=[min_trace_range, max_trace_range], show_trace_index=False,
                                          subtitle=f"Triplet {picked_key[0]}({trace1.trace_id}), {picked_key[1]}({trace2.trace_id}), {picked_key[2]}({trace3.trace_id}).")
                    ## show position
                    # show_plot_locations([trace1, trace2, trace3], whole_frame_range=[0, 0], from_to_frame=[min_overlap_range - round(at_least_one_overlap_range_len*0.1), max_overlap_range + round(at_least_one_overlap_range_len*0.1)],
                    show_plot_locations([trace1, trace2, trace3], whole_frame_range=[0, 0], from_to_frame=[min_overlap_range-15, max_overlap_range+15],
                                        subtitle=f"Triplet {picked_key[0]}({trace1.trace_id}) blue,{picked_key[1]}({trace2.trace_id}) orange,{picked_key[2]}({trace3.trace_id}) green.",
                                        silent=True)
                    # check that there are traces in the frame range
                    ## TODO maybe comment the following plot
                    if not input_video and show_all_plots:
                        if (picked_key[0] > 0 and any(traces[f].frame_range[1] > min_overlap_range - round(at_least_one_overlap_range_len * 0.1) for f in range(picked_key[0]))) or \
                                (picked_key[2] < len(traces) - 1 and traces[picked_key[2] + 1].frame_range[0] < max_overlap_range + round(at_least_one_overlap_range_len * 0.1)):
                            show_plot_locations(traces, whole_frame_range=[0, 0], from_to_frame=[min_overlap_range - round(at_least_one_overlap_range_len * 0.1),
                                                                                                 max_overlap_range + round(at_least_one_overlap_range_len * 0.1)],
                                                subtitle=f"Triplet {picked_key[0]}({trace1.trace_id}) blue, {picked_key[1]}({trace2.trace_id}) orange, {picked_key[2]}({trace3.trace_id}) green.",
                                                silent=True)
                    ## show the overlap
                    ## TODO maybe comment the following plot
                    if not input_video and show_all_plots:
                        show_overlaps([trace1, trace2, trace3], from_to_frame=True, show_overlap_indices=False, subtitle=f"Triplet {picked_key[0]}({trace1.trace_id}),{picked_key[1]}({trace2.trace_id}),{picked_key[2]}({trace3.trace_id}).")

                ## show frames of the video
                if input_video:
                    # show_video(input_video, traces=(), frame_range=(), video_speed=0.1, wait=False, points=(), video_params=True)
                    show_video(input_video, [trace1, trace2, trace3], frame_range=margin_range(double_overlap_range, 15), video_speed=0.01, wait=True, video_params=video_params)

                # Ask whether we should merge any of these traces
                if input_video:
                    to_merge_by_user = input("Are we gonna merge any of the shown traces? (yes or no) (press l to see longer video):")

                    if "l" in to_merge_by_user:
                        # to_show_longer_video = input("Do you want to see longer video? (yes or no):")
                        show_video(input_video, [trace1, trace2, trace3], frame_range=[min_overlap_range - 15, max_overlap_range + 15], video_speed=0.01, wait=True, video_params=video_params)
                        to_merge_by_user = input("Merge these traces now? (yes or no)")
                else:
                    to_merge_by_user = input("Are we gonna merge any of the shown traces? (yes or no):")

                if "y" in to_merge_by_user.lower():
                    # Ask for the index of the first trace to be merged and verify it
                    first_trace_to_merge = input("Write an index of one of the traces to be merged (number before the bracket):")
                    try:
                        first_trace_to_merge = int(first_trace_to_merge)
                    except ValueError:
                        print(colored("Not selected any trace to be merged. Skipping this triplet.", "red"))
                        continue
                    if first_trace_to_merge not in picked_key:
                        print(colored("Selected trace not in the triplet. Skipping it.", "red"))
                        continue

                    # Ask for the index of the second trace to be merged and verify it
                    second_trace_to_merge = input(
                        "Write an index of the other trace to be merged (number before the bracket):")
                    try:
                        second_trace_to_merge = int(second_trace_to_merge)
                    except ValueError:
                        print(colored("Not selected any trace to be merged. Skipping this triplet.", "red"))
                        continue
                    if second_trace_to_merge not in picked_key:
                        print(colored("Selected trace not in the triplet. Skipping it.", "red"))
                        continue
                    user_merging = True

                    # Find the trace which is not to be merged (the one not picked)
                    for trace_index in picked_key:
                        if trace_index != first_trace_to_merge and trace_index != second_trace_to_merge:
                            trace_index_to_omit = trace_index
                    trace_index_to_omit = picked_key.index(trace_index_to_omit)
                else:
                    user_merging = False
                    print(colored("Not merging this triplet.", "red"))

                # Ask to delete a trace
                spam = ask_to_delete_a_trace(traces, input_video, picked_key, video_params=video_params)
                if spam:
                    # add the traces to be deleted
                    traces_indices_to_be_removed.extend(spam)

                    if not user_merging:
                        # Actually delete the given traces now
                        for index in traces_indices_to_be_removed:
                            removed_traces.append(traces[index])
                        delete_indices(traces_indices_to_be_removed, traces, debug=False)
                        traces_indices_to_be_removed = []

                        # Continue searching for triplets
                        continue
                elif user_merging is False:
                    skipped_triplets_indices.append(picked_key)
                    if all(f in skipped_triplets_indices for f in dictionary.keys()):
                        go_next = False
                    continue

                # answer = input("Force merge these? Will not ask on the distance of the selected traces. (yes or no)")
                # if any(answer.lower() == f for f in ["yes", 'y', '1', 'ye', '6']):
                #     force_merge = True

            ## Remove the selected index - trace_index_to_omit - from the triplet of traces
            trace1, trace2, trace1_index, trace2_index = remove_a_trace_out_of_three(trace1, trace2, trace3, trace1_index, trace2_index, trace3_index, trace_index_to_omit)
            # Get the overlap
            pair_overlap_range = get_overlap(trace1.frame_range, trace2.frame_range)

            ## ACTUAL DECISION WHETHER TO MERGE
            if not guided:
                to_merge, use_shift = check_to_merge_two_overlapping_traces(traces, trace1, trace2, trace1_index,
                                                                            trace2_index,
                                                                            pair_overlap_range, shift=shift, show=False,
                                                                            silent=silent, debug=debug,
                                                                            input_video=input_video,
                                                                            video_params=video_params)
            if user_merging or to_merge:
                # Merge these two traces
                merge_two_overlapping_traces(trace1, trace2, trace1_index, trace2_index, silent=silent, debug=debug)

                # Remove the merged trace
                if debug:
                    print(colored(f"Will delete trace {trace2_index}({trace2.trace_id}).", "blue"))
                    print()
                del traces[trace2_index]
                go_next = False
            else:
                # NOT Merge these two traces
                go_next = True
                del dictionary[picked_key]

            if show:
                try:
                    scatter_detection(traces, subtitle=f"after merging overlapping traces {trace1_index} of id {trace1.trace_id} and {trace2_index} of id {trace2.trace_id}.")
                except UnboundLocalError:
                    pass

    print(colored(f"Returning {len(traces)} traces, {len(removed_traces)} removed, "
                  f"{starting_number_of_traces - len(traces) + len(removed_traces)} merged. "
                  f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
    return traces, removed_traces


def merge_triplets_by_partition(traces, shift=False, silent=False, debug=False, do_count=False, input_video=False, video_params=False):
    """ Merges traces triplets
        # Puts traces together such that all the agents but three are being tracked.

        :arg traces: (list): list of traces
        :arg shift: (False ir int): if False, no shift is used, else shift upto the given value is used to compare the traces
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :arg do_count: (bool): flag whether to count the numbers of events occurring
        :arg input_video: (str or bool): if set, path to the input video
        :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
        :returns: traces: (list): list of concatenated Traces
    """
    print(colored("MERGE OVERLAPPING TRIPLET TRACES - by partition", "blue"))
    # Initiation
    start_time = time()
    starting_number_of_traces = len(traces)
    pairs_of_traces_indices_to_merge = []
    ids_of_traces_to_be_merged = []

    # if do_count:
    #     set_single_run_seen_overlaps(0)
    #     set_single_run_allowed_overlaps_count(0)
    #     set_single_run_seen_overlaps_deleted(0)

    # Compute frame range partition by number of traces for each segment
    interval_to_traces_count = partition_frame_range_by_number_of_traces(traces)
    traces_count_to_intervals = reverse_partition_frame_range_by_number_of_traces(interval_to_traces_count)

    # try:
    #     set_single_run_seen_overlaps(len(traces_count_to_intervals[2]))
    # except KeyError:
    #     set_single_run_seen_overlaps(0)

    try:
        intervals = copy(traces_count_to_intervals[3])
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

        assert len(traces_subset) == 3
        assert len(traces_subset_indices) == 3

        # Get names

        trace1 = traces_subset[0]
        trace2 = traces_subset[1]
        trace3 = traces_subset[2]

        trace1_index = traces_subset_indices[0]
        trace2_index = traces_subset_indices[1]
        trace3_index = traces_subset_indices[2]

        # Remove the shortest trace
        trace1, trace2, trace1_index, trace2_index = remove_shortest_trace_out_of_three(trace1, trace2, trace3, trace1_index, trace2_index, trace3_index)

        # Check whether the pair is already there
        if (trace1_index, trace2_index) in pairs_of_traces_indices_to_merge:
            continue

        # Get the overlap
        overlap_range = get_overlap(trace1.frame_range, trace2.frame_range)

        ## ACTUAL DECISION WHETHER TO MERGE
        to_merge, use_shift = check_to_merge_two_overlapping_traces(traces, trace1, trace2, trace1_index, trace2_index,
                                                                    overlap_range, shift=shift, show=False, silent=silent,
                                                                    debug=debug, input_video=input_video, video_params=video_params)

        if to_merge is None:
            # set_single_run_seen_overlaps_deleted(get_single_run_seen_overlaps_deleted() + 1)
            continue
        elif to_merge is True:
            pairs_of_traces_indices_to_merge.append((trace1_index, trace2_index))
            ids_of_traces_to_be_merged.append((trace1.trace_id, trace2.trace_id))
        else:
            pass

    # ACTUALLY MERGE THE TRACES
    # set_single_run_allowed_overlaps_count(len(pairs_of_traces_indices_to_merge))
    merge_multiple_pairs_of_overlapping_traces(traces, pairs_of_traces_indices_to_merge, silent=silent, debug=debug)

    print(colored(f"Returning {len(traces)} traces, {starting_number_of_traces - len(traces)} merged. "
                  f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))

    return pairs_of_traces_indices_to_merge, ids_of_traces_to_be_merged


def merge_overlapping_triplets_brutto(traces, shift=False, guided=False, input_video=False, silent=False, debug=False,
                                      show=False, video_params=False):
    """ Merges traces with only a single overlap.
        # Puts traces together such that all the agents but one is being tracked.

        :arg traces: (list): list of traces
        :arg shift: (False ir int): if False, no shift is used, else shift upto the given value is used to compare the traces
        :arg whole_frame_range: [int, int]: frame range of the whole video (with margins)
        :arg guided: (bool): if True, user guided version would be run, this stops the whole analysis until a response is given
        :arg input_video: (str or bool): if set, path to the input video
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :arg show: (bool): if True plots are shown
        :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
        :returns: traces: (list): list of concatenated Traces
    """
    print(colored("MERGE OVERLAPPING TRIPLETS BRUTTO - using build", "blue"))
    start_time = time()
    starting_number_of_traces = len(traces)

    merge_pairs = []

    # Check whether there are at least 2 traces
    if len(traces) <= 2:
        if len(traces) == 2:
            print(colored("No triplet out of two traces. Skipping the rest of this analysis.\n", "yellow"))
            return
        if len(traces) == 1:
            print(colored("Cannot merge a single trace. Skipping the rest of this analysis.\n", "yellow"))
            return
        if len(traces) == 0:
            print(colored("Cannot merge no trace. Skipping the rest of this analysis.\n", "yellow"))
            return

    # Find all overlapping triplets
    dictionary = dictionary_of_m_overlaps_of_n_intervals(3, list(map(lambda x: x.frame_range, traces)), strict=True)
    if debug:
        print("dictionary", dictionary)

    if dictionary == {}:
        print(colored("Cannot merge any trace as there is no partial overlap of three traces.", "yellow"))
        print(colored(f"Returning {len(traces)} traces, {starting_number_of_traces - len(traces)} merged. "
                      f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
        return

    # Flag whether to try another pair of overlapping intervals
    for picked_key in dictionary.keys():
        trace1 = traces[picked_key[0]]
        trace2 = traces[picked_key[1]]
        trace3 = traces[picked_key[2]]

        trace1_index = picked_key[0]
        trace2_index = picked_key[1]
        trace3_index = picked_key[2]

        if is_there_full_overlap([trace1.frame_range, trace2.frame_range, trace3.frame_range]):
            continue

        overlap_range = dictionary[picked_key]

        ## Remove the trace with min len
        trace1, trace2, trace1_index, trace2_index = remove_shortest_trace_out_of_three(trace1, trace2, trace3, trace1_index, trace2_index, trace3_index)

        # This pair already to be validated, skipping it
        if (trace1_index, trace2_index) in merge_pairs:
            continue

        ## ACTUAL DECISION WHETHER TO MERGE
        to_merge, use_shift = check_to_merge_two_overlapping_traces(traces, trace1, trace2, trace1_index, trace2_index,
                                                                    overlap_range, shift=shift, show=False,
                                                                    silent=silent, debug=debug, input_video=input_video,
                                                                    video_params=video_params)
        # Manage the merge event
        if to_merge:
            # Merge these two traces later
            merge_pairs.append((trace1_index, trace2_index))

        if show:
            try:
                scatter_detection(traces, subtitle=f"after merging overlapping traces {trace1_index} of id {trace1.trace_id} and {trace2_index} of id {trace2.trace_id}.")
            except UnboundLocalError:
                pass

    ## MANAGE THE OVERLAPPING PAIRS
    pairs_to_skip = set()
    for index, pair in enumerate(merge_pairs):
        # there are no triplets of a single pair
        if len(merge_pairs) <= 1:
            break
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
            spam = list({traces[pair[0]], traces[pair[1]], traces[complementary_pair[0]], traces[complementary_pair[1]]})
            if len(spam) == 2:
                print()
            if dictionary_of_m_overlaps_of_n_intervals(3, list(map(lambda x: x.frame_range, spam)), strict=True, skip_whole_in=True):
                pairs_to_skip.add(pair)
                pairs_to_skip.add(complementary_pair)
                if debug:
                    print(f"getting rid of these pairs: {pair}, {complementary_pair}")

    # Get rid of the overlapping triplets
    merge_cut_pairs = list(filter(lambda x: x not in pairs_to_skip, merge_pairs))
    if debug:
        print(f"getting rid of these pairs: {pairs_to_skip}")

    # Actually merge the pure pairs
    merge_multiple_pairs_of_overlapping_traces(traces, merge_cut_pairs, silent=silent, debug=debug)

    print(colored(f"brut Returning {len(traces)} traces, {starting_number_of_traces - len(traces)} merged. "
                  f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
    return

