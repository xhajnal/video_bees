import os
import config
from analyse import analyse


if __name__ == "__main__":
    os.chdir('..')
    # raise Exception
    analyse("../data/Video_tracking/190920/20190920_145859333_1BEE_generated_20210910_083808_nn.csv", 5)
