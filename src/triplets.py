from time import time
from _socket import gethostname
from termcolor import colored
from operator import countOf

from fake import get_whole_frame_range
from config import *
from cross_traces import compare_two_traces
from misc import is_in, delete_indices, dictionary_of_m_overlaps_of_n_intervals, get_overlap, flatten2, margin_range
from trace import Trace

from traces_logic import merge_two_overlapping_traces, ask_to_delete_a_trace
from video import show_video
from visualise import scatter_detection, show_plot_locations, show_overlaps


def merge_overlapping_triplets_of_traces(traces, population_size, guided=False, input_video=False,  silent=False, debug=False, show=False, show_all_plots=False, video_params=False):
    """ Puts traces together such that all the agents but one is being tracked.

        :arg traces (list) list of traces
        :arg whole_frame_range: [int, int]: frame range of the whole video (with margins)
        :arg population_size (int) expected number of agents
        :arg guided: (bool): if True, user guided version would be run, this stops the whole analysis until a response is given
        :arg input_video: (str or bool): if set, path to the input video
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :arg show: (bool): if True plots are shown
        :arg show_all_plots: (bool): if True all plots are shown
        :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
        :returns: traces: (list): list of concatenated Traces
    """
    print(colored("MERGE OVERLAPPING TRIPLETS OF TRACES", "blue"))
    start_time = time()

    # Obtained variables
    whole_frame_range = get_whole_frame_range()
    starting_number_of_traces = len(traces)

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
            keys = flatten2(tuple(dictionary.keys()))

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
                              f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
                return

            # Pick the smallest index
            pick_key = min(count_two)

            if debug:
                print("pick_key", pick_key)

            # Find the triplet of the smallest index which has two overlaps
            pick_key2 = None
            for key in dictionary.keys():
                # with the smallest index
                if pick_key in key:
                    pick_key2 = key
                    if debug:
                        print("pick_key2", pick_key2)
                    break
            if pick_key2 is None:
                go_next = False
                break

            # parse the traces from dict
            trace1 = traces[pick_key2[0]]
            assert isinstance(trace1, Trace)
            trace2 = traces[pick_key2[1]]
            assert isinstance(trace2, Trace)
            trace3 = traces[pick_key2[2]]
            assert isinstance(trace3, Trace)

            # if the picked traces are overlapping in whole range of one of the traces we delete it from the dictionary and move on
            if not guided and (is_in(trace1.frame_range, trace2.frame_range) or is_in(trace2.frame_range, trace1.frame_range) or
                               is_in(trace2.frame_range, trace3.frame_range) or is_in(trace3.frame_range, trace2.frame_range) or
                               is_in(trace1.frame_range, trace3.frame_range) or is_in(trace3.frame_range, trace1.frame_range)):
                if debug:
                    print("trace1.frame_range", trace1.frame_range)
                    print("trace2.frame_range", trace2.frame_range)
                    print("trace3.frame_range", trace3.frame_range)
                    print("Will delete ", dictionary[pick_key2])
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
                print(colored(f"We have found a triplet of overlapping traces {pick_key2[0]}({trace1.trace_id}),{pick_key2[1]}({trace2.trace_id}),{pick_key2[2]}({trace3.trace_id}). Please select a pair to merge.", "blue"))

                ## Compute the ranges
                min_trace_range = min([trace1.frame_range[0], trace2.frame_range[0], trace3.frame_range[0]])
                max_trace_range = max([trace1.frame_range[1], trace2.frame_range[1], trace3.frame_range[1]])
                min_overlap_range = min(get_overlap(trace1.frame_range, trace2.frame_range)[0], get_overlap(trace2.frame_range, trace3.frame_range)[0])
                max_overlap_range = max(get_overlap(trace1.frame_range, trace2.frame_range)[1], get_overlap(trace2.frame_range, trace3.frame_range)[1])
                at_least_one_overlap_range_len = max_overlap_range - min_overlap_range + 1
                double_overlap_range = dictionary[pick_key2]

                print(f"Range of at least one overlap: [{min_overlap_range}, {max_overlap_range}]")
                print(f"Range of double overlap: {double_overlap_range}")

                ## Show the plots and the video
                if show:
                    ## TODO maybe comment the following plot
                    # scatter_detection(traces, whole_frame_range)
                    scatter_detection([trace1, trace2, trace3], [min_trace_range - 200, max_trace_range + 200], show_trace_index=False, subtitle=f"Triplet {pick_key2[0]}({trace1.trace_id}) blue, {pick_key2[1]}({trace2.trace_id}) orange, {pick_key2[2]}({trace3.trace_id}) green.")
                    # check that there are traces in frame range [min_trace_range - 200, max_trace_range + 200]
                    if (pick_key2[0] > 0 and any(traces[f].frame_range[1] > min_trace_range - 200 for f in range(pick_key2[0]))) or (pick_key2[2] < len(traces)-1 and traces[pick_key2[2]+1].frame_range[0] < max_trace_range + 200):
                        scatter_detection(traces, [min_trace_range - 200, max_trace_range + 200], from_to_frame=[min_trace_range, max_trace_range], show_trace_index=False,
                                          subtitle=f"Triplet {pick_key2[0]}({trace1.trace_id}), {pick_key2[1]}({trace2.trace_id}), {pick_key2[2]}({trace3.trace_id}).")
                    ## show position
                    # show_plot_locations([trace1, trace2, trace3], whole_frame_range=[0, 0], from_to_frame=[min_overlap_range - round(at_least_one_overlap_range_len*0.1), max_overlap_range + round(at_least_one_overlap_range_len*0.1)],
                    show_plot_locations([trace1, trace2, trace3], whole_frame_range=[0, 0], from_to_frame=[min_overlap_range-15, max_overlap_range+15],
                                        subtitle=f"Triplet {pick_key2[0]}({trace1.trace_id}) blue,{pick_key2[1]}({trace2.trace_id}) orange,{pick_key2[2]}({trace3.trace_id}) green.",
                                        silent=True)
                    # check that there are traces in the frame range
                    ## TODO maybe comment the following plot
                    if not input_video and show_all_plots:
                        if (pick_key2[0] > 0 and any(traces[f].frame_range[1] > min_overlap_range - round(at_least_one_overlap_range_len * 0.1) for f in range(pick_key2[0]))) or \
                                (pick_key2[2] < len(traces) - 1 and traces[pick_key2[2] + 1].frame_range[0] < max_overlap_range + round(at_least_one_overlap_range_len * 0.1)):
                            show_plot_locations(traces, whole_frame_range=[0, 0], from_to_frame=[min_overlap_range - round(at_least_one_overlap_range_len * 0.1),
                                                                                                 max_overlap_range + round(at_least_one_overlap_range_len * 0.1)],
                                                subtitle=f"Triplet {pick_key2[0]}({trace1.trace_id}) blue, {pick_key2[1]}({trace2.trace_id}) orange, {pick_key2[2]}({trace3.trace_id}) green.",
                                                silent=True)
                    ## show the overlap
                    ## TODO maybe comment the following plot
                    if not input_video and show_all_plots:
                        show_overlaps([trace1, trace2, trace3], from_to_frame=True, show_overlap_indices=False, subtitle=f"Triplet {pick_key2[0]}({trace1.trace_id}),{pick_key2[1]}({trace2.trace_id}),{pick_key2[2]}({trace3.trace_id}).")

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
                    if first_trace_to_merge not in pick_key2:
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
                    if second_trace_to_merge not in pick_key2:
                        print(colored("Selected trace not in the triplet. Skipping it.", "red"))
                        continue
                    user_merging = True
                    force_merge = True

                    # Find the trace which is not to be merged (the one not picked)
                    for trace_index in pick_key2:
                        if trace_index != first_trace_to_merge and trace_index != second_trace_to_merge:
                            trace_index_to_omit = trace_index
                    trace_index_to_omit = pick_key2.index(trace_index_to_omit)
                else:
                    user_merging = False
                    print(colored("Not merging this triplet.", "red"))

                # Ask to delete a trace
                spam = ask_to_delete_a_trace(traces, input_video, pick_key2, video_params=video_params)
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
                    skipped_triplets_indices.append(pick_key2)
                    if all(f in skipped_triplets_indices for f in dictionary.keys()):
                        go_next = False
                    continue

                # answer = input("Force merge these? Will not ask on the distance of the selected traces. (yes or no)")
                # if any(answer.lower() == f for f in ["yes", 'y', '1', 'ye', '6']):
                #     force_merge = True

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
            if not force_merge and distances is not None and any(list(map(lambda x: x > get_max_step_distance_to_merge_overlapping_traces(), distances))):
                go_next = True
                to_merge = False
                force_merge = False
                reason = f"single huge distance (>{get_max_step_distance_to_merge_overlapping_traces()})"

                # delete traces which have been picked to be deleted and merged as well
                delete_indices(traces_indices_to_be_removed, traces, debug=False)
                traces_indices_to_be_removed = []

                # the distance of the traces is greater than the given threshold, we move on
                del dictionary[pick_key2]

                skipped_triplets_indices.append(pick_key2)
                if all(f in skipped_triplets_indices for f in dictionary.keys()):
                    go_next = False
            else:
                # Merge these two traces
                to_merge = True
                merge_two_overlapping_traces(trace1, trace2, duplet_indices[0], duplet_indices[1],
                                             silent=silent, debug=debug)
                # Remove the merged trace
                if debug:
                    # print(colored(f"Will delete trace {trace2_id}.", "blue"))
                    print(colored(f"Will delete trace {duplet_indices[1]}({trace2_id}).", "blue"))
                    print()

                traces_indices_to_be_removed.append(duplet_indices[1])
                traces_indices_to_be_removed = list(set(traces_indices_to_be_removed))
                delete_indices(traces_indices_to_be_removed, traces, debug=False)
                traces_indices_to_be_removed = []

                # Show scatter plot of traces having two traces merged
                go_next = False

            if not silent:
                msg = f"{'' if to_merge else 'NOT '}MERGING THE OVERLAPPING TRACES {'' if to_merge else '(' + reason + ') '}"
                print(colored(msg, "yellow") if to_merge else colored(msg, "red"))
                print()

            if show:
                try:
                    scatter_detection(traces, subtitle=f"after merging overlapping traces {duplet_indices[0]} of id {trace1.trace_id} and {duplet_indices[1]} of id {trace2_id}.")
                except UnboundLocalError:
                    pass

    print(colored(f"Returning {len(traces)} traces, {len(removed_traces)} removed, "
                  f"{starting_number_of_traces - len(traces) + len(removed_traces)} merged. "
                  f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
    return traces, removed_traces
