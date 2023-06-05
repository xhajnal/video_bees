import os
import config
from analyse import analyse


if __name__ == "__main__":
    os.chdir('..')
    # raise Exception
    a = True
    # analyse("../data/Video_tracking/190904/20190904_155648360_2BEES_generated_20210521_104649_nn.csv", 2, is_first_run=a)

    analyse('../data/Video_tracking/test/test_20190930_114339021_2BEES_generated_20211019_104420_nn.csv', 2, is_first_run=a)

