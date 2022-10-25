import os.path
from glob import glob

a = [190822, 190823, 190903, 190904, 190905, 190906, 190916, 190917, 190918, 190919, 190920, 190922, 190924, 190925, 190926, 190927, 190928, 190929, 190930, 191001, 191002, 191003, 191007, 191008, 191011, 191014, 191016, 191017, 191018]

path = '../data/Video_tracking/'


for population_size in [1, 2, 5, 7, 10, 15]:
    if population_size == 1:
        print(f"# ############################################# SINGLE BEE #######################################################")
    else:
        print(f"# ############################################# {population_size} BEES #######################################################")
    for item in a:
        print(f"# ## {item}")
        for file in glob(f"{path}/{item}/*{population_size}BEE*_nn.csv", recursive=False):

            file = file.replace("//", "/")
            file = file.replace("\\", "/")
            # folder = os.path.dirname(file)
            # print(folder)
            file2 = os.path.basename(file)
            # print(file2)
            file2 = str("_".join(file2.split("_")[:3]))
            if glob(f"{path}/{item}/*{file2}*.mp4", recursive=False):
                if_video = " ## has video"
            else:
                if_video = ""
            print("# # -> -> ")
            print(f'# analyse("{file}", {population_size}) {if_video}')
            print("#")
