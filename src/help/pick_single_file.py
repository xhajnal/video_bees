import os
import config
from analyse import analyse


if __name__ == "__main__":
    os.chdir('..')
    # raise Exception
    a = True
    # analyse("../data/Video_tracking/190904/20190904_155648360_2BEES_generated_20210521_104649_nn.csv", 2, is_first_run=a)
    # analyse("../data/Video_tracking/190920/20190920_145859333_1BEE_generated_20210910_083808_nn.csv", 1)
    # analyse("../data/Video_tracking/190924/20190924_155725679_5BEES_generated_20210917_100221_nn.csv", 5)
    # analyse('../data/Video_tracking/190916/20190916_160703748_1BEE_generated_20210611_111022_nn.csv', 1, is_first_run=a)


    # analyse('../data/Video_tracking/190905/20190905_120614441_2BEES_generated_20210528_103143_nn.csv', 2, has_tracked_video=True, is_first_run=a)
    analyse('../data/Video_tracking/190928/20190928_153817856_2BEES_generated_20211008_100947_nn.csv', 2, is_first_run=a)


    # analyse('../data/Video_tracking/190919/20190919_110353881_1BEE_generated_20210908_084510_nn.csv', 1, is_first_run=a)

    # analyse('../data/Video_tracking/190920/20190920_152130894_5BEES_generated_20210910_085916_nnq.csv', 5, is_first_run=a).