import math
import sys

from matplotlib import pyplot as plt
from termcolor import colored

from config import get_bee_max_step_len
from misc import is_in
from trace import Trace, merge_two_traces


def trim_out_additional_agents_over_long_traces(traces, population_size, debug=False):
    """ Trims out additional appearance of an agent when long traces are over here

    :arg traces (list) list of Traces
    :arg population_size (int) expected number of agents
    :arg debug (bool) if True extensive output is shown
    """
    print(colored("TRIM OUT ADDITIONAL AGENTS OVER A LONG TRACES", "blue"))
    ## obtain the ranges with the size of frame more than 100 where all the agents are being tracked
    ranges = []
    for index1, trace in enumerate(traces):
        assert isinstance(trace, Trace)
        trace.check_trace_consistency()
        ranges.append(trace.frame_range)
    ranges = sorted(ranges)

    if population_size == 2:
        ## CHECKING WHETHER THERE ARE TWO OVERLAPPING TRACES
        at_least_two_overlaps = []
        for index1, range1 in enumerate(ranges[:-1]):
            current_overlaps = []
            if debug:
                print()
            for index2, range2 in enumerate(ranges):
                if index1 == index2:  # Skip the same index
                    continue

                if range2[1] <= range1[0]:  # Skip the traces which end before start of this
                    continue

                if range2[0] >= range1[1]:  # Beginning of the further intervals is behind the end of current one
                    # We go through the set of overlapping intervals
                    if debug:
                        print("current interval:", range1)
                        print("The set of overlapping intervals:", current_overlaps)
                    i = -1
                    min_range = 0
                    # We search for the longest overlapping interval
                    for index3, range3 in enumerate(current_overlaps):
                        if len(range3) > min_range:
                            i = index3
                            min_range = len(range3)
                    if i == -1:
                        if debug:
                            print("there was no overlapping interval")
                        at_least_two_overlaps.append([])
                    else:
                        if debug:
                            print("picking the longest interval:", current_overlaps[i])
                        at_least_two_overlaps.append(current_overlaps[i])
                    # Skipping the intervals which starts further than this interval
                    break
                else:
                    # Check whether the beginning of the two intervals are overlapping
                    if max(range1[0], range2[0]) > min(range1[1], range2[1]):
                        print(colored(range1, "red"))
                        print(colored(range2, "red"))
                        print("range1[1]", range1[1])
                        print("range2[0]", range2[0])
                        print(range2[0] >= range1[1])
                    # Add the overlap to the list
                    current_overlaps.append([max(range1[0], range2[0]), min(range1[1], range2[1])])
                    continue
        if debug:
            print(at_least_two_overlaps)
        # Selecting indices to be deleted
        indices_to_be_deleted = []
        for index1, range1 in enumerate(at_least_two_overlaps):
            if index1 in indices_to_be_deleted:
                continue
            for index2, range2 in enumerate(at_least_two_overlaps):
                if index2 in indices_to_be_deleted:
                    continue
                if index1 == index2:
                    continue
                # Start of the second interval is beyond end of first, we move on
                if range2[0] > range1[1]:
                    break
                # Range2 is in Range1
                if range2[0] >= range1[0] and range2[1] <= range1[1]:
                    if debug:
                        print(f"range index {index2} with value {range2} is in range index {index1} with value {range1}")
                    indices_to_be_deleted.append(index2)
        # Remove duplicates in the list of overlapping traces
        if debug:
            print()
            print(indices_to_be_deleted)
        indices_to_be_deleted = list(
            reversed(sorted(list(set(indices_to_be_deleted)))))  # Remove duplicates, reverse sort
        if debug:
            print()
            print(indices_to_be_deleted)
        for index in indices_to_be_deleted:
            del at_least_two_overlaps[index]
    elif population_size == 1:
        at_least_two_overlaps = []
        for index1, range1 in enumerate(ranges):
            at_least_two_overlaps.append(range1)
    else:
        raise NotImplemented("I`m sorry Dave, I`m afraid I cannot do that.")

    # Remove intervals which are redundantly overlapping - being over at_least_two_overlaps
    if debug:
        print()
        print(at_least_two_overlaps)
    traces_indices_to_be_deleted = []
    for index, tracee in enumerate(traces):
        for range in at_least_two_overlaps:
            if is_in(tracee.frame_range, range, strict=True):
                traces_indices_to_be_deleted.append(index)
    traces_indices_to_be_deleted = list(reversed(sorted(list(set(traces_indices_to_be_deleted)))))
    for index in traces_indices_to_be_deleted:
        del traces[index]

    for trace in traces:
        trace.check_trace_consistency()

    print(colored(f"Returning traces of length {len(traces)}", "blue"))
    return traces


