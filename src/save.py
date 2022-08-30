import os
import pickle
from time import time
from _socket import gethostname
from termcolor import colored

from trace import Trace


def save_traces(traces, file_name, silent=False, debug=False):
    """ Saves the traces as csv file in loopy manner.

        :arg traces (list) list of traces
        :arg file_name (string) name of the file to be saved in "output" folder
        :arg silent (bool) if True no output is shown
        :arg debug (bool) if True extensive output is shown
    """
    print(colored("SAVE TRACES AS CSV", "blue"))
    start_time = time()

    try:
        os.mkdir("../output")
    except Exception:
        pass

    trackings = []
    frames_tracked = []
    tracking_to_trace_index = {}

    for index, trace in enumerate(traces):
        assert isinstance(trace, Trace)
        frames = trace.frames_tracked
        trackings.extend(frames)
        frames_tracked.extend(frames)
        for frame in frames:
            if frame in tracking_to_trace_index.keys():
                tracking_to_trace_index[frame].append(index)
            else:
                tracking_to_trace_index[frame] = [index]
    # make a set of frames_tracked - delete duplicates
    # make a list of sorted list of it
    frames_tracked = list(sorted(list(set(frames_tracked))))

    if debug:
        # print("trackings", trackings)
        print("frames_tracked", frames_tracked)

    with open(f"../output/{file_name}", "w") as file:
        file.write(",date,err,frame_count,frame_number,frame_timestamp,name,oid,type,x,y\n")
        for index, frame in enumerate(trackings):
            # obtain the ids of traces with the given frame
            indices = tracking_to_trace_index[frame]
            # save the first index
            trace_index = indices[0]
            # delete the taken id
            tracking_to_trace_index[frame] = tracking_to_trace_index[frame][1:]
            # obtain the specific trace
            trace = traces[trace_index]
            # obtain the index of the frame
            frame_index = trace.frames_tracked.index(frame)
            location = trace.locations[frame_index]
            id = trace.trace_id
            message = f"{index},,,{frame},{frame},,object_{id},{id},BVIEW_tracked_object,{location[0]},{location[1]}\n"
            file.write(message)

    print(colored(f"Saving {len(traces)} traces, It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "yellow"))


def pickle_traces(traces, file_name, silent=False, debug=False):
    """ Saves the traces as pickle.

        :arg traces (list) list of traces
        :arg file_name (string) name of the file to be pickled in "output" folder
        :arg silent (bool) if True no output is shown
        :arg debug (bool) if True extensive output is shown
    """
    print(colored("SAVE TRACES AS PICKLE", "blue"))
    start_time = time()

    try:
        os.mkdir("../output")
    except Exception:
        pass

    file = str(os.path.splitext(f"../output/{file_name}")[0])+".p"
    if debug:
        print("file", file)
    with open(file, 'wb') as f:
        pickle.dump(traces, f)

    print(colored(f"Saving pickled {len(traces)} traces, It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "yellow"))
