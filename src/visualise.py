from matplotlib import pyplot as plt


def scatter_detection(traces):
    """ Creates a scatter plot of detected traces of each agent.

    :arg traces: (list): a list of Traces
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    for index, trace in enumerate(traces):
        x = trace.frames_tracked
        y = [index] * len(x)
        ax1.scatter(x, y, alpha=0.5)
    plt.xlabel('Frame number')
    plt.ylabel('Agent id')
    plt.title(f'Scatter plot of detections of individual agents over time.')
    plt.show()
