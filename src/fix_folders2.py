import glob
import os
import shutil
from pathlib import Path

from src.config import hash_config
my_hash = str(hash_config())
os.chdir("../data/Video_tracking")

## for each subfolder (day of tracking)
for folder in next(os.walk('.'))[1]:
    print(folder)
    os.chdir(folder)
    os.chdir("after_first_run")
    os.chdir(my_hash)
    # try:
    #     os.mkdir(hash)
    # except:
    #     pass
    for file in glob.glob(f"*.csv"):
        file = os.path.basename(file)
        file2 = Path(file).stem + ".p"
        print("file", file)
        print("file", file2)
        shutil.move(file, file2)

    os.chdir("..")

    try:
        os.removedirs("9155820875805629244")
    except Exception as err:
        print(err)
        pass

    os.chdir("..")
    os.chdir("..")
    print()
