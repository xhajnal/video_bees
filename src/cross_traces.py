import math
import sys
from matplotlib import pyplot as plt
from termcolor import colored
from misc import is_in, delete_indices, m_overlaps_of_n_intervals, index_of_shortest_range, get_overlap
from trace import Trace, merge_two_traces
from scipy.interpolate import InterpolatedUnivariateSpline


def compare_two_traces(trace1, trace2):
    """ Compares two traces

    :arg trace1: Trace: first trace to be compared
    :arg trace2: Trace: second trace to be compared
    """
    print(colored("COMPARE TWO TRACES", "blue"))
    assert isinstance(trace1, Trace)
    assert isinstance(trace2, Trace)

    overlapping_range = get_overlap(trace1.frame_range, trace2.frame_range)
    if overlapping_range is False:
        print(colored(f"There is no overlap of trace {trace1.trace_id} and trace {trace2.trace_id}"))
        return None
    start_index1 = trace1.frames_tracked.index(overlapping_range[0])
    end_index1 = trace1.frames_tracked.index(overlapping_range[1])
    start_index2 = trace2.frames_tracked.index(overlapping_range[0])
    end_index2 = trace2.frames_tracked.index(overlapping_range[1])
    print("start_index1", start_index1)
    print("end_index1", end_index1)
    print("start_index2", start_index2)
    print("end_index2", end_index2)
    print()

    print("Showing the overlap frame by frame:")
    inter_index = 0
    distances = []
    first_trace_overlapping_frames = []
    for index in range(start_index1, end_index1+1):
        first_trace_overlapping_frames.append(index)
        print("index1", index)
        index2 = range(start_index2, end_index2+1)[inter_index]
        print("index2", index2)
        inter_index = inter_index + 1
        position1 = trace1.locations[index]
        position2 = trace2.locations[index2]
        print("position1", position1)
        print("position2", position2)
        distance = math.dist(position1, position2)
        print("distance of the positions", distance)
        distances.append(distance)
        print()

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    x = first_trace_overlapping_frames
    y = distances
    ax1.scatter(x, y, alpha=0.5)
    plt.xlabel('Frame number of the first trace')
    plt.ylabel('distance of the two races')
    title = f'Scatter plot of of the distance of the overlapping section.'
    plt.title(title)
    plt.show()

    print(f"The overlap of the traces is {end_index2 - start_index2} long and its distance is {sum(distances)} pointwise")


def trim_out_additional_agents_over_long_traces2(traces, population_size, debug=False):
    """ Trims out additional appearance of an agent when long traces are over here.

    :arg traces: (list): list of Traces
    :arg population_size: (int): expected number of agents
    :arg debug: (bool): if True extensive output is shown
    :returns: traces: (list): list of trimmed Traces
    """
    print(colored("TRIM OUT ADDITIONAL AGENTS OVER A LONG TRACES 2", "blue"))
    ranges = []
    for index1, trace in enumerate(traces):
        assert isinstance(trace, Trace)
        trace.check_trace_consistency()
        ranges.append(trace.frame_range)
    ranges = sorted(ranges)
    dictionary = m_overlaps_of_n_intervals(population_size + 1, ranges, strict=False, debug=False)

    indices_of_intervals_to_be_deleted = []

    for overlap in dictionary.keys():
        if debug:
            print(colored(f"Currently checking overlapping indices: {overlap}", "blue"))
        overlapping_ranges = []
        for interval_index in overlap:
            overlapping_ranges.append(ranges[interval_index])

        shortest_index = overlap[index_of_shortest_range(overlapping_ranges)]
        if debug:
            print(colored(f" Index_of_shortest_range: {shortest_index}", "blue"))
        shortest_range = ranges[shortest_index]

        to_be_deleted = True
        for range in overlapping_ranges:
            if debug:
                print(colored(f" Checking whether range index {shortest_index}, {shortest_range}, is in {range}", "blue"))
            if not is_in(shortest_range, range):
                to_be_deleted = False

        if to_be_deleted:
            if debug:
                print(colored(f"Gonna delete range index {shortest_index}, {shortest_range}", "yellow"))
            indices_of_intervals_to_be_deleted.append(shortest_index)

    print(colored(f"Indices_of_intervals_to_be_deleted: {indices_of_intervals_to_be_deleted}", "red"))
    traces = delete_indices(indices_of_intervals_to_be_deleted, traces)

    return traces


