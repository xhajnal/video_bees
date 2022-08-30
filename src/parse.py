import csv
import os
import pickle
from time import time
from _socket import gethostname
from termcolor import colored


def pickle_load(file):
    """ Returns loaded pickled data

    Args:
        file (string or Path): filename/filepath
    """

    filename, file_extension = os.path.splitext(file)

    if file_extension == ".p":
        with open(file, "rb") as f:
            return pickle.load(f)
    elif file_extension == "":
        with open(str(file) + ".p", "rb") as f:
            return pickle.load(f)
    else:
        raise Exception("File extension does not match", f"{file} does not seem to be pickle file!")


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
    print(colored(f"Loaded {len(traces)} traces. It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "yellow"))
    return traces
