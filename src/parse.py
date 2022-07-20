import csv
import math
from termcolor import colored
from trace import Trace
import matplotlib.pyplot as plt
import numpy as np


def dummy_colision_finder(csvfile, size):
    """ Parses  a loopy csv file nn/ai. It prints the frame numbers where the additional agents. The print includes agent's id.
        Returns a list of frames where an additional agent was found

    :param csvfile: input file
    :param size: expected number of agents
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


def scatter_detection(traces_lenghts):
    """ Creates a scatter plot of detected traces of each agent.

    #TODO
    :param traces_lenghts (list): a list of lists of frame numbers where respective agent was tracked
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    for index, trace in enumerate(traces_lenghts):
        x = trace.times_tracked
        y = [index] * len(x)
        ax1.scatter(x, y, alpha=0.5)
    plt.xlabel('Frame number')
    plt.ylabel('Agent id')
    plt.title(f'Scatter plot of detections of individual agents over time.')
    plt.show()


def trim_out_additional_agents_over_long_trace(traces):
    """ Trims out additional appearance of an agent when long traces are over here """
    # TODO
    
    pass


def parse_traces(csvfile):
    """ Parses a loopy csv file nn/ai and returns a dictionary of traces 'oid' -> 'frame_number' -> location [x,y]

    :arg
        csvfile (file): input file

    :returns
        traces (dic): dictionary of traces 'oid' -> 'frame_number' -> location [x,y]
    """
    traces = dict()
    reader = csv.DictReader(csvfile)
    for row in reader:
        if int(row['oid']) not in traces.keys():
            # print("hello", row['oid'])
            traces[int(row['oid'])] = dict()
        traces[int(row['oid'])][row['frame_number']] = [row[''], [row['x'], row['y']]]
    return traces


if __name__ == "__main__":
    ## VARIABLE DECLARATION
    bee_max_step_len = 1000

    ## CODE
    i = 0
    with open('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv',
              newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            i = i + 1
            # print(row['date'], row['err'], row['frame_count'], row['frame_number'], row['frame_timestamp'], row['name'], row['oid'], row['type'], row['x'], row['y'])
            # print(row['oid'])

    with open('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv',
              newline='') as csvfile:
        print(dummy_colision_finder(csvfile, 2))



    with open('../data/Video_tracking/190823/20190823_115857275_2BEES_generated_20210507_083510_nn.csv',
              newline='') as csvfile:
        traces = parse_traces(csvfile)
        traces_lenghts = []
        for index, trace in enumerate(traces.keys()):
            traces_lenghts.append(Trace(traces[trace], index))

        ## INDEPENDENT TRACE-LIKE ANALYSIS
        for index, trace in enumerate(traces_lenghts):
            print("Agent number", index,
                  ". Number_of_frames, frame_range_len, trace_lenn, max_step_len, max_step_len_index, max_step_len_line:",
                  trace)
            if trace.trace_lenn == 0:
                print("This trace has length of 0. Consider deleting this agent")  ## this can be FP
            if trace.max_step_len > bee_max_step_len:
                print("This agent has moved", bee_max_step_len, "in a single step, you might consider deleting it.")

            # trace.show_step_lenghts_hist()

        ## SCATTER PLOT OF DETECTIONS
        scatter_detection(traces_lenghts)


    with open('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv',
              newline='') as csvfile:
        traces = parse_traces(csvfile)
        traces_lenghts = []
        for index, trace in enumerate(traces.keys()):
            traces_lenghts.append(Trace(traces[trace], index))

        ## INDEPENDENT TRACE-LIKE ANALYSIS
        for index, trace in enumerate(traces_lenghts):
            print("Agent number", index,
                  ". Number_of_frames, frame_range_len, trace_lenn, max_step_len, max_step_len_index, max_step_len_line:",
                  trace)
            if trace.trace_lenn == 0:
                print("This trace has length of 0. Consider deleting this agent")  ## this can be FP
            if trace.max_step_len > bee_max_step_len:
                print("This agent has moved", bee_max_step_len, "in a single step, you might consider deleting it.")

            # trace.show_step_lenghts_hist()

        ## SCATTER PLOT OF DETECTIONS
        scatter_detection(traces_lenghts)

        trim_out_additional_agents_over_long_trace(traces)

        ## CROSS-TRACE ANALYSIS
        for index, trace in enumerate(traces_lenghts):
            for index2, trace2 in enumerate(traces_lenghts):
                if index == index2:
                    continue
                if abs(trace.frame_range[1] - trace2.frame_range[0]) < 100:
                    # print(traces[index])
                    # print(traces[index]["23325"])
                    # print()
                    # print(traces[index][str(trace.frame_range[1])][1])
                    # print(traces[index2][str(trace2.frame_range[0])][1])
                    point_distance = math.dist(list(map(float, (traces[index][str(trace.frame_range[1])][1]))),
                                               list(map(float, (traces[index2][str(trace2.frame_range[0])][1]))))
                    message = "The beginning of trace", index2, "is close to end of trace", index, "by", abs(
                        trace.frame_range[1] - trace2.frame_range[0]), "while the x,y distance is ", point_distance, "Consider joining them."

                    if index2 == index + 1:
                        if point_distance < 10:
                            print(colored(message, "blue"))
                        else:
                            print(colored(message, "yellow"))
                    else:
                        print(message)
