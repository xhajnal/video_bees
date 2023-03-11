# number of all the overlaps in the file
global single_run_overlaps_count
single_run_overlaps_count = 0

# all observed overlaps
global single_run_seen_overlaps
single_run_seen_overlaps = 0

# number of merged overlaps
global single_run_seen_overlaps_deleted
single_run_seen_overlaps_deleted = 0

# number of deleted from the seen
global single_run_allowed_overlaps_count
single_run_allowed_overlaps_count = 0


def get_single_run_overlaps_count():
    return single_run_overlaps_count


def get_single_run_seen_overlaps():
    return single_run_seen_overlaps


def get_single_run_seen_overlaps_deleted():
    return single_run_seen_overlaps_deleted


def get_single_run_allowed_overlaps_count():
    return single_run_allowed_overlaps_count


def set_single_run_overlaps_count(value):
    global single_run_overlaps_count
    single_run_overlaps_count = value


def set_single_run_seen_overlaps(value):
    global single_run_seen_overlaps
    single_run_seen_overlaps = value


def set_single_run_seen_overlaps_deleted(value):
    global single_run_seen_overlaps_deleted
    single_run_seen_overlaps_deleted = value


def set_single_run_allowed_overlaps_count(value):
    global single_run_allowed_overlaps_count
    single_run_allowed_overlaps_count = value


# number of all the overlaps in the file
global this_file_overlaps_count
this_file_overlaps_count = 0

# all observed overlaps
global this_file_seen_overlaps
this_file_seen_overlaps = 0

# number of merged overlaps
global this_file_seen_overlaps_deleted
this_file_seen_overlaps_deleted = 0

# number of deleted from the seen
global this_file_allowed_overlaps_count
this_file_allowed_overlaps_count = 0


def get_this_file_overlaps_count():
    return this_file_overlaps_count


def get_this_file_seen_overlaps():
    return this_file_seen_overlaps


def get_this_file_seen_overlaps_deleted():
    return this_file_seen_overlaps_deleted


def get_this_file_allowed_overlaps_count():
    return this_file_allowed_overlaps_count


def set_this_file_overlaps_count(value):
    global this_file_overlaps_count
    this_file_overlaps_count = value


def set_this_file_seen_overlaps(value):
    global this_file_seen_overlaps
    this_file_seen_overlaps = value


def set_this_file_seen_overlaps_deleted(value):
    global this_file_seen_overlaps_deleted
    this_file_seen_overlaps_deleted = value


def set_this_file_allowed_overlaps_count(value):
    global this_file_allowed_overlaps_count
    this_file_allowed_overlaps_count = value



# cumulative number of all the overlaps in the file
global cumulative_all_overlaps_count
cumulative_all_overlaps_count = 0

# cumulative all observed overlaps
global cumulative_all_seen_overlaps
cumulative_all_seen_overlaps = 0

# cumulative number of merged overlaps
global cumulative_all_seen_overlaps_deleted
cumulative_all_seen_overlaps_deleted = 0

# cumulative number of deleted from the seen
global cumulative_all_allowed_overlaps_count
cumulative_all_allowed_overlaps_count = 0


def get_cumulative_all_overlaps_count():
    return cumulative_all_overlaps_count


def get_cumulative_all_seen_overlaps():
    return cumulative_all_seen_overlaps


def get_cumulative_all_seen_overlaps_deleted():
    return cumulative_all_seen_overlaps_deleted


def get_cumulative_all_allowed_overlaps_count():
    return cumulative_all_allowed_overlaps_count


def set_cumulative_all_overlaps_count(value):
    global cumulative_all_overlaps_count
    cumulative_all_overlaps_count = value


def set_cumulative_all_seen_overlaps(value):
    global cumulative_all_seen_overlaps
    cumulative_all_seen_overlaps = value


def set_cumulative_all_seen_overlaps_deleted(value):
    global cumulative_all_seen_overlaps_deleted
    cumulative_all_seen_overlaps_deleted = value


def set_cumulative_all_allowed_overlaps_count(value):
    global cumulative_all_allowed_overlaps_count
    cumulative_all_allowed_overlaps_count = value


def update_this_file_counts():
    set_this_file_overlaps_count(get_this_file_overlaps_count() + get_single_run_overlaps_count())
    set_this_file_seen_overlaps(get_this_file_seen_overlaps() + get_single_run_seen_overlaps())
    set_this_file_allowed_overlaps_count(get_this_file_allowed_overlaps_count() + get_single_run_allowed_overlaps_count())
    set_this_file_seen_overlaps_deleted(get_this_file_seen_overlaps_deleted() + get_single_run_seen_overlaps_deleted())


def reset_this_file_counts():
    set_this_file_overlaps_count(0)
    set_this_file_seen_overlaps(0)
    set_this_file_allowed_overlaps_count(0)
    set_this_file_seen_overlaps_deleted(0)


def update_cumulative_counts():
    set_cumulative_all_overlaps_count(get_cumulative_all_overlaps_count() + get_this_file_overlaps_count())
    set_cumulative_all_seen_overlaps(get_cumulative_all_seen_overlaps() + get_this_file_seen_overlaps())
    set_cumulative_all_allowed_overlaps_count(get_cumulative_all_allowed_overlaps_count() + get_this_file_allowed_overlaps_count())
    set_cumulative_all_seen_overlaps_deleted(get_cumulative_all_seen_overlaps_deleted() + get_this_file_seen_overlaps_deleted())


def print_single_call():
    return f"{get_single_run_overlaps_count()}; {get_single_run_seen_overlaps()}; {get_single_run_allowed_overlaps_count()}; {get_single_run_seen_overlaps_deleted()};"


def print_this_file():
    return f"{get_this_file_overlaps_count()}; {get_this_file_seen_overlaps()}; {get_this_file_allowed_overlaps_count()}; {get_this_file_seen_overlaps_deleted()}"


def print_cumulative():
    return f"{get_cumulative_all_overlaps_count()}; {get_cumulative_all_seen_overlaps()}; {get_cumulative_all_allowed_overlaps_count()}; {get_cumulative_all_seen_overlaps_deleted()}"