def put_traces_together(traces, population_size, debug=False):
    """ Puts traces together such that all the agents but one is being tracked

        :arg traces (list) list of traces
        :arg population_size (int) expected number of agents
        :arg debug (bool) if True extensive output is shown
    """
    print(colored("PUT TRACES TOGETHER", "blue"))
    ## params
    max_trace_gap = 500
    min_trace_length = 100

    ## code
    reappearence = track_reappearence(traces, show=False)
    if debug:
        print(len(traces))
        print(len(reappearence))

    trace_indices_to_trim = []

    video_range = [sys.maxsize, -sys.maxsize]

    for trace in traces:
        if trace.frame_range[0] < video_range[0]:
            video_range[0] = trace.frame_range[0]
        if trace.frame_range[1] > video_range[1]:
            video_range[1] = trace.frame_range[1]

    if debug:
        print(video_range)

    step_to = video_range[0]
    do_skip = False
    while step_to <= video_range[1]:
        next_steps_to = []
        indicies_in = []
        for index, trace in enumerate(traces):
            if index in trace_indices_to_trim:
                continue
            assert isinstance(trace, Trace)
            if trace.frame_range[0] <= step_to < trace.frame_range[1]:
                if debug:
                    print(colored(f"adding trace {index} of {trace.frame_range} to in between", "yellow"))
                next_steps_to.append(trace.frame_range[1])
                indicies_in.append(index)
            else:
                if debug:
                    print(colored(f"skipping trace {index} of {trace.frame_range}", "red"))
                continue
        if debug:
            print(colored(f"finished first cycle with next_steps_to:{next_steps_to}", "blue"))

        try:
            next_step_to = min(next_steps_to)
            print("next_steps_to: ", next_steps_to)
        except ValueError:
            print(f"Fixing empty next_steps_to while step_to: {step_to} and next_step_to:{next_step_to}")
            traces_after = 0
            for index3, trace3 in enumerate(traces):
                assert isinstance(trace3, Trace)
                # if trace3.frame_range[0] < step_to:
                if trace3.frame_range[0] < next_step_to:
                    continue
                else:
                    traces_after = traces_after + 1
                    next_step_to = trace3.frame_range[0]
                    next_steps_to.append(next_step_to)
                    step_to = next_step_to
                    print(f"FIXED next_step_to: {next_step_to}")
                    do_skip = True
                    break
            if traces_after == 0:
                do_skip = True

        if do_skip:
            do_skip = False
            if traces_after == 0:
                break
            else:
                continue

        spam = next_steps_to.index(next_step_to)
        index_to_go = indicies_in[spam]
        if debug:
            print("CHECKING")
            print("next_steps_to", next_steps_to)
            print("indicies_in", indicies_in)
            print("next_step_to", next_step_to)
            print("index_to_go", index_to_go)

        if len(next_steps_to) == population_size:
            step_to = next_step_to
            ## look for a mergeable trace
            print(colored("Gonna have a look for a mergeable traces", "blue"))
            for index2, trace2 in enumerate(traces):
                assert isinstance(trace2, Trace)
                if index2 in trace_indices_to_trim:
                    continue
                if trace2.frame_range[0] < step_to:
                    if debug:
                        print(colored(f"skipping trace {trace2.trace_id} which starts in {trace2.frame_range[0]}", "green"))
                    continue
                if trace2.frame_range[0] - step_to <= max_trace_gap and trace2.frame_range_len >= min_trace_length:
                    print(colored(f"MERGING TRACES {traces[index_to_go].trace_id} of frame {traces[index_to_go].frame_range} of length {traces[index_to_go].frame_range_len} and trace {trace2.trace_id} of range {trace2.frame_range} of length {trace2.frame_range_len}", "yellow"))
                    print(colored(f"the distance of traces in x,y is {math.dist(traces[index_to_go].locations[-1], trace2.locations[0])}", "yellow"))
                    print(colored(f"which is {math.dist(traces[index_to_go].locations[-1], trace2.locations[0]) / (trace2.frame_range[0] - traces[index_to_go].frame_range[-1])} per frame", "yellow"))
                    print(colored(f"the distance of traces in frames is {trace2.frame_range[0] - traces[index_to_go].frame_range[-1]}", "yellow"))
                    trace = merge_two_traces(traces[index_to_go], trace2)
                    traces[index_to_go] = trace
                    if debug:
                        print(trace)
                    trace_indices_to_trim.append(index2)
                    step_to = trace.frame_range[1]
                else:
                    print(colored(f"NOT MERGING TRACES {traces[index_to_go].trace_id} of frame {traces[index_to_go].frame_range} of length {traces[index_to_go].frame_range_len} and trace {trace2.trace_id} of range {trace2.frame_range} of length {trace2.frame_range_len}", "red"))
                    print(colored(f"the distance of traces in x,y is {math.dist(traces[index_to_go].locations[-1], trace2.locations[0])}", "red"))
                    print(colored(f"which is {math.dist(traces[index_to_go].locations[-1], trace2.locations[0]) / (trace2.frame_range[0] - traces[index_to_go].frame_range[-1])} per frame", "red"))
                    print(colored(f"the distance of traces in frames is {trace2.frame_range[0] - traces[index_to_go].frame_range[-1]}", "red"))
        else:
            step_to = next_step_to
        print(colored(f"jumping to step {step_to}", "blue"))

    print(f"Gonna delete the following traces: {trace_indices_to_trim}")
    for index in list(reversed(sorted(trace_indices_to_trim))):
        if debug:
            print(f"deleting trace {index}")
        del traces[index]

    print(colored(f"Returning traces of length {len(traces)}", "blue"))
    return traces


