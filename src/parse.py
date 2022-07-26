import csv
import sys

from termcolor import colored
from trace import Trace, merge_two_traces
import matplotlib.pyplot as plt


def dummy_colision_finder(csvfile, size):
    """ Parses  a loopy csv file nn/ai. It prints the frame numbers where the additional agents. The print includes agent's id.
        Returns a list of frames where an additional agent was found

    :arg csvfile: input file
    :arg size: expected number of agents
    :return frame_numbers_of_collided_agents: list of frames where an additional agent was found
    """
    print(colored("DUMMY COLLISION FINDER", "blue"))
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
    print(colored("SINGLE TRACE CHECKER", "blue"))
    for index, trace in enumerate(traces):
        print(colored("Single trace checker", "blue"))
        print(colored(f"Checking trace: {trace}", "blue"))
        if trace.trace_lenn == 0:
            print(colored("This trace has length of 0. Consider deleting this agent", "blue"))  ## this can be FP
        if trace.max_step_len > bee_max_step_len:
            print(colored(f"This agent has moved {bee_max_step_len} in a single step, you might consider deleting it.", "blue"))


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


def track_reappearence(traces, show=True, debug=False):
    """ Tracks the time it takes for an agent to appear when one is lost

    :arg traces: (list): a list of lists of frame numbers where respective agent was tracked
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

    time_to_reappeare = list(map(lambda x, y: y - x, frames_of_loss, frames_of_reappearence))
    if debug:
        print("time_to_reappeare", time_to_reappeare)

    if show:
        plt.hist(time_to_reappeare, bins=20)
        plt.xlabel('Step size')
        plt.ylabel('Count of time to reappear')
        plt.title(f'Histogram of times to reappear.')
        plt.show()

    return time_to_reappeare


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
            ## look for a mergable trace
            print(colored("Gonna have a look for a mergable traces", "blue"))
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
                    trace = merge_two_traces(traces[index_to_go], trace2)
                    traces[index_to_go] = trace
                    if debug:
                        print(trace)
                    trace_indices_to_trim.append(index2)
                    step_to = trace.frame_range[1]
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


def trim_out_additional_agents_over_long_traces(traces, population_size, debug=False):
    """ Trims out additional appearance of an agent when long traces are over here

    :arg traces (list) list of traces
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

    at_least_two_overlaps = []
    for index1, range1 in enumerate(ranges[:-1]):
        current_overlaps = []
        if debug:
            print()
        for index2, range2 in enumerate(ranges):
            if index1 == index2:
                continue

            if range2[1] <= range1[0]:
                continue

            if range2[0] >= range1[1]:  ## Beginning of the further intervals is behind the end of current one
                if debug:
                    print("current interval:", range1)
                    print("The set of overlapping intervals:", current_overlaps)
                i = -1
                min_range = 0
                for index3, range3 in enumerate(current_overlaps):
                    if len(range3) > min_range:
                        i = index3
                        min_range = len(range3)
                if i == -1:
                    if debug:
                        print("there was no overlaping interval")
                    at_least_two_overlaps.append([])
                else:
                    if debug:
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
    if debug:
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
                if debug:
                    print(f"range index {index2} with value {range2} is in range index {index1} with value {range1}")
                indices_to_be_deleted.append(index2)

    if debug:
        print()
        print(indices_to_be_deleted)
    indices_to_be_deleted = list(reversed(sorted(list(set(indices_to_be_deleted))))) ## Remove duplicates
    if debug:
        print()
        print(indices_to_be_deleted)
    for index in indices_to_be_deleted:
        del at_least_two_overlaps[index]

    if debug:
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

    for trace in traces:
        trace.check_trace_consistency()

    print(colored(f"Returning traces of length {len(traces)}", "blue"))
    return traces


def parse_traces(csvfile):
    """ Parses a loopy csv file nn/ai and returns a dictionary of traces 'oid' -> 'frame_number' -> location [x,y]

    :arg
        csvfile (file): input file

    :returns
        traces (dic): dictionary of traces 'oid' -> 'frame_number' -> [line_id, location [x,y]]
    """
    print(colored("PARSE TRACES", "blue"))
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
            # print(trace)
            # print(scraped_traces[trace])
            traces.append(Trace(scraped_traces[trace], index))

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

        ## TRIM TRACES
        before_number_of_traces = len(traces)
        after_number_of_traces = 0
        while not before_number_of_traces == after_number_of_traces:
            before_number_of_traces = len(traces)
            traces = trim_out_additional_agents_over_long_traces(traces, 2)
            scatter_detection(traces)
            traces = put_traces_together(traces, 2)
            scatter_detection(traces)
            after_number_of_traces = len(traces)

        track_reappearence(traces)
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
