import os
from analyse import analyse


if __name__ == "__main__":
    os.chdir('..')
    # raise Exception
    a = True
    # analyse("../data/Video_tracking/190904/20190904_155648360_2BEES_generated_20210521_104649_nn.csv", 2, is_first_run=a)

    # analyse('../data/Video_tracking/test/test_20190930_114339021_2BEES_generated_20211019_104420_nn.csv', 2, is_first_run=True)
    # analyse('../data/Video_tracking/test/test_20190930_114339021_2BEES_generated_20211019_104420_nn.csv', 2, is_first_run=False)
    # analyse('../data/Video_tracking/test/test_20190930_114339021_2BEES_generated_20211019_104420_nn.csv', 2,
    #         to_purge=True, is_first_run=True)

    analyse('../data/Video_tracking/test/test_20190930_112905317_1BEE_generated_20211019_103540_nn.csv', 2, is_first_run=True)
    analyse('../data/Video_tracking/test/test_20190930_112905317_1BEE_generated_20211019_103540_nn.csv', 2, is_first_run=False)
    analyse('../data/Video_tracking/test/test_20190930_112905317_1BEE_generated_20211019_103540_nn.csv', 2, to_purge=True, is_first_run=True)

    # analyse('../data/Video_tracking/test/20190930_140834155_5BEES_generated_20211020_104342_nn.csv', 5, is_first_run=True)
    # analyse('../data/Video_tracking/test/20190930_140834155_5BEES_generated_20211020_104342_nn.csv', 5, is_first_run=False)


