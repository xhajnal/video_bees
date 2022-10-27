import json
from time import time
from termcolor import colored


def check_setting():
    """
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


if __name__ == "__main__":
    check_setting()
