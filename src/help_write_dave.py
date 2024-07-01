import copy
import os.path
from glob import glob

import analyse
from config import hash_config
from dave_io import load_result


## TODO ATTENTION CASE SPECIFIC
def write_dave(show_first_run_result=False, show_second_run_result=False, get_for_current_hash=True):
    """ Writes the dave script.

    arg: show_first_run_result (bool): whether to show the results of the first run
    arg: show_second_run_result (bool): whether to show the results of the second run
    arg: get_for_current_hash (bool): whether to obtain the results for the current hash, otherwise the ast result is used
    """
    ## INITIATION
    # PATH TO THE FILES
    path = '../data/Video_tracking/'

    # LIST OF DATA FOLDERS
    a = [2024, 190822, 190823, 190903, 190904, 190905, 190906, 190916, 190917, 190918, 190919, 190920, 190922, 190924, 190925, 190926, 190927, 190928, 190929, 190930, 191001, 191002, 191003, 191007, 191008, 191011, 191014, 191016, 191017, 191018]

    # LIST OF POPULATION SIZES
    population_sizes = [1, 2, 5, 7, 10, 15]

    # Get current hash
    if get_for_current_hash:
        my_hash = str(hash_config())
    else:
        my_hash = None

    # RUN
    print("a = is_first_run")
    for population_size in population_sizes:
        if population_size == 1:
            print(f"# ############################################# SINGLE BEE #######################################################")
        else:
            print(f"# ############################################# {population_size} BEES #######################################################")
        for folder in a:
            print(f"# ## {folder}")
            # find csv files with xBee in name ending with _nn
            for file in glob(f"{path}/{folder}/*_{population_size}[B|b][E|e][E|e]*_nn.csv", recursive=False):

                # skip loopy results which have more parts
                if "part" in file:
                    continue

                file = file.replace("//", "/")
                file = file.replace("\\", "/")
                # folder = os.path.dirname(file)
                # print(folder)

                original_file = copy.copy(file)

                short_file_name = os.path.basename(file)
                # print(short_file_name)
                short_file_name = str("_".join(short_file_name.split("_")[:3]))
                # print(short_file_name)
                if glob(f"{path}/{folder}/movie*{short_file_name}*.mp4", recursive=False):
                    if_video = ", has_tracked_video=True, is_first_run=a"
                else:
                    if_video = ", is_first_run=a"

                # print("#")
                # print("#")
                if show_first_run_result:
                    print_result(original_file, True, get_for_current_hash, my_hash, short_file_name)

                if show_second_run_result:
                    print_result(original_file, False, get_for_current_hash, my_hash, short_file_name)

                print(f"# analyse('{file}', {population_size}{if_video})")
                print("#")


def print_result(original_file, is_first_run, get_for_current_hash, my_hash, short_file_name):
    if is_first_run:
        which_run = "1stRun"
    else:
        which_run = "finalRun"

    try:
        file_results = load_result(file_name=f"{original_file}", is_first_run=is_first_run)
        all_loaded = []
        all_single = []
        all_final = []

        for hash in file_results.keys():
            if get_for_current_hash:
                if hash != my_hash:
                    continue
            for time_stamp in file_results[hash].keys():
                item = file_results[hash][time_stamp]
                # print(item)

                ## TODO hotfix
                if all_loaded:
                    if item["loaded"] not in all_loaded:
                        continue

                all_loaded.append(item["loaded"])
                try:
                    all_single.append(item["zero length"])
                except KeyError:
                    pass
                all_final.append(item["after merging overlapping traces"])

        if len(all_loaded) == 0:
            err = f"No loaded results for file {short_file_name} in {which_run}"
            raise LookupError(err)
        if len(set(all_loaded)) != 1:
            err = f"In {which_run}, {short_file_name} some 'loaded' are not the same: {all_loaded}"
            raise Exception(err)

        if all_final[-1] == min(all_final):
            is_found = "*"
        else:
            is_found = ""
    except KeyError:
        all_loaded = [""]
        all_single = [""]
        all_final = [""]
        is_found = ""
    except FileNotFoundError:
        all_loaded = [""]
        all_single = [""]
        all_final = [""]
        is_found = ""
    except LookupError:
        all_loaded = [""]
        all_single = [""]
        all_final = [""]
        is_found = ""

    try:
        print(f"# # {which_run} {all_loaded[0]} -> {all_single[0]} -> {all_final[-1]} {is_found}")
    except IndexError:
        try:
            print(f"# # {which_run} {all_loaded[0]} -> {all_single[0]} -> ")
        except IndexError:
            try:
                print(f"# # {which_run} {all_loaded[0]} -> -> ")
            except IndexError:
                print(f"# # {which_run} -> -> ")


if __name__ == "__main__":
    write_dave(show_first_run_result=True, show_second_run_result=True, get_for_current_hash=True)
