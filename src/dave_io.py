import csv
import glob
import json
import os
import pickle
from pathlib import Path
from time import time
from _socket import gethostname
from termcolor import colored
from datetime import datetime

from bee_specific import parse_population_size
from trace import Trace
from config import *


def get_video_path(file_path):
    """ Obtain the path of the video files. This may be case specific.

    :arg file_path: (str): filepath of the analysed file (csv)
    """
    # get the name of the file without suffix
    video_file = Path(file_path).stem
    # get the stem of the filename - digital identifier
    video_file = video_file.split("_")[:2]
    video_file = "_".join(video_file)
    # print(video_file)

    folder = os.path.dirname(Path(file_path))
    # print(folder)

    video_file = glob.glob(os.path.join(folder, f'*{video_file}*.mp4'))
    # Remove file with "movie_from"
    for index, file in enumerate(video_file):
        if "movie_from_" in file:
            del video_file[index]

    if len(video_file) > 1:
        raise Exception(f"There are more input videos with given identifier: {video_file}. We do not know which to pick.")
    elif len(video_file) == 0:
        video_file = ""
        output_video_file = ""
    else:
        video_file = video_file[0]
        try:
            os.mkdir("../output")
        except OSError:
            pass
        try:
            os.mkdir("../output/video")
        except OSError:
            pass
        output_video_file = os.path.join("..", "output", "video", os.path.basename(video_file))
        # print("default output_video_file:", output_video_file)

    return video_file, output_video_file


def is_new_config(file_name, is_first_run=None):
    """ Returns whether this config is new in the results.

    :arg file_name: (str): filename of the record
    :arg is_first_run: (bool): iff True, "results_after_first_run.txt" will be used instead of standard "results.txt"

    """
    if not (is_first_run is True):
        results_file = "../output/results.txt"
    else:
        results_file = "../output/results_after_first_run.txt"

    ## LOAD SAVED RESULTS
    try:
        with open(results_file) as file:
            results = json.load(file)
    except FileNotFoundError as err:
        # f = open("../output/results.p", "a")
        file = open(results_file, "a")
        file.close()
        results = {}

    if file_name not in results.keys():
        return True

    # GET SETTING
    setting = {"distance_from_calculated_arena": get_distance_from_calculated_arena(),
               "max_trace_gap": get_max_trace_gap(),
               "min_trace_length": get_min_trace_length(),
               "bee_max_step_len": get_bee_max_step_len(),
               "bee_max_step_len_per_frame": get_bee_max_step_len_per_frame(),
               "max_trace_gap_to_interpolate_distance": get_max_trace_gap_to_interpolate_distance(),
               "max_step_distance_to_merge_overlapping_traces": get_max_step_distance_to_merge_overlapping_traces(),
               "screen_size": get_screen_size()}

    same_setting_found = False

    for timestamp in results[file_name]:
        result = results[file_name][timestamp]
        if same_setting_found:
            break
        for key in setting.keys():
            # print(f"setting[{key}]", setting[key])
            # print(f"result[{key}]", result[key])
            if setting[key] != result[key]:
                same_setting_found = False
                break
            same_setting_found = True

    if same_setting_found:
        print(colored(f"Already found the same setting - skipping this file. \n", "magenta"))
    return not same_setting_found


def load_setting(file_name=None, time_stamp=None):
    """ Load the setting or its part given parameters.

    :arg file_name: (string): name of the file to be loaded, if None all file names are loaded
    :arg time_stamp: (string): time stamp to load for a given file, if None all time stamps are loaded
    """
    with open("../output/results.txt") as file:
        results = json.load(file)

    if file_name is not None:
        results = results[file_name]
        if time_stamp is not None:
            results = results[time_stamp]

    return results


