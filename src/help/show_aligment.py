import os
import config
from analyse import analyse


if __name__ == "__main__":
    os.chdir('..')
    ## Delete the respective record in 'auxiliary/transpositions.txt' before running this

    # analyse('../data/Video_tracking/190822/20190822_111607344_1BEE_generated_20210430_080914_nn.csv', 1)
    # raise Exception
    analyse("../data/Video_tracking/190822/20190822_114441236_5BEE_generated_20210503_090128_nn.csv", 5)
