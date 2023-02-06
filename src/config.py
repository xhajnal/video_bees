## ARENA SETTING
def get_distance_from_calculated_arena():
    """ Returns distance from the estimated arena circle to be assigned as outside of the arena."""
    # Usage: outside of arena
    return 50


## SINGLE TRACE SETTING
def get_min_trace_len():
    """ Return minimal value of a trace len in frames to be kept."""
    return 100


def get_bee_max_step_len():
    """ Returns maximal step of a bee in a single frame in xy distance."""
    # TODO check this value
    # Usage: gaping traces - LONG gap
    return 70


def get_bee_max_step_len_per_frame():
    """ Returns maximal step of a bee in a single frame in xy distance in continuous manner.
        We recommend to set this value lower than get_bee_max_step_len"""
    # TODO check this value
    # Usage: gaping traces - SHORT gap
    return 20


## TWO TRACES SETTING (GAPS AND OVERLAPS SETTING)

def get_min_trace_length_to_merge():
    """ Returns a minimal length of a trace to be merged with the other."""
    # Usage: gaping traces
    return 50


def get_max_trace_gap():
    """ Returns maximal distance between two traces in frames to be able to merge.
        Effectively computes how long an agent can hide from being tracked (max_trace_gap / frame rate).
    """
    # Usage: gaping trace - ABOVE
    return 100


def get_max_step_distance_to_merge_overlapping_traces():
    """ Returns a maximal distance two traces can differ in any point to be NOT merged."""
    # TODO check this value
    # Usage: overlapping traces
    return 120


def get_min_step_distance_to_merge_overlapping_traces():
    """ Returns a minimal distance two traces can differ in any point to be merged.
        In other words, the two traces have to be at least this near at any point to be merged.
    """
    # TODO check this value
    # Usage: overlapping traces
    return 49


def get_force_merge_vicinity_distance():
    """ Returns min range for which there should be no overlap in order to force merge traces."""
    # Usage: merge_overlapping_traces
    return 508


def get_vicinity_of_short_traces():
    """ Returns number of frames short traces need to be at least far from other short trace to be trimmed."""
    return 200


def get_maximal_distance_to_check_for_trace_swapping():
    """ Returns a maximal distance in xy of two traces at a certain frame to check whether the traces are not swapped."""
    return 100


def get_max_trace_gap_to_interpolate_distance():
    """ Returns a maximal distance in frames so that the location of the bee is linearly interpolated based on border points."""
    # TODO check this value
    # Usage: gaping traces, whether to calculate the location in the gap
    return 50  # 1 second (as frame rate is 100)


## CAMERA / VIDEO SETTING
def get_screen_size():
    """ Returns size of the screen as [[xmin, xmax],[ymin, ymax]] . (To be) Used only in visualisations."""
    return [[0, 900], [0, 900]]


def hash_config(this=True):
    """ Creates a hash of the given config file."""
    if this is True:
        setting = (get_distance_from_calculated_arena(),
                   get_min_trace_len(),
                   get_vicinity_of_short_traces(),
                   get_max_trace_gap(),
                   get_min_trace_length_to_merge(),
                   get_bee_max_step_len(),
                   get_bee_max_step_len_per_frame(),
                   get_max_trace_gap_to_interpolate_distance(),
                   get_max_step_distance_to_merge_overlapping_traces(),
                   get_min_step_distance_to_merge_overlapping_traces(),
                   get_force_merge_vicinity_distance(),
                   tuple([item for sublist in get_screen_size() for item in sublist]))
    else:
        assert isinstance(this, list)
        setting = (this[0],
                   this[1],
                   this[2],
                   this[3],
                   this[4],
                   this[5],
                   this[6],
                   this[7],
                   this[8],
                   this[9],
                   this[10],
                   tuple([item for sublist in this[11] for item in sublist]))

    return str(abs(hash(setting)))


if __name__ == "__main__":
    print(hash_config())
