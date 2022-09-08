from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

from traces_logic import get_gaps_of_traces
from misc import dictionary_of_m_overlaps_of_n_intervals


def show_all_traces(traces, whole_frame_range):
    """ Plots the traces in three plots, traces in x-axis and y-axis separately,
    time on horizontal axis in frame numbers. Last plot is the traces in x,y.

    :arg traces: (list): a list of Traces
    :arg whole_frame_range: [int, int]: frame range of the whole video
    """
    for index, trace in enumerate(traces):
        if len(traces) == 1:
            figs = trace.show_trace_in_xy(whole_frame_range, show=True)
        elif index == 0:
            figs = trace.show_trace_in_xy(whole_frame_range, show=False)
        elif index < len(traces) - 1:
            figs = trace.show_trace_in_xy(whole_frame_range, where=figs, show=False)
        else:
            figs = trace.show_trace_in_xy(whole_frame_range, where=figs, show=True)


def scatter_detection(traces, whole_frame_range, subtitle=False):
    """ Creates a scatter plot of detected traces of each agent.

    :arg traces: (list): a list of Traces
    :arg whole_frame_range: [int, int]: frame range of the whole video
    :arg subtitle: (string): subtitle of the plot
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    for index, trace in enumerate(traces):
        x = trace.frames_list
        y = [index] * len(x)
        ax1.scatter(x, y, alpha=0.5)
    ax1.set_xlim(whole_frame_range)
    plt.xlabel('Frame number')
    plt.ylabel('Agent id')
    title = f'Scatter plot of detections of individual agents over time.'
    if subtitle:
        assert isinstance(subtitle, str)
        plt.title(title + "\n" + subtitle)
    else:
        plt.title(title)
    plt.show()


def show_overlaps(traces, whole_frame_range, subtitle=False, silent=False, debug=False):
    """ Creates a scatter plot of overlaps of traces.

    :arg traces: (list): a list of Traces
    :arg whole_frame_range: [int, int]: frame range of the whole video
    :arg subtitle: (string): subtitle of the plot
    :arg silent (bool) if True no output is shown
    :arg debug (bool) if True extensive output is shown
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    if len(traces) >= 2:
        dictionary = dictionary_of_m_overlaps_of_n_intervals(2, list(map(lambda x: x.frame_range, traces)), while_not_in=True)
        overlaps = list(dictionary.keys())
        if debug:
            print("overlaps", overlaps)
            print("dictionary.items()", dictionary.items())

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


def show_gaps(traces, whole_frame_range, show_all_gaps=False, subtitle=False, debug=False):
    """ Creates a scatter plot of gaps of traces.

    :arg traces: (list): a list of Traces
    :arg whole_frame_range: [int, int]: frame range of the whole video
    :arg show_all_gaps: (bool) if True shows all gaps
    :arg subtitle: (string): subtitle of the plot
    :arg debug: (bool): if True extensive output is shown
    """
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
