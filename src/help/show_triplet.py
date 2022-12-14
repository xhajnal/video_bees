import os

from analyse import analyse

if __name__ == "__main__":
    os.chdir('..')

    # 55 -> 46 -> 21
    analyse("../data/Video_tracking/190823/20190823_154249666_2BEES_generated_20210510_095112_nn.csv", 2, has_tracked_video=True)
