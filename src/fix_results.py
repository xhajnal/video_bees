import json
from time import time
from termcolor import colored

import analyse
from config import hash_config
from dave_io import convert_results_from_json_to_csv


def check_setting():
    """ Fixes population size column,

    """
    print(colored("SAVE SETTING AND COUNTS OF TRACES AS JSON", "blue"))
    start_time = time()

    ## LOAD SAVED RESULTS TO UPDATE IT
    with open("../output/results.txt") as file:
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

    with open("../output/results.txt", 'w') as file:
        file.write(json.dumps(results))


def add_this_config_hash_to_results():
    """ Adds the config hash to the result."""
    new_results = {}

    with open("../output/results.txt") as file:
        results = json.load(file)

    for file in results.keys():
        for time_stamp in results[file].keys():
            print(results[file][time_stamp])

            # setting = (get_distance_from_calculated_arena(),
            #            get_min_trace_len(),
            #            get_vicinity_of_short_traces(),
            #            get_max_trace_gap(),
            #            get_min_trace_length_to_merge(),
            #            get_bee_max_step_len(),
            #            get_bee_max_step_len_per_frame(),
            #            get_max_trace_gap_to_interpolate_distance(),
            #            get_max_step_distance_to_merge_overlapping_traces(),
            #            get_force_merge_vicinity_distance(),
            #            tuple([item for sublist in get_screen_size() for item in sublist]))

            try:
                min_trace_len = results[file][time_stamp]['min_trace_len']
            except KeyError:
                min_trace_len = -1

            try:
                min_trace_length_to_merge = results[file][time_stamp]['min_trace_length']
            except KeyError:
                try:
                    min_trace_length_to_merge = results[file][time_stamp]['bee_min_trace_len']
                except KeyError:
                    min_trace_length_to_merge = -1


            try:
                force_merge_vicinity_distance = results[file][time_stamp]['force_merge_vicinity']
            except KeyError:
                force_merge_vicinity_distance = -1

            this_config_hash = hash_config(this=[results[file][time_stamp]['distance_from_calculated_arena'],
                                                 min_trace_len,
                                                 -1,
                                                 results[file][time_stamp]['max_trace_gap'],
                                                 min_trace_length_to_merge,
                                                 results[file][time_stamp]['bee_max_step_len'],
                                                 results[file][time_stamp]['bee_max_step_len_per_frame'],
                                                 results[file][time_stamp]['max_trace_gap_to_interpolate_distance'],
                                                 results[file][time_stamp]['max_step_distance_to_merge_overlapping_traces'],
                                                 force_merge_vicinity_distance,
                                                 results[file][time_stamp]['screen_size']])

            try:
                a = new_results[file]
            except KeyError:
                new_results[file] = {}

            try:
                a = new_results[file][this_config_hash]
            except KeyError:
                new_results[file][this_config_hash] = {}

            try:
                a = new_results[file][this_config_hash][time_stamp]
            except KeyError:
                new_results[file][this_config_hash][time_stamp] = {}

            new_results[file][this_config_hash][time_stamp] = results[file][time_stamp]

    print(new_results)

    with open("../output/results.txt", 'w') as file:
        file.write(json.dumps(new_results))

add_this_config_hash_to_results()

## BEE SPECIFIC
def fix_order_setting():
    """ Fixes order of records. Trim parts from record."""
    print(colored("SAVE SETTING AND COUNTS OF TRACES AS JSON", "blue"))
    start_time = time()

    ## LOAD SAVED RESULTS TO UPDATE IT
    with open("../output/results.txt") as file:
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

    with open("../output/results.txt", 'w') as file:
        file.write(json.dumps(results1))

    convert_results_from_json_to_csv()


if __name__ == "__main__":
    pass
    # check_setting()
    # fix_order_setting()
