from termcolor import colored

from misc import dictionary_of_m_overlaps_of_n_intervals, merge_sorted_dictionaries, margin_range, delete_indices, \
    range_len
from traces_logic import get_gaps_of_traces, ask_to_delete_a_trace, merge_two_overlapping_traces, merge_two_traces_with_gap
from video import show_video
from visualise import scatter_detection, show_plot_locations


def full_guided(traces, input_video, show=True, silent=False, debug=False, video_params=False):
    """ Goes a gap and overlap one by one in a user-guided manner

        :arg traces: (list): a list of Traces
        :arg input_video: (str or bool): if set, path to the input video
        :arg show: (bool): a flag whether to show the plot
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
    """
    print(colored("VIDEO-GUIDED SOLVER", "blue"))
    if not input_video:
        print(colored("No video given, skipping this analysis. \n"))
        return

    removed_traces = []
    traces_indices_to_be_removed = []
    last_edited_index = -1

    gaps = get_gaps_of_traces(traces, get_all_gaps=False)
    overlaps = dictionary_of_m_overlaps_of_n_intervals(2, list(map(lambda a: a.frame_range, traces)), skip_whole_in=True)

    overlaps_and_gaps = merge_sorted_dictionaries(gaps, overlaps)

    for key in overlaps_and_gaps.keys():
        ## check whether we did not change the first trace of the pair
        if last_edited_index == key[0]:
            # Actually delete the given traces
            delete_indices(traces_indices_to_be_removed, traces, debug=False)
            traces, spam = full_guided(traces, input_video, show=show, silent=silent, debug=debug, video_params=video_params)
            removed_traces.extend(spam)
            return traces, removed_traces

        trace1 = traces[key[0]]
        trace2 = traces[key[1]]
        trace1_index = key[0]
        trace2_index = key[1]

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
        print(colored(f"We have found a {'overlapping' if is_overlap else 'gaping'} traces {key[0]}({traces[key[0]].trace_id}),{key[1]}({traces[key[1]].trace_id}).", "blue"))

        frame_range = overlaps_and_gaps[key]

        # Video-guided visualisations
        scatter_detection([trace1, trace2], [min_range - 200, max_range + 200], show_trace_index=False,
                          subtitle=f"Triplet {trace1_index}({trace1.trace_id}) blue, {trace2_index}({trace2.trace_id}) orange.")
        show_plot_locations([trace1, trace2], [0, 0], from_to_frame=show_range,
                            subtitle=f"Triplet {trace1_index}({trace1.trace_id}) blue,{trace2_index}({trace2.trace_id}) orange.",
                            silent=True)

        # show_video(input_video, traces=(), frame_range=(), video_speed=0.1, wait=False, points=(), video_params=True)
        # show_video(input_video=video_file, frame_range=[8000, 8500], wait=True, video_params=True)
        show_video(input_video=input_video, traces=[trace1, trace2], frame_range=margin_range(frame_range, 15), video_speed=0.02, wait=True, video_params=video_params)
        to_show_longer_video = input("Do you want to see longer video? (yes or no):")
        if "y" in to_show_longer_video.lower():
            show_video(input_video=input_video, traces=[trace1, trace2], frame_range=(trace1.frame_range[0] - 15, trace2.frame_range[1] + 15),
                       video_speed=0.02, wait=True, video_params=video_params)

        to_merge_by_user = input("Merge these traces? (yes or no):")
        if "n" in to_merge_by_user.lower():
            spam = ask_to_delete_a_trace(traces, input_video, key, video_params=video_params)
            if spam:
                traces_indices_to_be_removed.extend(spam)
                last_edited_index = spam[0]

        elif "y" in to_merge_by_user.lower():
            if is_overlap:
                merge_two_overlapping_traces(traces[key[0]], traces[key[1]], key[0], key[1], silent=silent, debug=debug)
            else:
                merge_two_traces_with_gap(traces[key[0]], traces[key[1]], silent=silent, debug=debug)
            traces_indices_to_be_removed.append(key[1])
            removed_traces.append(traces[key[1]])
            last_edited_index = key[1]

    # Actually delete the given traces now
    delete_indices(traces_indices_to_be_removed, traces, debug=False)

    return traces, removed_traces
