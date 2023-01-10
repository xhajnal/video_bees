import math
from time import time
from _socket import gethostname
from termcolor import colored
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

from trace import Trace
from traces_logic import get_gaps_of_traces, get_traces_from_range
from misc import dictionary_of_m_overlaps_of_n_intervals, nice_range_print


def get_fontsize(number_of_traces):
    if number_of_traces > 100:
        fontsize = 0
    elif number_of_traces > 60:
        fontsize = 5
    elif number_of_traces > 45:
        fontsize = 5
    elif number_of_traces > 30:
        fontsize = 6
    elif number_of_traces > 20:
        fontsize = 8
    else:
        fontsize = 10
    return fontsize


def show_plot_locations(traces, whole_frame_range, from_to_frame=False, show_middle_point=False, subtitle=False, silent=False, debug=False):
    """ Plots the traces in three plots, traces in x-axis and y-axis separately,
    time on horizontal axis in frame numbers. Last plot is the traces in x,y.

    :arg traces: (list): a list of Traces
    :arg whole_frame_range: [int, int]: frame range of the whole video (with margins) 
    :arg from_to_frame: (list): if given, showing only frames in given range
    :arg show_middle_point: (bool): if True, a point in the middle of the trace is highlighted
    :arg subtitle: (string): subtitle of the plot
    :arg silent: (bool) if True minimal output is shown
    :arg debug: (bool) if True extensive output is shown
    """
    if debug:
        print(colored("SHOW PLOT LOCATIONS", "blue"))
    start_time = time()
    for index, trace in enumerate(traces):
        if len(traces) == 1:
            figs = trace.show_trace_in_xy(whole_frame_range, from_to_frame=from_to_frame, show=True, show_middle_point=show_middle_point, subtitle=subtitle, silent=silent, debug=debug)
        elif index == 0:
            figs = trace.show_trace_in_xy(whole_frame_range, from_to_frame=from_to_frame, show=False, show_middle_point=show_middle_point, subtitle=subtitle, silent=silent, debug=debug)
        elif index < len(traces) - 1:
            figs = trace.show_trace_in_xy(whole_frame_range, from_to_frame=from_to_frame, where=figs, show_middle_point=show_middle_point, show=False, subtitle=subtitle, silent=silent, debug=debug)
        else:
            figs = trace.show_trace_in_xy(whole_frame_range, from_to_frame=from_to_frame, where=figs, show_middle_point=show_middle_point, show=True, subtitle=subtitle, silent=silent, debug=debug)

    if debug:
        print(colored(f"Showing location of {len(traces)} traces, It took {gethostname()} {round(time() - start_time, 3)} seconds.\n", "yellow"))


