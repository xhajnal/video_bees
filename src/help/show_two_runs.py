from analyse import analyse, set_just_annotate, set_force_new_video
import os
import config
from analyse import analyse


def run_both():
    """ Runs both, the first and the second run. """
    run(is_first_run=True)
    run(is_first_run=False)


def run_just_annotate():
    """ Runs only annotation from the pickled file. """
    set_just_annotate(True)
    set_force_new_video(True)
    run()
    set_just_annotate(False)
    set_force_new_video(False)


def run(is_first_run=None):
    analyse("../data/Video_tracking/190903/20190903_134034775_1BEE_generated_20210511_083234_nn.csv", 1, is_first_run=is_first_run)

    # 62 -> 29 -> 1 Done, video checked, passed
    analyse("../data/Video_tracking/190903/20190903_172942424_1BEE_generated_20210520_073610_nn.csv", 1,
            has_tracked_video=True, is_first_run=is_first_run)


if __name__ == "__main__":
    os.chdir('..')
    # run_both()
    run_just_annotate()
