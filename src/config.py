def get_distance_from_calculated_arena():
    """ Returns distance from the estimated arena circle to be assigned as outside of the arena."""
    # Usage: outside of arena
    return 53


def get_max_trace_gap():
    """ Returns maximal distance between two traces in frames to be able to merge.
        Effectively computes how long an agent can hide from being tracked (max_trace_gap / frame rate).
    """
    # Usage: gaping trace - ABOVE
    return 150


def get_min_trace_length():
    """ Returns a minimal length of a trace to be merged with the other."""
    # TODO FIND THIS
    # Usage: gaping traces
    return 10


def get_bee_max_step_len():
    """ Returns maximal step of a bee in a single frame in xy distance."""
    # TODO check this
    # Usage: gaping traces - LONG gap
    return 50


def get_bee_max_step_len_per_frame():
    """ Returns maximal step of a bee in a single frame in xy distance in continuous manner over more than 50 frames."""
    # TODO check this
    # Usage: gaping traces - SHORT gap
    return 28


def get_max_trace_gap_to_interpolate_distance():
    """ Returns a maximal distance in frames so that the location of the bee is linearly interpolated based on border points. """
    # TODO check this
    # Usage: gaping traces, whether to calculate the location in the gap
    return 100  # 1 second (as frame rate is 100)


def get_max_step_distance_to_merge_overlapping_traces():
    """ Returns a maximal distance two traces can differ in any point to be not merged."""
    # TODO check this
    # Usage: overlapping traces
    return 200


def get_maximal_distance_to_check_for_trace_swapping():
    """ Returns a maximal distance in xy of two traces at a certain frame to check whether the traces are not swapped."""
    return 100


def get_force_merge_vicinity():
    """ Returns range for which there should be no overlap in order to force merge overlapping traces."""
    # TODO apply this to gaping traces
    # Usage: merge_overlapping_traces
    return 200


def get_screen_size():
    """ Returns size of the screen as [[xmin, xmax],[ymin, ymax]] ."""
    return [[0, 900], [0, 900]]
