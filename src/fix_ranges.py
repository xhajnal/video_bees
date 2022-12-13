import csv
import os
from time import time
from _socket import gethostname
from termcolor import colored


def fix_ranges(file_path, autodelete=False, debug=False):
    """ Fixes ranges so that the frame with minimal value is set to 1.
    Use this if you trimmed frames of the video from the beginning.


    :arg file_path: (file or str): input file
    :arg autodelete: (bool): if True it deletes the original file
    :arg debug: (bool): if True extensive output is shown
    """
    print(colored("FIX RANGES", "blue"))
    start_time = time()

    file_path = file_path.replace("\\", "/")
    new_file_path = file_path.replace("original/", "")
    lowest_range = -9
    header = []

    if os.path.isfile(new_file_path):
        print(colored(f"file {new_file_path} already exists. We skip {file_path}. It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
        return
    else:
        with open(file_path, newline='') as input_csv_file:
            with open(new_file_path, "w", newline='') as output_csv_file:
                # parse traces from csv file
                traces = dict()
                reader = csv.DictReader(input_csv_file)
                for row in reader:
                    if debug:
                        print(row)
                        print(row.keys())
                    if lowest_range == -9:
                        lowest_range = int(row['frame_number'])
                        header = row.keys()
                        writer = csv.DictWriter(output_csv_file, fieldnames=header)
                        writer.writeheader()

                    row["frame_number"] = str(int(row["frame_number"]) - lowest_range)
                    writer.writerow(row)

                print(colored(f"Loaded {str(file_path)} and saving to {str(new_file_path)}. "
                              f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))

    if autodelete:
        os.remove(file_path)


if __name__ == "__main__":
    # before
    # fix_ranges('../data/Video_tracking/190822/original/20190822_111607344_1BEE_generated_20210430_080914_nn.csv')

    # now using glob - all folders with original files
    from glob import glob
    path = '../data/Video_tracking/'
    # get all folder names
    folders = list(os.walk(path))[0][1]

    for folder in folders:
        path1 = os.path.join(path, folder, 'original')
        # print(path1)
        # print(glob(str(path1)+"/*_nn.csv", recursive=False))

        # get all files in /original/ folder
        for file in glob(str(path1)+"/*_nn.csv", recursive=False):
            # print(file)
            fix_ranges(file, autodelete=False)
