import copy
import csv
import math
from termcolor import colored
from trace import Trace
import matplotlib.pyplot as plt
import numpy as np
from misc import merge_dictionary, is_in, has_overlap, is_before


def dummy_colision_finder(csvfile, size):
    """ Parses  a loopy csv file nn/ai. It prints the frame numbers where the additional agents. The print includes agent's id.
        Returns a list of frames where an additional agent was found

    :arg csvfile: input file
    :arg size: expected number of agents
    :return frame_numbers_of_collided_agents: list of frames where an additional agent was found
    """
    reader = csv.DictReader(csvfile)
    i = 0
    frame_numbers_of_collided_agents = []

    for row in reader:
        # print(row['oid'])
        if int(row['oid']) > size - 1:
            print("A new fake agents appears on frame number", row['frame_number'], "iteration number", i, "with oid",
                  row['oid'])
            frame_numbers_of_collided_agents.append(row['frame_number'])
            size = size + 1
        i = i + 1

    return frame_numbers_of_collided_agents


def single_trace_checker(traces):
    for index, trace in enumerate(traces):
        print(f"Agent number {index} Number_of_frames {trace.number_of_frames}, frame_range_len "
              f"{trace.frame_range_len}, trace_lenn {trace.trace_lenn}, "
              f"max_step_len {trace.max_step_len}, max_step_len_index {trace.max_step_len}, "
              f"max_step_len_line {trace.max_step_len_line}")
        if trace.trace_lenn == 0:
            print("This trace has length of 0. Consider deleting this agent")  ## this can be FP
        if trace.max_step_len > bee_max_step_len:
            print("This agent has moved", bee_max_step_len, "in a single step, you might consider deleting it.")


