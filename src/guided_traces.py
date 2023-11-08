from termcolor import colored

import analyse
from misc import dictionary_of_m_overlaps_of_n_intervals, merge_sorted_dictionaries, margin_range, delete_indices, \
    range_len
from primal_traces_logic import get_gaps_of_traces
from traces_logic import ask_to_delete_a_trace, merge_two_overlapping_traces, merge_two_traces_with_gap, \
    ask_to_merge_two_traces_and_save_decision
# from visualise import scatter_detection, show_plot_locations


def full_guided(traces, input_video, show=True, silent=False, debug=False, video_params=False, to_skip_tuples=(), has_tracked_video=False):
    """ Goes a gap and overlap one by one in a user-guided manner

        :arg traces: (list): a list of Traces
        :arg input_video: (str or bool): if set, path to the input video
        :arg show: (bool): a flag whether to show the plot
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
        :arg to_skip_tuples: (tuple): pairs of trace ids, which to be skipped (as they have been already checked)
        :arg has_tracked_video: (bool): flag whether a video with tracking is available

        :returns: traces, removed_traces, to_skip_tuples
    """
    print(colored("VIDEO-GUIDED SOLVER", "blue"))
    if not input_video:
        print(colored("No video given, skipping this analysis. \n", "red"))
        return

    removed_traces = []
    traces_indices_to_be_removed = []
    last_edited_index = -1

    to_skip_tuples = list(to_skip_tuples)

    gaps = get_gaps_of_traces(traces, get_all_gaps=False)
    overlaps = dictionary_of_m_overlaps_of_n_intervals(2, list(map(lambda a: a.frame_range, traces)), strict=False, skip_whole_in=True)

    overlaps_and_gaps = merge_sorted_dictionaries(gaps, overlaps)

    for key in overlaps_and_gaps.keys():
        ## check whether we did not change the first trace of the pair
        if last_edited_index == key[0]:
            # Actually delete the given traces
            delete_indices(traces_indices_to_be_removed, traces, debug=False)
            traces, spam, to_skip_tuples = full_guided(traces, input_video, show=show, silent=silent, debug=debug, video_params=video_params, to_skip_tuples=to_skip_tuples, has_tracked_video=has_tracked_video)
            removed_traces.extend(spam)
            return traces, removed_traces, to_skip_tuples

        trace1 = traces[key[0]]
        trace2 = traces[key[1]]
        trace1_index = key[0]
        trace2_index = key[1]

        if [trace1.trace_id, trace2.trace_id] in to_skip_tuples:
            continue

        min_range = min([trace1.frame_range[0], trace2.frame_range[0]])
        max_range = max([trace1.frame_range[1], trace2.frame_range[1]])

        if key in overlaps.keys():
            is_overlap = True
            show_range = overlaps[key]
        else:
            is_overlap = False
            show_range = gaps[key]
            show_range = margin_range(show_range, max(100, 0.2*range_len(show_range)))
            show_range = list(map(round, show_range))
        print()
        print(colored(f"We have found a pair of {'overlapping' if is_overlap else 'gaping'} traces - {trace1.trace_id},{trace2.trace_id}.", "blue"))

        # frame_range = overlaps_and_gaps[key]

        # Video-guided visualisations
        # TODO MAYBE UNCOMMENT THE FOLLOWING LINES
        # scatter_detection([trace1, trace2], whole_frame_range=[min_range - 200, max_range + 200], show_trace_index=False,
        #                   subtitle=f"Triplet {trace1_index}({trace1.trace_id}) blue, {trace2_index}({trace2.trace_id}) orange.")
        # show_plot_locations([trace1, trace2], whole_frame_range=[0, 0], from_to_frame=show_range,
        #                     subtitle=f"Triplet {trace1_index}({trace1.trace_id}) blue, {trace2_index}({trace2.trace_id}) orange.",
        #                     silent=True)

        # to_merge = ask_to_merge_two_traces_and_save_decision(traces, [trace1, trace2], analyse.video_file, video_params=analyse.video_params, silent=silent, gaping=True)
        to_merge, video_was_shown = ask_to_merge_two_traces_and_save_decision(traces, [trace1, trace2], overlapping=is_overlap,
                                                                              gaping=not is_overlap)

        if to_merge is True:
            if is_overlap:
                merge_two_overlapping_traces(traces[key[0]], traces[key[1]], key[0], key[1], silent=silent, debug=debug)
            else:
                merge_two_traces_with_gap(traces[key[0]], traces[key[1]], silent=silent, debug=debug)
            traces_indices_to_be_removed.append(key[1])
            removed_traces.append(traces[key[1]])
            last_edited_index = key[1]
        elif video_was_shown:
            to_skip_tuples.append([trace1.trace_id, trace2.trace_id])

    # Actually delete the given traces now
    delete_indices(traces_indices_to_be_removed, traces, debug=False)

    return traces, removed_traces, to_skip_tuples
