import csv
import math
from termcolor import colored

class Trace:
    """ Single agent trace obtained from the loopy csv file or changed within the analysis.

    """
    def __init__(self, name, age):
        self.name = name
        self.age = age


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
            print("A new fake agents appears on frame number", row['frame_number'], "iteration number", i, "with oid", row['oid'])
            frame_numbers_of_collided_agents.append(row['frame_number'])
            size = size + 1
        i = i + 1

    return frame_numbers_of_collided_agents


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


def trace_len(trace: dict):
    """ Parses a trace - see traces in fun parse_traces. Returns number of frames of the trace, [minimal, maximal frame number], length of the trace in x,y space.

    :param trace: a single trace of traces

    :returns [number_of_frames, frame_range_len, trace_lenn, max_step_len]: [number of frames of the trace, [minimal, maximal frame number], length of the trace in x,y space, maximal length of a single step between the frames]

    """
    frames = sorted(list(map(int, trace.keys())))
    # print("frames", frames)

    number_of_frames = len(trace.keys())
    frame_range = (frames[0], frames[-1])
    # print(frame_range)
    frame_range_len = float(frames[-1]) - float(frames[0])
    max_step_len = 0
    max_step_len_step_index = None
    max_step_len_line = None
    max_step_len_frame_number = None

    trace_lenn = 0
    for index, frame in enumerate(frames):
        # print(trace[frames[index]])
        # print(trace[frames[index+1]])
        try:
            # print("index", index)
            # print("frames index ", frames[index])
            # print("traces frames index ", trace[str(frames[index])])
            # print("traces frames index, x,y part", trace[str(frames[index])][1])
            # print("map it to floats", list(map(float, (trace[str(frames[index])][1]))))
            step_len = math.dist(list(map(float, (trace[str(frames[index])][1]))), list(map(float, (trace[str(frames[index+1])][1]))))
            if step_len > max_step_len:  ## Set max step len
                max_step_len = step_len
                max_step_len_step_index = index
                max_step_len_line = trace[str(frames[index])][0]
                max_step_len_frame_number = frame
            trace_lenn = trace_lenn + step_len
        except IndexError as err:
            if not index == len(frames) - 1:
                # print(index)
                # print(len(frames))
                # print(trace)
                # print("Error:", str(err))
                raise err

    return frame_range, number_of_frames, frame_range_len, trace_lenn, max_step_len, max_step_len_step_index, max_step_len_line, max_step_len_frame_number


if __name__ == "__main__":
    ## VARIABLE DECLARATION
    bee_max_step_len = 1000

    ## CODE
    i = 0
    with open('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            i = i+1
            # print(row['date'], row['err'], row['frame_count'], row['frame_number'], row['frame_timestamp'], row['name'], row['oid'], row['type'], row['x'], row['y'])
            # print(row['oid'])

    with open('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv', newline='') as csvfile:
        # dummy_colision_finder(csvfile, 2)
        pass

    with open('../test/test.csv', newline='') as csvfile:
        traces = parse_traces(csvfile)
        # print()
        print(traces[0])
        print("number_of_frames, frame_range_len, trace_length:", trace_len(traces[0]))
        print(traces[1])
        print("number_of_frames, frame_range_len, trace_length:", trace_len(traces[1]))

    with open('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv', newline='') as csvfile:
        traces = parse_traces(csvfile)
        traces_lenghts = []
        for index, trace in enumerate(traces.keys()):
           traces_lenghts.append(trace_len(traces[trace]))

        ## INDEPENDENT TRACE-LIKE ANALYSIS
        for index, trace_length in enumerate(traces_lenghts):
           print("Agent number", index, ". Number_of_frames, frame_range_len, trace_lenn, max_step_len, max_step_len_index, max_step_len_line:", trace_length)
           if trace_length[3] == 0:
               print("This trace has length of 0. Consider deleting this agent")  ## this can be FP
           if trace_length[4] > bee_max_step_len:
               print("This agent has moved", bee_max_step_len, "in a single step, you might consider deleting it.")

        ## CROSS-TRACE ANALYSIS
        for index, trace in enumerate(traces_lenghts):
            for index2, trace2 in enumerate(traces_lenghts):
                if index == index2:
                    continue
                if abs(trace[0][1] - trace2[0][0]) < 100:
                    # print(traces[index])
                    # print(traces[index]["23325"])
                    # print()
                    print(traces[index][str(trace[0][1])][1])
                    print(traces[index2][str(trace2[0][0])][1])
                    point_distance = math.dist(list(map(float, (traces[index][str(trace[0][1])][1]))), list(map(float, (traces[index2][str(trace2[0][0])][1]))))
                    message = "The beginning of trace", index2, "is close to end of trace", index, "by", abs(trace[0][1] - trace2[0][0]), "while the x,y distance is ", point_distance, "Consider joining them."

                    if index2 == index + 1:
                        if point_distance < 10:
                            print(colored(message, "blue"))
                        else:
                            print(colored(message, "yellow"))
                    else:
                        print(message)
