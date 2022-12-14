import os

from analyse import analyse

if __name__ == "__main__":
    os.chdir('..')
    ## 190822
    # # a lot of jump back and forth
    # # one swap of traces
    # # 65 -> 56 -> 25 (12/10/22)
    # # 65 -> 56 -> 2 (16/10/22)
    analyse("../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv", 2, [41159], has_tracked_video=True)