def trim_out_additional_agents_over_long_traces(traces, population_size, debug=False):
    """ Trims out additional appearance of an agent when long traces are over here.

    :arg traces: (list): list of Traces
    :arg population_size: (int): expected number of agents
    :arg debug: (bool): if True extensive output is shown
    :returns: traces: (list): list of trimmed Traces
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
        at_least_two_overlaps = delete_indices(indices_to_be_deleted, at_least_two_overlaps)
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
        for overlap_range in at_least_two_overlaps:
            if is_in(tracee.frame_range, overlap_range, strict=True):
                traces_indices_to_be_deleted.append(index)
    traces_indices_to_be_deleted = list(reversed(sorted(list(set(traces_indices_to_be_deleted)))))
    for index in traces_indices_to_be_deleted:
        del traces[index]

    for trace in traces:
        trace.check_trace_consistency()

    print(colored(f"Returning traces of length {len(traces)}", "green"))
    print()
    return traces


def put_traces_together(traces, population_size, debug=False):
    """ Puts traces together such that all the agents but one is being tracked.

    :arg traces (list) list of traces
    :arg population_size (int) expected number of agents
    :arg debug (bool) if True extensive output is shown
    :returns: traces: (list): list of concatenated Traces
    """
    print(colored("PUT TRACES TOGETHER", "blue"))
    ## params
    max_trace_gap = 500
    min_trace_length = 100

    ## code
    reappearance = track_reappearance(traces, show=False)
    if debug:
        print(len(traces))
        print(len(reappearance))

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
        indices_in = []
        for index, trace in enumerate(traces):
            if index in trace_indices_to_trim:
                continue
            assert isinstance(trace, Trace)
            if trace.frame_range[0] <= step_to < trace.frame_range[1]:
                if debug:
                    print(colored(f"adding trace {trace.trace_id} of {trace.frame_range} to in between", "yellow"))
                next_steps_to.append(trace.frame_range[1])
                indices_in.append(index)
            else:
                if debug:
                    print(colored(f"skipping trace {trace.trace_id} of {trace.frame_range}", "red"))
                continue
        if debug:
            print(colored(f"finished first cycle with next_steps_to:{next_steps_to}", "blue"))

        try:
            next_step_to = min(next_steps_to)
            if debug:
                print("next_steps_to: ", next_steps_to)
        except ValueError:
            if debug:
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
        index_to_go = indices_in[spam]
        if debug:
            print("CHECKING")
            print("next_steps_to", next_steps_to)
            print("indices_in", indices_in)
            print("next_step_to", next_step_to)
            print("index_to_go", index_to_go)

        if len(next_steps_to) == population_size:
            ## look for a mergeable trace
            print(colored(f"Gonna have a look for a mergeable traces from {step_to} till {next_step_to} (frame range)", "blue"))
            step_to = next_step_to
            for index2, trace2 in enumerate(traces):
                assert isinstance(trace2, Trace)
                if index2 in trace_indices_to_trim:
                    continue
                if trace2.frame_range[0] < step_to:
                    if debug:
                        print(colored(f"skipping trace {trace2.trace_id} which starts in {trace2.frame_range[0]}", "green"))
                    continue

                trace1 = traces[index_to_go]
                # EXTRAPOLATE TRACE
                frames = trace1.frames_tracked[-50:]  # last 50 frames
                x = list(map(lambda x: x[0], trace1.locations[-50:]))  # last 50 locations
                y = list(map(lambda y: y[1], trace1.locations[-50:]))
                splt_x = InterpolatedUnivariateSpline(frames, x, ext=0)  # extrapolator
                splt_y = InterpolatedUnivariateSpline(frames, y, ext=0)

                # COMPUTE DISTANCES AND REST
                dist_of_traces_in_frames = trace2.frame_range[0] - trace1.frame_range[-1]
                dist_of_traces_in_xy = math.dist(trace1.locations[-1], trace2.locations[0])
                extrapolated_point = [splt_x(trace1.frames_tracked[-1] + dist_of_traces_in_frames), splt_y(trace1.frames_tracked[-1] + dist_of_traces_in_frames)]
                dist_of_trace2_and_extrapolation =  math.dist(extrapolated_point, trace2.locations[0])

                # COMPUTE WHETHER THE TWO TRACES ARE "ALIGNED"
                spam = trace2.frame_range[0] - step_to <= max_trace_gap and trace2.frame_range_len >= min_trace_length
                msg = f"{'' if spam else 'NOT '}MERGING TRACES {trace1.trace_id} of " \
                      f"frame {trace1.frame_range} of length {trace1.frame_range_len} and " \
                      f"trace {trace2.trace_id} of range {trace2.frame_range} of " \
                      f"length {int(trace2.frame_range_len)} " \
                      f"the distance of traces in x,y is {round(dist_of_traces_in_xy, 3)} which is " \
                      f"{round(dist_of_traces_in_xy / (trace2.frame_range[0] - trace1.frame_range[-1]), 3)} per frame " \
                      f"the distance of traces in frames is {round(dist_of_traces_in_frames, 3)} " \
                      f"last point position: {trace1.locations[-1]} " \
                      f"the extrapolated point is {extrapolated_point} " \
                      f"the distance of extrapolated point to the second trace {round(dist_of_trace2_and_extrapolation, 3)} "
                print(colored(msg, "yellow" if spam else "red"))

                if spam:

                    trace = merge_two_traces(trace1, trace2)
                    trace1 = trace
                    if debug:
                        print(trace)
                    trace_indices_to_trim.append(index2)
                    step_to = trace.frame_range[1]
        else:
            step_to = next_step_to
        if debug:
            print(colored(f"jumping to step {step_to}", "blue"))

    if debug:
        print(f"Gonna delete the following traces as we have merged them: {trace_indices_to_trim}")
    traces = delete_indices(trace_indices_to_trim, traces)

    print(colored(f"Returning traces of length {len(traces)}, {len(trace_indices_to_trim)} shorter", "green"))
    print()
    return traces


def track_reappearance(traces, show=True, debug=False):
    """ Tracks the time it takes for an agent to appear when one is lost (end of a trace)

    :arg traces: (list): a list of Traces
    :arg show: (bool): a flag whether to show the plot
    :arg debug: (bool): if True extensive output is shown

    :returns: time_to_reappear (list): list of times for an agent to reappear after end of a trace
    """
    print(colored("TRACE REAPPEARANCE", "blue"))
    frames_of_loss = []
    for trace in traces:
        frames_of_loss.append(trace.frame_range[1])

    frames_of_loss = list(sorted(frames_of_loss))
    if debug:
        print("frames_of_loss", frames_of_loss)

    # for trace in traces:
    #     print(trace.frame_range[0])

    frames_of_reappearance = []
    for frame in frames_of_loss:
        for trace in traces:
            if trace.frame_range[0] < frame:
                continue
            else:
                frames_of_reappearance.append(trace.frame_range[0])
                break
    if debug:
        print("frames_of_reappearance", frames_of_reappearance)

    time_to_reappear = list(map(lambda x, y: y - x, frames_of_loss, frames_of_reappearance))
    if debug:
        print("time_to_reappear", time_to_reappear)

    if show:
        plt.hist(time_to_reappear, bins=20)
        plt.xlabel('Step size')
        plt.ylabel('Count of time to reappear')
        plt.title(f'Histogram of times to reappear.')
        plt.show()

    return time_to_reappear


## CROSS-TRACE ANALYSIS
def cross_trace_analyse(traces, scraped_traces):
    """ Checks traces against each other.

    :arg traces: list: a list of Traces
    :arg scraped_traces: list: a list of scraped traces obtained by parse_traces()
    """
    print(colored("CROSS-TRACE ANALYSIS", "blue"))
    for index, trace in enumerate(traces):
        for index2, trace2 in enumerate(traces):
            if index == index2:
                continue
            if abs(trace.frame_range[1] - trace2.frame_range[0]) < 100:
                # print(traces[index])
                # print(traces[index]["23325"])
                # print()
                # print(traces[index][str(trace.frame_range[1])][1])
                # print(traces[index2][str(trace2.frame_range[0])][1])
                point_distance = math.dist(list(map(float, (scraped_traces[trace.trace_id][trace.frame_range[1]][1]))),
                                           list(map(float, (scraped_traces[trace2.trace_id][trace2.frame_range[0]][1]))))
                message = f"The beginning of trace {trace2.trace_id} is close to end of trace {trace.trace_id} " \
                          f"by {abs(trace.frame_range[1] - trace2.frame_range[0])} while the x,y distance is " \
                          f"{round(point_distance,3)}. Consider joining them."

                if index2 == index + 1:
                    if point_distance < 10:
                        print(colored(message, "blue"))
                    else:
                        print(colored(message, "yellow"))
                else:
                    print(message)
    print()