def save_setting(counts, file_name, population_size, is_guided, is_force_merge_allowed, video_available, silent=False, debug=False, is_first_run=None):
    """ Loads, Updates, and Saves the results as dictionary in a "../output/results.txt" json file.
     file_path -> time stamp -> {config params, traces len and number of swapped traces/ jumps back and forth detected}

     for exact enumeration have a look in the code.
     for FIRST RUN the results are stored in "../output/results_after_first_run.txt"


    :arg counts: (list of int): counts of traces after each analysis part
    :arg file_name: (string): name of the file loaded
    :arg population_size: (int): number of agents tracked
    :arg is_guided: (bool): whether guided flag was on
    :arg is_force_merge_allowed: (bool): whether allow_force_merge was on
    :arg video_available: (bool) whether video was available
    :arg silent: (bool): if True minimal output is shown
    :arg debug: (bool): if True extensive output is shown
    :returns is_new: (bool): flag whether this result is new
    """
    print(colored("SAVE SETTING AND COUNTS OF TRACES AS JSON", "blue"))
    start_time = time()

    ## CHECK
    try:
        os.mkdir("../output")
    except OSError:
        pass
    # check all counts are counted
    assert len(counts) == 7

    ## LOAD SAVED RESULTS TO UPDATE IT
    if not (is_first_run is True):
        results_txt_file = "../output/results.txt"
    else:
        results_txt_file = "../output/results_after_first_run.txt"

    try:
        with open(results_txt_file) as file:
            results = json.load(file)
            if debug:
                print("RESULTS", results)
    except FileNotFoundError as err:
        file = open(results_txt_file, "a")
        file.close()
        results = {}

    # PARSE NEW ENTRY
    now = str(datetime.now())
    new_entry = {"had_video": video_available,
                 "is_guided": is_guided,
                 "force_merge_allowed": is_force_merge_allowed,
                 "distance_from_calculated_arena": get_distance_from_calculated_arena(),
                 "min_trace_len": get_min_trace_len(),
                 "max_trace_gap": get_max_trace_gap(),
                 "min_trace_length": get_min_trace_length(),
                 "bee_max_step_len": get_bee_max_step_len(),
                 "bee_max_step_len_per_frame": get_bee_max_step_len_per_frame(),
                 "max_trace_gap_to_interpolate_distance": get_max_trace_gap_to_interpolate_distance(),
                 "max_step_distance_to_merge_overlapping_traces": get_max_step_distance_to_merge_overlapping_traces(),
                 "force_merge_vicinity": get_force_merge_vicinity(),
                 "screen_size": get_screen_size(),
                 "loaded": counts[0],
                 "inside arena": counts[1],
                 "zero length": counts[2],
                 "jumps forth and back fixed": counts[3],
                 "traces swapped": counts[4],
                 "after first gaps and redundant": counts[5],
                 "after merging overlapping traces": counts[6],
                 # "after second gaps and redundant": counts[7],
                 "population_size": population_size}

    ## UPDATE THE RESULTS
    if file_name not in results.keys():
        results[file_name] = {}

    ## Check whether there is no replicate
    for timestamp in results[file_name]:
        result = results[file_name][timestamp]
        if debug:
            print("possibly same result", result)
        if result == new_entry:
            print(colored(
                f"Already found the same result - not saving it. It took {gethostname()} {round(time() - start_time, 3)} seconds. \n",
                "yellow"))
            return False

    results[file_name][now] = new_entry

    ## SAVE THE RESULTS
    # with open("../output/results.p", 'wb') as file:
    #     pickle.dump(results, file)

    with open(results_txt_file, 'w') as file:
        file.write(json.dumps(results))

    # if debug:
    #     print(results)
    # print(results)

    print(colored(
        f"Updating the results using this run. Saved in {os.path.abspath(results_txt_file)}. It took {gethostname()} {round(time() - start_time, 3)} seconds. \n",
        "yellow"))
    return True


def convert_results_from_json_to_csv(silent=False, debug=False, is_first_run=None):
    """ Stores the json results file as csv to show the results in a human-readable format.
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
    """

    print(colored("STORES THE JSON RESULTS FILE AS A CSV", "blue"))
    start_time = time()

    if not (is_first_run is True):
        results_txt_file = "../output/results.txt"
        results_csv_file = "../output/results.csv"
    else:
        results_txt_file = "../output/results_after_first_run.txt"
        results_csv_file = "../output/results_after_first_run.csv"

    with open(results_txt_file) as file:
        results = json.load(file)
        if debug:
            print(results_txt_file, results)

    try:
        with open(results_csv_file, "w") as file:
            # write header
            ## TODO parse the population size
            file.write(
                f"track_file; timestamp of the run; had_video; was_guided; was_force_merge_allowed; "
                f"distance_from_calculated_arena; max_trace_gap; min_trace_length; bee_max_step_len; "
                f"bee_max_step_len_per_frame; max_trace_gap_to_interpolate_distance; "
                f"max_step_distance_to_merge_overlapping_traces; force_merge_vicinity; screen_size; loaded traces; "
                f"inside arena; zero length; jumps forth and back fixed; traces swapped; after first gaps and redundant; "
                f"after merging overlapping traces; population size \n")
            assert isinstance(results, dict)
            for track_file in results.keys():
                if debug:
                    print("track_file", track_file)
                assert isinstance(results[track_file], dict)
                for timestamp in results[track_file].keys():
                    if debug:
                        print("timestamp", timestamp)
                    assert isinstance(results[track_file][timestamp], dict)
                    record = results[track_file][timestamp]
                    try:
                        had_video = record['had_video']
                    except KeyError as err:
                        had_video = "Unknown"

                    try:
                        guided = record['is_guided']
                        # print("")
                    except KeyError as err:
                        guided = "Unknown"

                    try:
                        force_merge_allowed = record['force_merge_allowed']
                    except KeyError as err:
                        force_merge_allowed = "Unknown"

                    try:
                        population_size = record['population_size']
                    except KeyError as err:
                        population_size = None
                        spam = track_file.split('_')
                        for item in spam:
                            if "bee" in item.lower():
                                population_size = ''.join([n for n in item if n.isdigit()])
                                break
                        if population_size is None:
                            raise err
                    try:
                        min_trace_len = record['min_trace_len']
                    except KeyError as err:
                        min_trace_len = ""
                    try:
                        zero_len = record['zero length']
                    except KeyError as err:
                        zero_len = ""

                    try:
                        force_merge_vicinity = record['force_merge_vicinity']
                    except KeyError as err:
                        force_merge_vicinity = ""

                    file.write(f"{track_file}; {timestamp}; {had_video}; {guided}; {force_merge_allowed}; "
                               f"{record['distance_from_calculated_arena']}; {record['max_trace_gap']}; {min_trace_len};"
                               f" {record['min_trace_length']}; {record['bee_max_step_len']}; "
                               f"{record['bee_max_step_len_per_frame']}; {record['max_trace_gap_to_interpolate_distance']}; "
                               f"{record['max_step_distance_to_merge_overlapping_traces']}; {force_merge_vicinity}; "
                               f"{record['screen_size']}; {record['loaded']}; {record['inside arena']}; {zero_len}; "
                               f"{record['jumps forth and back fixed']}; {record['traces swapped']}; "
                               f"{record['after first gaps and redundant']};"
                               f" {record['after merging overlapping traces']}; {population_size}\n")
    except OSError:
        print(colored(f"Could not write into csv file! Try to close it first.", "red"))
        return

    print(colored(f"Converting the json into a csv file. Saved in {os.path.abspath(results_csv_file)}. It took {gethostname()} {round(time() - start_time, 3)} seconds. \n","yellow"))


