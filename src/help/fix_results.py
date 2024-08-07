import glob
import json
import os
import pickle
from copy import copy
from time import time
from termcolor import colored

import analyse
from config import hash_config
from dave_io import convert_results_from_json_to_csv, pickle_load


# DEPRECATED
def check_setting():
    """ Fixes population population_size column,

    """
    print(colored("SAVE SETTING AND COUNTS OF TRACES AS JSON", "blue"))
    start_time = time()

    ## LOAD SAVED RESULTS TO UPDATE IT
    with open("../../output/results.txt") as file:
        results = json.load(file)

    for file in results.keys():
        population_size = None
        spam = file.split('_')
        for item in spam:
            if "bee" in item.lower():
                population_size = ''.join([n for n in item if n.isdigit()])
                break
        if population_size is None:
            raise Exception

        for timestamp in results[file]:
            try:
                if int(results[file][timestamp]["population_size"]) != int(population_size):
                    print("file", file)
                    print("population_size", population_size)
                    print("results[file][timestamp]['population_size']", results[file][timestamp]["population_size"])
                    results[file][timestamp]["population_size"] = int(population_size)
            except KeyError:
                results[file][timestamp]["population_size"] = int(population_size)

    with open("../../output/results.txt", 'w') as file:
        file.write(json.dumps(results))


def add_this_config_hash_to_results(after_first_run=False, debug=False):
    """ Adds the config hash to the result."""
    new_results = {}

    file_name = f"../output/results{'_after_first_run' if after_first_run else ''}.txt"
    # print(file_name)

    with open(file_name) as file:
        results = json.load(file)

    for file in results.keys():
        for config_hash in results[file].keys():
            for time_stamp in results[file][config_hash].keys():
                # print(results[file])
                # print(results[file][config_hash])
                # print(results[file][config_hash][time_stamp])

                # setting = (get_distance_from_calculated_arena(),
                #            get_min_trace_len(),
                #            get_vicinity_of_short_traces(),
                #            get_max_trace_gap(),
                #            get_min_trace_length_to_merge(),
                #            get_bee_max_step_len(),
                #            get_bee_max_step_len_per_frame(),
                #            get_max_trace_gap_to_interpolate_distance(),
                #            get_max_step_distance_to_merge_overlapping_traces(),
                #            get_min_step_distance_to_merge_overlapping_traces(),
                #            get_force_merge_vicinity_distance(),
                #            tuple([item for sublist in get_screen_size() for item in sublist]))

                try:
                    min_trace_len = results[file][config_hash][time_stamp]['min_trace_len']
                except KeyError:
                    min_trace_len = -1

                try:
                    get_vicinity_of_short_traces = results[file][config_hash][time_stamp]['get_vicinity_of_short_traces']
                except KeyError:
                    get_vicinity_of_short_traces = -1

                try:
                    min_trace_length_to_merge = results[file][config_hash][time_stamp]['min_trace_length']
                except KeyError:
                    try:
                        min_trace_length_to_merge = results[file][config_hash][time_stamp]['bee_min_trace_len']
                    except KeyError:
                        min_trace_length_to_merge = -1

                try:
                    min_step_distance_to_merge_overlapping_traces = results[file][config_hash][time_stamp]['min_step_distance_to_merge_overlapping_traces']
                except KeyError:
                    min_step_distance_to_merge_overlapping_traces = ""

                try:
                    force_merge_vicinity_distance = results[file][config_hash][time_stamp]['force_merge_vicinity']
                except KeyError:
                    force_merge_vicinity_distance = -1

                # try:
                #     a = int((list(results[file].keys())[0]))
                #     print(a)
                #     continue
                # except ValueError:
                #     pass

                this_config_hash = hash_config(this=[results[file][config_hash][time_stamp]['distance_from_calculated_arena'],
                                                     min_trace_len,
                                                     get_vicinity_of_short_traces,
                                                     results[file][config_hash][time_stamp]['max_trace_gap'],
                                                     min_trace_length_to_merge,
                                                     results[file][config_hash][time_stamp]['bee_max_step_len'],
                                                     results[file][config_hash][time_stamp]['bee_max_step_len_per_frame'],
                                                     results[file][config_hash][time_stamp]['max_trace_gap_to_interpolate_distance'],
                                                     results[file][config_hash][time_stamp]['max_step_distance_to_merge_overlapping_traces'],
                                                     min_step_distance_to_merge_overlapping_traces,
                                                     force_merge_vicinity_distance,
                                                     results[file][config_hash][time_stamp]['screen_size']])

                try:
                    a = new_results[file]
                except KeyError:
                    # print(f"no file {file}")
                    new_results[file] = {}

                try:
                    a = new_results[file][this_config_hash]
                except KeyError:
                    # print(f"no hash {this_config_hash}")
                    new_results[file][this_config_hash] = {}

                try:
                    a = new_results[file][this_config_hash][time_stamp]
                except KeyError:
                    # print(f"no time_stamp {time_stamp}")
                    new_results[file][this_config_hash][time_stamp] = {}

                new_results[file][this_config_hash][time_stamp] = results[file][config_hash][time_stamp]

    if debug:
        print(new_results)

    with open(file_name, 'w') as file:
        file.write(json.dumps(new_results))



