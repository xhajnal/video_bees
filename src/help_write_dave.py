import copy
import os.path
from glob import glob

import analyse
from dave_io import load_result


def write_dave():
    """ Writes the dave script main without result values. """
    a = [190822, 190823, 190903, 190904, 190905, 190906, 190916, 190917, 190918, 190919, 190920, 190922, 190924, 190925, 190926, 190927, 190928, 190929, 190930, 191001, 191002, 191003, 191007, 191008, 191011, 191014, 191016, 191017, 191018]

    path = '../data/Video_tracking/'

    print("a = is_first_run")
    for population_size in [1, 2, 5, 7, 10, 15]:
        if population_size == 1:
            print(f"# ############################################# SINGLE BEE #######################################################")
        else:
            print(f"# ############################################# {population_size} BEES #######################################################")
        for folder in a:
            print(f"# ## {folder}")
            for file in glob(f"{path}/{folder}/*_{population_size}BEE*_nn.csv", recursive=False):

                if "part" in file:
                    continue

                file = file.replace("//", "/")
                file = file.replace("\\", "/")
                # folder = os.path.dirname(file)
                # print(folder)

                original_file = copy.copy(file)

                file2 = os.path.basename(file)
                # print(file2)
                file2 = str("_".join(file2.split("_")[:3]))
                # print(file2)
                if glob(f"{path}/{folder}/*{file2}*.mp4", recursive=False):
                    if_video = ", has_tracked_video=True, is_first_run=is_first_run"
                else:
                    if_video = ", is_first_run=a"

                try:
                    file_results = load_result(file_name=f"{original_file}")
                    all_loaded = []
                    all_single = []
                    all_final = []

                    for item in file_results.items():
                        item = item[1]
                        # print(item)
                        all_loaded.append(item["loaded"])
                        try:
                            all_single.append(item["zero length"])
                        except KeyError:
                            pass
                        all_final.append(item["after merging overlapping traces"])

                    if len(set(all_loaded)) != 1:
                        raise Exception(f"{file2} some 'loaded' are not the same")
                    # if len(set(all_single)) != 1:
                    #     raise Exception(f"{file2} some after single are not the same")

                    if all_final[-1] == min(all_final):
                        is_found = "*"
                    else:
                        is_found = ""
                except KeyError:
                    all_loaded = [""]
                    all_single = [""]
                    all_final = [""]
                    is_found = ""

                try:
                    print(f"# # {all_loaded[0]} -> {all_single[0]} -> {all_final[-1]} {is_found}")
                except IndexError:
                    try:
                        print(f"# # {all_loaded[0]} -> {all_single[0]} -> ")
                    except IndexError:
                        try:
                            print(f"# # {all_loaded[0]} -> -> ")
                        except IndexError:
                            print(f"# # -> -> ")

                print(f'# analyse("{file}", {population_size}{if_video})')
                print("#")


if __name__ == "__main__":
    write_dave()