def save_traces(traces, file_name, silent=False, debug=False, is_first_run=None):
    """ Saves the traces as csv file in loopy manner.

        :arg traces (list) list of traces
        :arg file_name: (string): name of the file to be saved in "output" folder
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
    """

    if is_first_run is True:
        return

    print(colored("SAVE TRACES AS CSV", "blue"))
    start_time = time()

    try:
        os.mkdir("../output")
    except OSError:
        pass

    try:
        os.mkdir("../output/traces")
    except OSError:
        pass

    digit = parse_population_size(file_name)
    if digit is not False:
        try:
            os.mkdir(f"../output/traces/{digit}")
        except OSError:
            pass

    trackings = []
    frames_tracked = []
    tracking_to_trace_index = {}

    for index, trace in enumerate(traces):
        assert isinstance(trace, Trace)
        frames = trace.frames_list
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

    with open(f"../output/traces/{'' if digit is False else str(digit)+'/'}{file_name}", "w") as file:
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
            frame_index = trace.frames_list.index(frame)
            location = trace.locations[frame_index]
            id = trace.trace_id
            message = f"{index},,,{frame},{frame},,object_{id},{id},BVIEW_tracked_object,{location[0]},{location[1]}\n"
            file.write(message)

        print(colored(f"Saving {len(traces)} traces as csv in {os.path.abspath(f'../output/{file_name}')}. It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "yellow"))


def pickle_traces(traces, csv_file_path, silent=False, debug=False, is_first_run=None):
    """ Saves the traces as pickle.

        :arg traces: (list): list of traces
        :arg csv_file_path: (string): path to the file to be pickled in "output" folder
        :arg silent: (bool): if True minimal output is shown
        :arg debug: (bool): if True extensive output is shown
        :arg is_first_run: (bool): iff True, traces are stored in 'after_first_run' folder next to the input file
    """
    print(colored("SAVE TRACES AS PICKLE", "blue"))
    start_time = time()

    file_name = os.path.basename(csv_file_path)

    try:
        os.mkdir("../output")
    except OSError:
        pass

    try:
        os.mkdir("../output/traces")
    except OSError:
        pass

    digit = parse_population_size(file_name)
    if digit is not False:
        try:
            os.mkdir(f"../output/traces/{digit}")
        except OSError:
            pass

    if is_first_run is True:
        try:
            os.mkdir(os.path.join(os.path.dirname(csv_file_path), "after_first_run"))
        except OSError:
            pass

        file_path = str(os.path.join(os.path.dirname(csv_file_path), "after_first_run", file_name.replace(".csv", ".p")))
    else:
        file_path = str(os.path.splitext(f"../output/traces/{'' if digit is False else str(digit)+'/'}{file_name}")[0]) + ".p"

    if debug:
        print("file", file_path)
    with open(file_path, 'wb') as file:
        pickle.dump(traces, file)

    print(colored(f"Saving pickled {len(traces)} traces in {os.path.abspath(file_path)}. It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "yellow"))


def pickle_load(file):
    """ Returns loaded pickled data

    Args:
        file (string or Path): filename/filepath of the file to be loaded
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


def load_result_traces(file_path):
    """ Returns saved traces.

    Args:
        file_path (string or Path): filename/filepath of the bee file to load respective result file
    """
    digit = parse_population_size(file_path)
    file_name = Path(os.path.basename(file_path)).stem
    return pickle_load(f"../output/traces/{digit}/{file_name}")


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

# if __name__ == "__main__":
#     convert_results_from_json_to_csv()
