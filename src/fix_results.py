import json
from time import time
from termcolor import colored

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
    # check_setting()
    fix_order_setting()
