import csv
from time import time

from _socket import gethostname
from termcolor import colored


def dummy_collision_finder(csv_file, size):
    """ Parses  a loopy csv file nn/ai. It prints the frame numbers where the additional agents.
    The print includes agent's id.
    Returns a list of frames where an additional agent was found.

    :arg csv_file: (file): input file
    :arg size: (int): expected number of agents
    :returns: frame_numbers_of_collided_agents: list of frames where an additional agent was found
    """
    print(colored("DUMMY COLLISION FINDER", "blue"))
    reader = csv.DictReader(csv_file)
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


def parse_traces(csv_file):
    """ Parses a loopy csv file nn/ai and returns a dictionary of traces 'oid' -> 'frame_number' -> location [x,y]

    :arg csv_file: (file): input file
    :returns: traces (dic): dictionary of traces 'oid' -> 'frame_number' -> [line_id, location [x,y]]
    """
    start_time = time()
    print(colored("PARSE TRACES", "blue"))
    traces = dict()
    reader = csv.DictReader(csv_file)
    for row in reader:
        if int(row['oid']) not in traces.keys():
            # print("hello", row['oid'])
            traces[int(row['oid'])] = dict()
        traces[int(row['oid'])][int(row['frame_number'])] = [row[''], [float(row['x']), float(row['y'])]]
    print(colored(f"Loaded {len(traces)} traces. It took {gethostname()} {time() - start_time} seconds.", "yellow"))
    return traces
