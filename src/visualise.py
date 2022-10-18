import math
from time import time
from _socket import gethostname
from termcolor import colored
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

from traces_logic import get_gaps_of_traces
from misc import dictionary_of_m_overlaps_of_n_intervals, nice_range_print


def show_plot_locations(traces, whole_frame_range, from_to_frame=False, subtitle=False):
    """ Plots the traces in three plots, traces in x-axis and y-axis separately,
    time on horizontal axis in frame numbers. Last plot is the traces in x,y.

    :arg traces: (list): a list of Traces
    :arg whole_frame_range: [int, int]: frame range of the whole video
    :arg from_to_frame: (list): if set, showing only frames in given range
    :arg subtitle: (string): subtitle of the plot
    """
    print(colored("SHOW PLOT LOCATIONS", "blue"))
    start_time = time()
    for index, trace in enumerate(traces):
        if len(traces) == 1:
            figs = trace.show_trace_in_xy(whole_frame_range, from_to_frame=from_to_frame, show=True, subtitle=subtitle)
        elif index == 0:
            figs = trace.show_trace_in_xy(whole_frame_range, from_to_frame=from_to_frame, show=False, subtitle=subtitle)
        elif index < len(traces) - 1:
            figs = trace.show_trace_in_xy(whole_frame_range, from_to_frame=from_to_frame, where=figs, show=False, subtitle=subtitle)
        else:
            figs = trace.show_trace_in_xy(whole_frame_range, from_to_frame=from_to_frame, where=figs, show=True, subtitle=subtitle)

    print(colored(f"Showing location of {len(traces)} traces, It took {gethostname()} {round(time() - start_time, 3)} seconds.\n", "yellow"))


def scatter_detection(traces, whole_frame_range, from_to_frame=False, subtitle=False, show_trace_index=True, show_trace_range=True):
    """ Creates a scatter plot of detected traces of each agent.

    :arg traces: (list): a list of Traces
    :arg whole_frame_range: [int, int]: frame range of the whole video
    :arg from_to_frame: (list): if set, showing only frames in given range
    :arg subtitle: (string): subtitle of the plot
    :arg show_trace_index: (bool): if True trace index is shown above the trace
    :arg show_trace_range: (bool): if True frame number of beginning af the trace and end of the trace is shown above the trace
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    if len(traces) > 100:
        fontsize = 0
    elif len(traces) > 60:
        fontsize = 5
    elif len(traces) > 30:
        fontsize = 6
    elif len(traces) > 20:
        fontsize = 8
    else:
        fontsize = 10

    for index, trace in enumerate(traces):
        x = trace.frames_list
        y = [index] * len(x)
        ax1.scatter(x, y, alpha=0.5)
        if show_trace_index:
            if len(traces) > 5:
                # ax1.text((trace.frame_range[0] + trace.frame_range[1]) / 2, y[0]-0.5, trace.trace_id, fontsize=fontsize)
                ax1.text((trace.frame_range[0] + trace.frame_range[1]) / 2, y[0] - 0.5, f"{index}({trace.trace_id})", fontsize=fontsize)
            else:
                # ax1.text((trace.frame_range[0] + trace.frame_range[1]) / 2, y[0] - 0.3/(6-len(traces)), trace.trace_id, fontsize=fontsize)
                ax1.text((trace.frame_range[0] + trace.frame_range[1]) / 2, y[0] - 0.3 / (6 - len(traces)), f"{index}({trace.trace_id})", fontsize=fontsize)
        if show_trace_range:
            if trace.frame_range_len < 5000:
                ax1.text(trace.frame_range[0], y[0], f"{nice_range_print(trace.frame_range)} [{trace.frame_range_len}]", fontsize=fontsize)
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
    title = f'Scatter plot of detections of individual agents over time.'
    if subtitle:
        assert isinstance(subtitle, str)
        plt.title(title + "\n" + subtitle + f" {len(traces)} traces.")
    else:
        plt.title(title + f"\n{len(traces)} traces.")
    plt.show()


def show_overlaps(traces, whole_frame_range, skip_whole_in=False, subtitle=False, silent=False, debug=False):
    """ Creates a scatter plot of overlaps of traces.

    :arg traces: (list): a list of Traces
    :arg whole_frame_range: [int, int]: frame range of the whole video
    :arg skip_whole_in: (bool): if True skipping the intervals which are overlapping with whole range
    :arg subtitle: (string): subtitle of the plot
    :arg silent: (bool): if True no output is shown
    :arg debug: (bool): if True extensive output is shown
    """
    # Check
    if len(traces) < 2:
        # print(colored("There is only one/no trace, skipping this analysis.\n", "yellow"))
        return

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    if len(traces) >= 2:
        # get dictionary of overlaps of two traces: pair of traces indices -> overlap frame range
        dictionary = dictionary_of_m_overlaps_of_n_intervals(2, list(map(lambda x: x.frame_range, traces)), skip_whole_in=skip_whole_in)
        overlaps = list(dictionary.keys())
        if debug:
            print("dictionary", dictionary)
            print("overlaps", overlaps)

        for index, overlap in enumerate(overlaps):
            x = list(range(dictionary[overlap][0], dictionary[overlap][1]+1))
            y = [index] * len(x)
            ax1.scatter(x, y, alpha=0.5)
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax1.set_xlim(whole_frame_range)
    plt.xlabel('Frame number')
    plt.ylabel('Overlap id')
    title = f'Scatter plot of overlaps of two traces.'
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
        :arg silent: (bool): if True no output is shown
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
    title = f'Scatter plot of the distance of the overlapping section (blue). \n Distance of two border frames when merged cutting trace {trace1.trace_id} (left red) \n or cutting trace {trace2.trace_id} (right red).'

    distances2 = []
    distances2.append(math.dist(trace1.locations[start_index1 - 1], trace2.locations[0]))
    distances2.append(math.dist(trace1.locations[-1], trace2.locations[end_index2 + 1]))
    ax1.scatter([x[0] - 1, x[-1] + 1], distances2, c="r")

    plt.title(title)
    plt.tight_layout()
    plt.show()


def show_gaps(traces, whole_frame_range, show_all_gaps=False, subtitle=False, silent=False, debug=False):
    """ Creates a scatter plot of gaps of traces.

    :arg traces: (list): a list of Traces
    :arg whole_frame_range: [int, int]: frame range of the whole video
    :arg show_all_gaps: (bool) if True shows all gaps
    :arg subtitle: (string): subtitle of the plot
    :arg silent: (bool): if True no output is shown
    :arg debug: (bool): if True extensive output is shown
    """
    # Check
    if len(traces) < 2:
        # print(colored("There is only one/no trace, skipping this analysis.\n", "yellow"))
        return

    pairs_of_gaps = get_gaps_of_traces(traces, get_all_gaps=show_all_gaps)

    if debug:
        print("pairs_of_gaps", pairs_of_gaps)
    gaps = list(pairs_of_gaps.keys())

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    for index, gap in enumerate(gaps):
        x = list(range(pairs_of_gaps[gap][0], pairs_of_gaps[gap][1]+1))
        y = [index] * len(x)
        ax1.scatter(x, y, alpha=0.5)
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax1.set_xlim(whole_frame_range)
    plt.xlabel('Frame number')
    plt.ylabel('Gap id')
    title = f'Scatter plot of {"all " if show_all_gaps else ""}gaps of two traces.'
    if subtitle:
        assert isinstance(subtitle, str)
        plt.title(title + "\n" + subtitle)
    else:
        plt.title(title)
    plt.show()
