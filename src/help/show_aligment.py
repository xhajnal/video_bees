import os
import config
from analyse import analyse


if __name__ == "__main__":
    os.chdir('..')
    ## 190822
    # 1416 -> 1091 -> 679
    # GOT VIDEO
    analyse("../data/Video_tracking/190822/20190822_114441236_5BEE_generated_20210503_090128_nn.csv", 5)