## BEE SPECIFIC
def fix_order_setting():
    """ Fixes order of records. Trim parts from record."""
    print(colored("SAVE SETTING AND COUNTS OF TRACES AS JSON", "blue"))
    start_time = time()

    ## LOAD SAVED RESULTS TO UPDATE IT
    with open("../../output/results.txt") as file:
        results = json.load(file)

    results1 = {}
    results2 = {}
    results5 = {}
    results7 = {}
    results10 = {}
    results15 = {}

    for file in results.keys():
        # trim part from the record
        if "part" in str(file).lower():
            continue
        if "_1bee" in str(file).lower():
            # print("hello")
            results1[file] = results[file]
        elif "_2bee" in str(file).lower():
            # print("hello")
            results2[file] = results[file]
        elif "_5bee" in str(file).lower():
            # print("hello")
            results5[file] = results[file]
        elif "_7bee" in str(file).lower():
            # print("hello")
            results7[file] = results[file]
        elif "_10bee" in str(file).lower():
            # print("hello")
            results10[file] = results[file]
        elif "_15bee" in str(file).lower():
            # print("hello")
            results15[file] = results[file]

    for file in results2.keys():
        results1[file] = results2[file]
    for file in results5.keys():
        results1[file] = results5[file]
    for file in results7.keys():
        results1[file] = results7[file]
    for file in results10.keys():
        results1[file] = results10[file]
    for file in results15.keys():
        results1[file] = results15[file]

    with open("../../output/results.txt", 'w') as file:
        file.write(json.dumps(results1))

    convert_results_from_json_to_csv()


def fix_wrong_loaded():
    """ Fixes wrongly loaded items"""
    print(colored("SAVE SETTING AND COUNTS OF TRACES AS JSON", "blue"))
    start_time = time()

    ## LOAD SAVED RESULTS TO UPDATE IT
    with open("../../output/results.txt") as file:
        results = json.load(file)

    for file in results.keys():
        all_loaded = []
        for my_hash in results[file].keys():
            for time_stamp in results[file][my_hash].keys():
                item = results[file][my_hash][time_stamp]
                ## TODO hotfix
                if all_loaded:
                    if item["loaded"] not in all_loaded:
                        del results[file][my_hash][time_stamp]

    with open("../../output/results.txt", 'w') as file:
        file.write(json.dumps(results))


def fix_wrong_trim_in_decisions():
    """ Fixes wrongly saved trimming """
    os.chdir("../../output/partial")
    print(os.getcwd())

    files = glob.glob("./*.p")
    print(files)

    for file in files:
        a = pickle_load(file)
        b = copy(a)
        for key, value in a.items():
            if key[0][0] == 'trim_trace':
                spam = (key[0][0], key[0][1], key[0][2], (key[1], key[2]))
                del b[key]
                b[spam] = value
        # print(b)

        with open(file, 'wb') as filee:
            pickle.dump(b, filee)


if __name__ == "__main__":
    pass
    fix_wrong_trim_in_decisions()
    # add_this_config_hash_to_results(after_first_run=True, debug=True)
    # fix_wrong_loaded()
    # check_setting()
    # fix_order_setting()
