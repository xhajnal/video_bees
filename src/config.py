
def get_distance_from_calculated_arena():
    """ Returns distance from the estimated arena circle to be assigned as outside of the arena."""
    return 50


def get_max_trace_gap():
    """ Returns maximal distance between two traces in frames to be able to merge."""
    return 500


def get_min_trace_length():
    """ Returns a minimal distance of a trace to be merged with other."""
    return 100


def get_bee_max_step_len():
    """ Returns maximal step of a bee in a single frame in xy distance."""
    return 150


def get_screen_size():
    """ Returns size of the screen as [[xmin, xmax],[ymin, ymax]] ."""
    return [[0, 900], [0, 900]]
