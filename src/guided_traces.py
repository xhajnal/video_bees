from termcolor import colored

import analyse
from misc import dictionary_of_m_overlaps_of_n_intervals, merge_sorted_dictionaries, margin_range, delete_indices, \
    range_len, get_overlap
from primal_traces_logic import get_gaps_of_traces
from traces_logic import ask_to_delete_a_trace, merge_two_overlapping_traces, merge_two_traces_with_gap, \
    ask_to_merge_two_traces_and_save_decision
# from visualise import scatter_detection, show_plot_locations


def full_guided(traces, input_video, show=True, silent=False, debug=False, video_params=False, has_tracked_video=False):
    """ Goes a gap and overlap one by one in a user-guided manner

        :arg traces: (list): a list of Traces
        :arg input_video: (str or bool): if set, path to the input video
        :arg show: (bool): a flag whether to show the plot
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
        :arg has_tracked_video: (bool): flag whether a video with tracking is available

        :returns: traces, removed_traces, to_skip_tuples
    """
    print(colored("VIDEO-GUIDED SOLVER", "blue"))
    if not input_video:
        print(colored("No video given, skipping this analysis. \n", "red"))
        return

    traces_indices_to_be_removed = []    # indices of traces to be deleted
    removed_traces = []                  # traces removed
    skip_this = False

    gaps = get_gaps_of_traces(list(map(lambda a: a.frame_range, traces)), debug=debug)
    overlaps = dictionary_of_m_overlaps_of_n_intervals(2, list(map(lambda a: a.frame_range, traces)), strict=False, skip_whole_in=True)

    overlaps_and_gaps = merge_sorted_dictionaries(gaps, overlaps)

    for key in overlaps_and_gaps.keys():
        # Check whether any of the traces is not marked to be deleted
        for item in traces_indices_to_be_removed:
            if item == key[0] or item == key[1]:
                # print("this already deleted")
                skip_this = True

        if skip_this:
            skip_this = False
            continue

        try:
            trace1 = traces[key[0]]
        except IndexError as err:
            print("key[0]", key[0])
            raise err

        try:
            trace2 = traces[key[1]]
        except IndexError as err:
            print("key[1]", key[1])
            raise err
        
        # trace1_index = key[0]
        # trace2_index = key[1]

        # min_range = min([trace1.frame_range[0], trace2.frame_range[0]])
        # max_range = max([trace1.frame_range[1], trace2.frame_range[1]])

        is_overlap = get_overlap(trace1.frame_range, trace2.frame_range)

        print()
        print(colored(f"We have found a pair of {'overlapping' if is_overlap else 'gaping'} traces - {trace1.trace_id},{trace2.trace_id}.  {trace1.frame_range}; {trace2.frame_range}", "blue"))

        # frame_range = overlaps_and_gaps[key]

        # Video-guided visualisations
        # TODO MAYBE UNCOMMENT THE FOLLOWING LINES
        # scatter_detection([trace1, trace2], whole_frame_range=[min_range - 200, max_range + 200], show_trace_index=False,
        #                   subtitle=f"Triplet {trace1_index}({trace1.trace_id}) blue, {trace2_index}({trace2.trace_id}) orange.")
        # show_plot_locations([trace1, trace2], whole_frame_range=[0, 0], from_to_frame=show_range,
        #                     subtitle=f"Triplet {trace1_index}({trace1.trace_id}) blue, {trace2_index}({trace2.trace_id}) orange.",
        #                     silent=True)

        ## Check all the traces have been processed
        if len(analyse.new_trace_ids_to_be_deleted) > 0:
            raise Exception("At some point we did not deal with new traces to be deleted.")

        to_merge, video_was_shown = ask_to_merge_two_traces_and_save_decision(traces, [trace1, trace2], overlapping=is_overlap, gaping=not is_overlap)

        ## Check for new traces to be deleted while video was shown
        for index, trace_id in analyse.new_trace_ids_to_be_deleted:
            if traces[index].trace_id == trace_id:
                traces_indices_to_be_removed.append(index)
                removed_traces.append(traces[index])
            else:
                raise Exception("While trying to delete a trace the traces changed.")
        analyse.new_trace_ids_to_be_deleted = []

        # for trace_id in analyse.new_trace_ids_to_be_deleted:
        #     for index, trace in enumerate(traces):
        #         if trace.trace_id == trace_id:
        #             traces_indices_to_be_removed.append(index)
        #             removed_traces.append(trace)
        #             break
        #         raise Exception(f"trace id {trace_id} not found in traces to be deleted")
        # analyse.new_trace_ids_to_be_deleted = []

        if to_merge is True:
            if is_overlap:
                merge_two_overlapping_traces(traces[key[0]], traces[key[1]], key[0], key[1], silent=silent, debug=debug)
            else:
                merge_two_traces_with_gap(traces[key[0]], traces[key[1]], silent=silent, debug=debug)
            traces_indices_to_be_removed.append(key[1])
            removed_traces.append(traces[key[1]])

    # Actually delete the given traces now
    delete_indices(traces_indices_to_be_removed, traces, debug=debug)

    return traces, removed_traces
