from matplotlib import pyplot as plt

from traces_logic import get_gaps_of_traces
from misc import dictionary_of_m_overlaps_of_n_intervals


def show_all_traces(traces):
    """ Plots the traces in three plots, traces in x-axis and y-axis separately,
    time on horizontal axis in frame numbers. Last plot is the traces in x,y.

    :arg traces: (list): a list of Traces
    """
    for index, trace in enumerate(traces):
        if len(traces) == 1:
            figs = trace.show_trace_in_xy(show=True)
        elif index == 0:
            figs = trace.show_trace_in_xy(show=False)
        elif index < len(traces) - 1:
            figs = trace.show_trace_in_xy(figs, show=False)
        else:
            figs = trace.show_trace_in_xy(figs, show=True)


def scatter_detection(traces, subtitle=False):
    """ Creates a scatter plot of detected traces of each agent.

    :arg traces: (list): a list of Traces
    :arg subtitle: (string): subtitle of the plot
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    for index, trace in enumerate(traces):
        x = trace.frames_list
        y = [index] * len(x)
        ax1.scatter(x, y, alpha=0.5)
    plt.xlabel('Frame number')
    plt.ylabel('Agent id')
    title = f'Scatter plot of detections of individual agents over time.'
    if subtitle:
        assert isinstance(subtitle, str)
        plt.title(title + "\n" + subtitle)
    else:
        plt.title(title)
    plt.show()


def show_all_overlaps(traces, subtitle=False):
    """ Creates a scatter plot of overlaps of traces.

    :arg traces: (list): a list of Traces
    :arg subtitle: (string): subtitle of the plot
    """
    dictionary = dictionary_of_m_overlaps_of_n_intervals(2, list(map(lambda x: x.frame_range, traces)), while_not_in=True)
    overlaps = list(dictionary.keys())
    print("overlaps", overlaps)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    for index, overlap in enumerate(overlaps):
        x = list(range(overlap[0], overlap[1]+1))
        y = [index] * len(x)
        ax1.scatter(x, y, alpha=0.5)
    plt.xlabel('Frame number')
    plt.ylabel('Overlap id')
    title = f'Scatter plot of overlaps of two traces.'
    if subtitle:
        assert isinstance(subtitle, str)
        plt.title(title + "\n" + subtitle)
    else:
        plt.title(title)
    plt.show()


def show_all_gaps(traces, subtitle=False, debug=False):
    """ Creates a scatter plot of gaps of traces.

    :arg traces: (list): a list of Traces
    :arg subtitle: (string): subtitle of the plot
    :arg debug: (bool): if True extensive output is shown
    """
    pairs_of_gaps = get_gaps_of_traces(traces)

    if debug:
        print("pairs_of_gaps", pairs_of_gaps)
    gaps = list(pairs_of_gaps.keys())

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    for index, gap in enumerate(gaps):
        x = list(range(pairs_of_gaps[gap][0], pairs_of_gaps[gap][1]+1))
        y = [index] * len(x)
        ax1.scatter(x, y, alpha=0.5)
    plt.xlabel('Frame number')
    plt.ylabel('Gap id')
    title = f'Scatter plot of gaps of two traces.'
    if subtitle:
        assert isinstance(subtitle, str)
        plt.title(title + "\n" + subtitle)
    else:
        plt.title(title)
    plt.show()
