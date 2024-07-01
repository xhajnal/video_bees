import glob
import os
import shutil

os.chdir("../../data/Video_tracking")

## for each subfolder (day of tracking)
for folder in next(os.walk('..'))[1]:
    print(folder)
    # make a folder original inside
    try:
        os.mkdir(f"{folder}/original")
    except:
        pass

    os.chdir(folder)

    # move all files from the loopy folder one up
    for file in glob.glob(f"deep*/*"):
        # print("file", file)
        shutil.move(file, f"{os.path.basename(file)}")

    # remove the old folder
    try:
        print(os.listdir(glob.glob(f"deep*")[0]))
        if len(os.listdir(glob.glob(f"deep*")[0])) == 0:
            os.removedirs(glob.glob(f"deep*")[0])
    except IndexError:
        pass

    # move all the csv files to folder original
    for file in glob.glob(f"*.csv"):
        # print("file", os.path.basename(file))
        shutil.move(f"{os.path.basename(file)}", f"original/{os.path.basename(file)}")

    os.chdir("../..")
    print()