def single_trace_checker(traces):
    """ Checks a single trace.

    :arg traces: (list): a list of Traces
    """
    print(colored("SINGLE TRACE CHECKER", "blue"))
    for index, trace in enumerate(traces):
        print(colored("Single trace checker", "blue"))
        print(colored(f"Checking trace: {trace}", "blue"))
        if trace.trace_lenn == 0:
            print(colored("This trace has length of 0. Consider deleting this agent", "blue"))  ## this can be FP
        if trace.max_step_len > get_bee_max_step_len():
            print(colored(f"This agent has moved {get_bee_max_step_len()} in a single step, you might consider deleting it.", "blue"))


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


def track_reappearence(traces, show=True, debug=False):
    """ Tracks the time it takes for an agent to appear when one is lost

    :arg traces: (list): a list of Traces
    :arg show: (bool): a flag whether to show the plot
    :arg debug (bool) if True extensive output is shown
    """
    print(colored("TRACE REAPPEARENCE", "blue"))
    frames_of_loss = []
    for trace in traces:
        frames_of_loss.append(trace.frame_range[1])

    frames_of_loss = list(sorted(frames_of_loss))
    if debug:
        print("frames_of_loss", frames_of_loss)

    # for trace in traces:
    #     print(trace.frame_range[0])

    frames_of_reappearence = []
    for frame in frames_of_loss:
        for trace in traces:
            if trace.frame_range[0] < frame:
                continue
            else:
                frames_of_reappearence.append(trace.frame_range[0])
                break
    if debug:
        print("frames_of_reappearence", frames_of_reappearence)

    time_to_reappear = list(map(lambda x, y: y - x, frames_of_loss, frames_of_reappearence))
    if debug:
        print("time_to_reappear", time_to_reappear)

    if show:
        plt.hist(time_to_reappear, bins=20)
        plt.xlabel('Step size')
        plt.ylabel('Count of time to reappear')
        plt.title(f'Histogram of times to reappear.')
        plt.show()

    return time_to_reappear
