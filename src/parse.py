import csv
import math


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
        traces[int(row['oid'])][row['frame_number']] = [row['x'], row['y']]
    return traces


def trace_len(trace: dict):
    """ Parses a trace - see traces in fun parse_traces. Returns number of frames of the trace, [minimal, maximal frame number], length of the trace in x,y space.

    :param trace: a single trace of traces

    :returns [number_of_frames, frame_range_len, trace_lenn]: [number of frames of the trace, [minimal, maximal frame number], length of the trace in x,y space]

    """
    frames = sorted(list(map(float, trace.keys())))

    number_of_frames = len(trace.keys())
    frame_range = (frames[0], frames[-1])
    # print(frame_range)
    frame_range_len = float(frames[-1]) - float(frames[0])

    trace_lenn = 0
    for index, frame in enumerate(frames):
        # print(trace[frames[index]])
        # print(trace[frames[index+1]])
        try:
            trace_lenn = trace_lenn + math.dist(list(map(float, (trace[frames[index]]))), list(map(float, (trace[frames[index+1]]))))
        except Exception as err:
            print(trace)
            print("Error:", str(err))
            raise err

    return number_of_frames, frame_range_len, trace_lenn


if __name__ == "__main__":

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

    with open('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv', newline='') as csvfile:
        traces = parse_traces(csvfile)
        # print()
        # print(traces[2])
        print(trace_len(traces[1]))

    # print(i)