def scatter_detection(traces, whole_frame_range, from_to_frame=False, subtitle=False, show_trace_index=True,
                      show_trace_id=True, show_trace_range=True):
    """ Creates a scatter plot of detected traces of each agent.

    :arg traces: (list): a list of Traces
    :arg whole_frame_range: [int, int]: frame range of the whole video (with margins)
    :arg from_to_frame: (list): if set, showing only frames in given range
    :arg subtitle: (string): subtitle of the plot
    :arg show_trace_index: (bool): if True trace index is shown above the trace
    :arg show_trace_id: (bool): if True trace id is shown above the trace
    :arg show_trace_range: (bool): if True frame number of beginning af the trace and end of the trace is shown above the trace
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    fontsize = get_fontsize(len(traces))

    if from_to_frame:
        traces_to_show = get_traces_from_range(traces, from_to_frame)
    else:
        traces_to_show = traces

    vertical_margin = get_vertical_margin(len(traces))

    for index, trace in enumerate(traces_to_show):
        assert isinstance(trace, Trace)

        x = trace.frames_list
        y = [index] * len(x)
        ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax1.scatter(x, y, alpha=0.5)
        if show_trace_index or show_trace_id:
            if show_trace_index and show_trace_id:
                msg = f"{index}({trace.trace_id})"
            elif show_trace_index and not show_trace_id:
                msg = f"{index}"
            else:
                msg = f"({trace.trace_id})"

            ax1.text((trace.frame_range[0] + trace.frame_range[1]) / 2, y[0] - vertical_margin, msg, fontsize=fontsize)

        if show_trace_range:
            if trace.frame_range_len < 5000:
                ax1.text(trace.frame_range[1] + 0.035*(whole_frame_range[1] - whole_frame_range[0]), y[0] + vertical_margin/2, f"{nice_range_print(trace.frame_range)} [{trace.frame_range_len}]", fontsize=fontsize)
            else:
                ax1.text(trace.frame_range[0], y[0], trace.frame_range[0], fontsize=fontsize)
                ax1.text(trace.frame_range[1], y[0], f"{trace.frame_range[1]} [{trace.frame_range_len}]", fontsize=fontsize)
        x = trace.overlap_frames
        y = [index] * len(x)
        ax1.scatter(x, y, c="black")
        x = trace.gap_frames
        y = [index] * len(x)
        ax1.scatter(x, y, alpha=0.5, c="white", edgecolors="black")

    if from_to_frame is not False:
        ax1.set_xlim(from_to_frame)
    else:
        ax1.set_xlim(whole_frame_range)

    plt.xlabel('Frame number')
    plt.ylabel('Agent id')
    title = f'Timeline plot of TRACES.'
    if subtitle:
        assert isinstance(subtitle, str)
        plt.title(title + "\n" + subtitle + f"{' Showing' if from_to_frame else ''} {len(traces_to_show)} traces.")
    else:
        plt.title(title + f"\n{' Showing' if from_to_frame else ''} {len(traces_to_show)} traces.")
    plt.show()


def show_overlaps(traces, whole_frame_range, from_to_frame=False, skip_whole_in=False, subtitle=False, silent=False, debug=False,
                  show_overlap_indices=True, show_overlap_ids=True, show_overlap_range=True):
    """ Creates a scatter plot of overlaps of traces.

    :arg traces: (list): a list of Traces
    :arg whole_frame_range: [int, int]: frame range of the whole video (with margins)
    :arg from_to_frame: (list): if set, showing only frames in given range
    :arg skip_whole_in: (bool): if True skipping the intervals which are overlapping with whole range
    :arg subtitle: (string): subtitle of the plot
    :arg silent: (bool): if True minimal output is shown
    :arg debug: (bool): if True extensive output is shown
    :arg show_overlap_indices: (bool): if True trace indices are shown above the overlap
    :arg show_overlap_ids: (bool): if True trace id-s are shown above the overlap
    :arg show_overlap_range: (bool): if True frame number of beginning af the overlap and end of the overlap is shown above the overlap
    """
    # Check
    if len(traces) < 2:
        # print(colored("There is only one/no trace, skipping this analysis.\n", "yellow"))
        return

    fontsize = get_fontsize(len(traces))

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    if len(traces) >= 2:
        # get dictionary of overlaps of two traces: pair of traces indices -> overlap frame range
        dictionary = dictionary_of_m_overlaps_of_n_intervals(2, list(map(lambda a: a.frame_range, traces)), skip_whole_in=skip_whole_in)
        overlaps = list(dictionary.keys())

        # print(dictionary)
        # print(dictionary.values())
        if not dictionary.keys():
            return
        whole_overlap_range = [min(map(lambda a: a[0], dictionary.values())), max(map(lambda a: a[1], dictionary.values()))]

        vertical_margin = get_vertical_margin(len(overlaps))

        if debug:
            print("dictionary", dictionary)
            print("overlaps", overlaps)

        for index, overlap in enumerate(overlaps):
            overlap_range = dictionary[overlap]
            overlap_range_len = overlap_range[1] - overlap_range[0] + 1

            x = list(range(overlap_range[0], overlap_range[1]+1))
            y = [index] * len(x)
            ax1.scatter(x, y, alpha=0.5)

            if show_overlap_indices or show_overlap_ids:
                if show_overlap_indices and show_overlap_ids:
                    msg = f"{overlap[0]}({traces[overlap[0]].trace_id}), {overlap[1]}({traces[overlap[1]].trace_id})"
                elif show_overlap_indices and not show_overlap_ids:
                    msg = f"{overlap[0]}, {overlap[1]}"
                else:
                    msg = f"({traces[overlap[0]].trace_id}), ({traces[overlap[1]].trace_id})"

                # ax1.text((trace.frame_range[0] + trace.frame_range[1]) / 2, y[0]-0.5, trace.trace_id, fontsize=fontsize)
                ax1.text((overlap_range[0] + overlap_range[1]) / 2, y[0] - vertical_margin, msg, fontsize=fontsize)

            if show_overlap_range:
                if overlap_range_len < 5000:
                    ax1.text(overlap_range[0] + (overlap_range[1]-overlap_range[0])/2, y[0] + vertical_margin/2, f"{nice_range_print(overlap_range)} [{overlap_range_len}]",
                             fontsize=fontsize)
                else:
                    ax1.text(overlap_range[0], y[0], overlap_range[0], fontsize=fontsize)
                    ax1.text(overlap_range[1], y[0], f"{overlap_range[1]} [{overlap_range_len}]", fontsize=fontsize)

    if from_to_frame is not False:
        if from_to_frame is True and len(traces) >= 2:
            # print(whole_overlap_range)
            ax1.set_xlim(whole_overlap_range)
        else:
            ax1.set_xlim(from_to_frame)
    else:
        ax1.set_xlim(whole_frame_range)

    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel('Frame number')
    plt.ylabel('Overlap id')
    title = f'Scatter plot of OVERLAPS of two traces.'
    if subtitle:
        assert isinstance(subtitle, str)
        plt.title(title + "\n" + subtitle)
    else:
        plt.title(title)
    plt.show()


# TODO maybe make this more general
def show_overlap_distances(x, trace1, trace2, distances, start_index1, end_index2, silent=False, debug=False):
    """ Shows a scatter plot of distances between two traces point-by-point including distance of two point merger -
    when skipping the overlap of the first or the second trace.

        :arg x: (list): x axis - frame list subset
        :arg trace1: (Trace): the first trace to show
        :arg trace2: (Trace): the second trace to show
        :arg distances: (list of int): y-axis - list of distances of the two traces
        :arg start_index1: (int): starting index of overlap/showing of the first trace frame list
        :arg end_index2: (int): end index of overlap/showing of the second trace frame list
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    y = distances
    if debug:
        print("distance len", len(distances))
        print("x len", len(x))
    ax1.scatter(x, y, alpha=0.5)
    plt.xlabel('Overlapping frame numbers')
    plt.ylabel('Distance of the two traces')
    title = f'Scatter plot of the distance of the overlapping section (blue). \n Distance of two border frames when merged cutting trace ({trace1.trace_id}) (left red) \n or cutting trace ({trace2.trace_id}) (right red).'

    distances2 = []
    distances2.append(math.dist(trace1.locations[start_index1 - 1], trace2.locations[0]))
    distances2.append(math.dist(trace1.locations[-1], trace2.locations[end_index2 + 1]))
    ax1.scatter([x[0] - 1, x[-1] + 1], distances2, c="r")

    plt.title(title)
    plt.tight_layout()
    plt.show()