def scatter_detection(traces):
    """ Creates a scatter plot of detected traces of each agent.

    :arg traces: (list): a list of lists of frame numbers where respective agent was tracked
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


def track_reappearence(traces, show=True):
    """ Tracks the time it takes for an agent to appear when one is lost

    :arg traces: (list): a list of lists of frame numbers where respective agent was tracked
    :arg show: (bool): a flag whether to show the plot
    """
    frames_of_loss = []
    for trace in traces:
        frames_of_loss.append(trace.frame_range[1])

    frames_of_loss = list(sorted(frames_of_loss))
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
    print("frames_of_reappearence", frames_of_reappearence)

    time_to_reappeare = list(map(lambda x, y: y - x, frames_of_loss, frames_of_reappearence))
    print("time_to_reappeare", time_to_reappeare)

    if show:
        plt.hist(time_to_reappeare, bins=20)
        plt.xlabel('Step size')
        plt.ylabel('Count of time to reappear')
        plt.title(f'Histogram of times to reappear.')
        plt.show()

    return time_to_reappeare


def merge_two_traces(trace1: Trace, trace2: Trace):
    """ Puts two traces together

    :arg trace1 (Trace) a Trace to be merged with the following trace
    :arg trace1 (Trace) a Trace to be merged with the following trace
    """
    ## CHECK
    assert isinstance(trace1, Trace)
    assert isinstance(trace2, Trace)
    if has_overlap(trace1.frame_range, trace2.frame_range):
        raise Exception("The two traces have an overlap. We cannot merge them.")

    ## MERGE
    trace1.trace_id = min(trace1.trace_id, trace2.trace_id)

    if is_before(trace1.frame_range, trace2.frame_range):
        merge_step = math.dist(trace1.locations[-1], trace2.locations[0])
        trace1.trace_lenn = trace1.trace_lenn + merge_step + trace2.trace_lenn

        trace1.frames_tracked.extend(trace2.frames_tracked)

        trace1.locations.extend(trace2.locations)

    else:
        merge_step = math.dist(trace2.locations[-1], trace1.locations[0])
        trace1.trace_lenn = trace2.trace_lenn + merge_step + trace1.trace_lenn

        spam = copy.copy(trace2.frames_tracked)
        spam.extend(trace1.frames_tracked)
        trace1.frames_tracked = spam

        spam = copy.copy(trace2.locations)
        spam.extend(trace1.locations)
        trace1.locations = spam


    trace1.frame_range = (min(trace1.frame_range[0], trace2.frame_range[0]), max(trace1.frame_range[1], trace2.frame_range[1]))
    trace1.number_of_frames = trace1.number_of_frames + trace2.number_of_frames
    if has_overlap(trace1.frame_range, trace2.frame_range):
        trace1.frame_range_len = trace1.frame_range[1] - trace1.frame_range[0]
    else:
        trace1.frame_range_len = trace1.frame_range_len + trace2.frame_range_len

    # print("trace1.max_step_len", trace1.max_step_len)
    # print("trace2.max_step_len", trace2.max_step_len)

    if trace1.max_step_len < trace2.max_step_len:
        trace1.max_step_len_step_index = trace2.max_step_len_step_index
        trace1.max_step_len_line = trace2.max_step_len_line
        trace1.max_step_len_frame_number = trace2.max_step_len_frame_number

    trace1.max_step_len = max(trace1.max_step_len, trace2.max_step_len)

    trace1.trace_lengths = merge_dictionary(trace1.trace_lengths, trace2.trace_lengths)

    # print(trace1.trace_lengths)
    if round(merge_step, 6) in trace1.trace_lengths.keys():
        trace1.trace_lengths[round(merge_step, 6)] = trace1.trace_lengths[round(merge_step, 6)] + 1
    else:
        trace1.trace_lengths[round(merge_step, 6)] = 1
    # print(trace1.trace_lengths)

    return trace1


def put_traces_together(traces, population_size):
    """ Puts traces together such that all the agents but one is being tracked

        :arg traces (list) list of traces
        :arg population_size (int) expected number of agents
    """
    reappearence = track_reappearence(traces, show=False)
    print(len(traces))
    print(len(reappearence))

    for trace in traces:
        pass


def trim_out_additional_agents_over_long_trace(traces, population_size):
    """ Trims out additional appearance of an agent when long traces are over here

    :arg traces (list) list of traces
    :arg population_size (int) expected number of agents
    """

    ## obtain the ranges with the size of frame more than 100 where all the agents are being tracked
    ranges = []
    for index1, trace in enumerate(traces):
        assert isinstance(trace, Trace)
        trace.check_trace_consistency()
        ranges.append(trace.frame_range)
    ranges = sorted(ranges)

    at_least_two_overlaps = []
    for index1, range1 in enumerate(ranges[:-1]):
        current_overlaps = []
        print()
        for index2, range2 in enumerate(ranges):
            if index1 == index2:
                continue

            if range2[1] <= range1[0]:
                continue

            if range2[0] >= range1[1]:  ## Beginning of the further intervals is behind the end of current one
                print("current interval:", range1)
                print("The set of overlapping intervals:", current_overlaps)
                i = -1
                min_range = 0
                for index3, range3 in enumerate(current_overlaps):
                    if len(range3) > min_range:
                        i = index3
                        min_range = len(range3)
                if i == -1:
                    print("there was no overlaping interval")
                    at_least_two_overlaps.append([])
                else:
                    print("picking the longest interval:", current_overlaps[i])
                    at_least_two_overlaps.append(current_overlaps[i])
                break
            else:
                if max(range1[0], range2[0]) > min(range1[1], range2[1]):
                    print(colored(range1, "red"))
                    print(colored(range2, "red"))
                    print("range1[1]", range1[1])
                    print("range2[0]", range2[0])
                    print(range2[0] >= range1[1])
                # print(range1)
                # print(range2)
                # print(max(range1[0], range2[0]))
                # print(min(range1[1], range2[1]))
                current_overlaps.append([max(range1[0], range2[0]), min(range1[1], range2[1])])
                # ranges[index2] = (range1[1], ranges[index2][1])
                continue
    print(at_least_two_overlaps)
    indices_to_be_deleted = []
    for index1, range1 in enumerate(at_least_two_overlaps):
        if index1 in indices_to_be_deleted:
            continue
        for index2, range2 in enumerate(at_least_two_overlaps):
            if index2 in indices_to_be_deleted:
                continue
            if index1 == index2:
                continue
            if range2[0] > range1[1]:
                break
            if range2[0] >= range1[0] and range2[1] <= range1[1]:
                print(f"range index {index2} with value {range2} is in range index {index1} with value{range1}")
                indices_to_be_deleted.append(index2)
    print()
    print(indices_to_be_deleted)
    indices_to_be_deleted = list(reversed(sorted(list(set(indices_to_be_deleted))))) ## Remove duplicates
    print()
    print(indices_to_be_deleted)
    for index in indices_to_be_deleted:
        del at_least_two_overlaps[index]

    print()
    print(at_least_two_overlaps)

    traces_indices_to_be_deleted = []
    for index, tracee in enumerate(traces):
        for range in at_least_two_overlaps:
            if tracee.frame_range[0] > range[0] and tracee.frame_range[1] < range[1]:
                traces_indices_to_be_deleted.append(index)
    traces_indices_to_be_deleted = list(reversed(sorted(list(set(traces_indices_to_be_deleted)))))
    for index in traces_indices_to_be_deleted:
        del traces[index]

    print(len(traces))

    for trace in traces:
        trace.check_trace_consistency()

    return traces


def parse_traces(csvfile):
    """ Parses a loopy csv file nn/ai and returns a dictionary of traces 'oid' -> 'frame_number' -> location [x,y]

    :arg
        csvfile (file): input file

    :returns
        traces (dic): dictionary of traces 'oid' -> 'frame_number' -> [line_id, location [x,y]]
    """
    traces = dict()
    reader = csv.DictReader(csvfile)
    for row in reader:
        if int(row['oid']) not in traces.keys():
            # print("hello", row['oid'])
            traces[int(row['oid'])] = dict()
        traces[int(row['oid'])][int(row['frame_number'])] = [row[''], [float(row['x']), float(row['y'])]]
    return traces


if __name__ == "__main__":
    ## VARIABLE DECLARATION
    bee_max_step_len = 1000

    ## CODE

    # i = 0
    # with open('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv',
    #           newline='') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         i = i + 1
    #         print(row['date'], row['err'], row['frame_count'], row['frame_number'], row['frame_timestamp'], row['name'], row['oid'], row['type'], row['x'], row['y'])
    #         print(row['oid'])

    #
    # with open('../data/Video_tracking/190823/20190823_115857275_2BEES_generated_20210507_083510_nn.csv',
    #           newline='') as csvfile:
    #     scraped_traces = parse_traces(csvfile)
    #     traces = []
    #     for index, trace in enumerate(scraped_traces.keys()):
    #         traces.append(Trace(scraped_traces[trace], index))
    #
    #     ## INDEPENDENT TRACE-LIKE ANALYSIS
    #     for index, trace in enumerate(traces):
    #         print("Agent number", index,
    #               ". Number_of_frames, frame_range_len, trace_lenn, max_step_len, max_step_len_index, max_step_len_line:",
    #               trace)
    #         if trace.trace_lenn == 0:
    #             print("This trace has length of 0. Consider deleting this agent")  ## this can be FP
    #         if trace.max_step_len > bee_max_step_len:
    #             print("This agent has moved", bee_max_step_len, "in a single step, you might consider deleting it.")
    #
    #         # trace.show_step_lenghts_hist()
    #
    #     ## SCATTER PLOT OF DETECTIONS
    #     scatter_detection(traces)

    with open('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv',
              newline='') as csvfile:

        # TODO uncomment the following line
        # print(dummy_colision_finder(csvfile, 2))

        ## PARSER
        scraped_traces = parse_traces(csvfile)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            print(trace)
            print(scraped_traces[trace])
            raise Exception()
            traces.append(Trace(scraped_traces[trace], index))
        raise Exception()

        ## INDEPENDENT TRACE-LIKE ANALYSIS
        # TODO uncomment the following line
        # single_trace_checker(traces)

        # TODO uncomment the following line
        # for trace in traces:
        #     trace.show_step_lenghts_hist(bins=5000)

        # TODO uncomment the following line
        # traces[0].show_step_lenghts_hist(bins=5000)

        ## SCATTER PLOT OF DETECTIONS
        scatter_detection(traces)
        track_reappearence(traces)

        traces = trim_out_additional_agents_over_long_trace(traces, 2)

        scatter_detection(traces)
        track_reappearence(traces)

        put_traces_together(traces, 2)
        raise Exception()

        ## CROSS-TRACE ANALYSIS
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
                    point_distance = math.dist(list(map(float, (scraped_traces[index][str(trace.frame_range[1])][1]))),
                                               list(map(float, (scraped_traces[index2][str(trace2.frame_range[0])][1]))))
                    message = "The beginning of trace", index2, "is close to end of trace", index, "by", abs(
                        trace.frame_range[1] - trace2.frame_range[0]), "while the x,y distance is ", point_distance, "Consider joining them."

                    if index2 == index + 1:
                        if point_distance < 10:
                            print(colored(message, "blue"))
                        else:
                            print(colored(message, "yellow"))
                    else:
                        print(message)
