from matplotlib import pyplot as plt


def scatter_detection(traces, subtitle=False):
    """ Creates a scatter plot of detected traces of each agent.

    :arg traces: (list): a list of Traces
    :arg subtitle: (string): subtitle of the plot
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    for index, trace in enumerate(traces):
        x = trace.frames_tracked
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