def show_gaps(traces, whole_frame_range, show_all_gaps=False, subtitle=False, silent=False, debug=False,
              show_gap_indices=True, show_gap_range=True):
    """ Creates a scatter plot of gaps of traces.

    :arg traces: (list): a list of Traces
    :arg whole_frame_range: [int, int]: frame range of the whole video (with margins)
    :arg show_all_gaps: (bool) if True shows all gaps
    :arg subtitle: (string): subtitle of the plot
    :arg silent: (bool): if True minimal output is shown
    :arg debug: (bool): if True extensive output is shown
    :arg show_gap_indices: (bool): if True trace indices is shown above the gap
    :arg show_gap_range: (bool): if True frame number of beginning af the gap and end of the gap is shown above the gap
    """
    # Check
    if len(traces) < 2:
        # print(colored("There is only one/no trace, skipping this analysis.\n", "yellow"))
        return

    dict_pairs_of_gaps = get_gaps_of_traces(traces, get_all_gaps=show_all_gaps)

    if debug:
        print("pairs_of_gaps", dict_pairs_of_gaps)
    gaps = list(dict_pairs_of_gaps.keys())

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    fontsize = get_fontsize(len(gaps))
    vertical_margin = get_vertical_margin(len(gaps))

    for index, gap in enumerate(gaps):
        gap_range_len = dict_pairs_of_gaps[gap][1] - dict_pairs_of_gaps[gap][0]
        gap_range = [dict_pairs_of_gaps[gap][0], dict_pairs_of_gaps[gap][1]]

        x = list(range(gap_range[0], gap_range[1]+1))
        y = [index] * len(x)
        ax1.scatter(x, y, alpha=0.5)

        if show_gap_indices:
            # ax1.text((trace.frame_range[0] + trace.frame_range[1]) / 2, y[0]-0.5, trace.trace_id, fontsize=fontsize)
            ax1.text((gap_range[0] + gap_range[1]) / 2, y[0] - vertical_margin, f"{gap[0]}({traces[gap[0]].trace_id}), {gap[1]}({traces[gap[1]].trace_id})", fontsize=fontsize)

        if show_gap_range:
            if gap_range_len < 5000:
                ax1.text(gap_range[0] + 700, y[0] + vertical_margin/2, f"{nice_range_print(gap_range)} [{gap_range_len}]", fontsize=fontsize)
            else:
                ax1.text(gap_range[0], y[0], gap_range[0], fontsize=fontsize)
                ax1.text(gap_range[1], y[0], f"{gap_range[1]} [{gap_range_len}]", fontsize=fontsize)

    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax1.set_xlim(whole_frame_range)
    plt.xlabel('Frame number')
    plt.ylabel('Gap id')
    title = f'Scatter plot of {"all " if show_all_gaps else ""}GAPS of two traces.'
    if subtitle:
        assert isinstance(subtitle, str)
        plt.title(title + "\n" + subtitle)
    else:
        plt.title(title)
    plt.show()


def get_vertical_margin(count):
    """ Returns vertical margin for the plots based on number of items in the plot."""
    return 0.5 if count > 5 else 0.3 / (7 - count)
