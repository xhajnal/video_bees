import csv
from time import time
from _socket import gethostname
from termcolor import colored


def fix_ranges(file_path, population_size, debug=False):
    print(colored("FIX RANGES", "blue"))
    start_time = time()

    new_file_path = file_path.replace("original/", "")
    lowest_range = -9
    header = []

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

            print(colored(f"Loaded {len(traces)} traces. It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "yellow"))
            return traces




if __name__ == "__main__":
    ## SINGLE BEE xxxx22
    fix_ranges('../data/Video_tracking/190822/original/20190822_111607344_1BEE_generated_20210430_080914_nn.csv', 1)
    fix_ranges('../data/Video_tracking/190822/original/20190822_141925574_1bee_generated_20210504_081658_nn.csv', 1)

    ## xxxx23
    fix_ranges('../data/Video_tracking/190823/original/20190823_114450691_1BEE_generated_20210506_100518_nn.csv', 1)
    fix_ranges('../data/Video_tracking/190823/original/20190823_153007029_1BEE_generated_20210507_091854_nn.csv', 1)

    ## TWO BEES xxxx22
    fix_ranges('../data/Video_tracking/190822/original/20190822_112842909_2BEE_generated_20210503_074806_nn.csv', 2)
    fix_ranges('../data/Video_tracking/190822/original/20190822_143216366_2bees_generated_20210504_064410_nn.csv', 2)

    ## xxxx23
    fix_ranges('../data/Video_tracking/190823/original/20190823_115857275_2BEES_generated_20210507_083510_nn.csv', 2)
    fix_ranges('../data/Video_tracking/190823/original/20190823_154249666_2BEES_generated_20210510_095112_nn.csv', 2)

    ## FIVE BEES xxxx22
    fix_ranges('../data/Video_tracking/190822/original/20190822_114441236_5BEE_generated_20210503_090128_nn.csv', 5)
    fix_ranges('../data/Video_tracking/190822/original/20190822_144547243_5BEE_generated_20210504_081238_nn.csv', 5)

    ## xxxx23
    fix_ranges('../data/Video_tracking/190823/original/20190823_121326323_5BEES_generated_20210505_103301_nn.csv', 5)
    fix_ranges('../data/Video_tracking/190823/original/20190823_155506355_5BEES_generated_20210507_092606_nn.csv', 5)

    ## SEVEN BEES xxxx22
    fix_ranges('../data/Video_tracking/190822/original/20190822_115819107_7BEE_generated_20210504_064122_nn.csv', 7)

    ## xxxx23
    fix_ranges('../data/Video_tracking/190823/original/20190823_124111790_7BEES_generated_20210507_070601_nn.csv', 7)
    fix_ranges('../data/Video_tracking/190823/original/20190823_161115188_7BEES_generated_20210507_093529_nn.csv', 7)

    ## TEN BEES xxxx22
    fix_ranges('../data/Video_tracking/190822/original/20190822_121127355_10BEE_generated_20210430_102736_nn.csv', 10)
    fix_ranges('../data/Video_tracking/190822/original/20190822_151158355_10BEE_generated_20210504_082545_nn.csv', 10)

    ## xxxx23
    fix_ranges('../data/Video_tracking/190823/original/20190823_162410226_10BEES_generated_20210510_080842_nn.csv', 10)

    ## FIFTEEN BEES xxxx22
    fix_ranges('../data/Video_tracking/190822/original/20190822_122407809_15BEE_generated_20210803_085008_nn.csv', 15)

    ## xxxx23
    fix_ranges('../data/Video_tracking/190823/original/20190823_163934743_15BEES_generated_20210510_082044_nn.csv', 15)
