# number of all the overlaps in the file
global all_overlaps_count
all_overlaps_count = 0

# all observed overlaps
global all_seen_overlaps
all_seen_overlaps = 0

# number of merged overlaps
global all_seen_overlaps_deleted
all_seen_overlaps_deleted = 0

# number of deleted from the seen
global all_allowed_overlaps_count
all_allowed_overlaps_count = 0


def get_all_overlaps_count():
    return all_overlaps_count


def get_all_seen_overlaps():
    return all_seen_overlaps


def get_all_seen_overlaps_deleted():
    return all_seen_overlaps_deleted


def get_all_allowed_overlaps_count():
    return all_allowed_overlaps_count


def set_all_overlaps_count(value):
    global all_overlaps_count
    all_overlaps_count = value


def set_all_seen_overlaps(value):
    global all_seen_overlaps
    all_seen_overlaps = value


def set_all_seen_overlaps_deleted(value):
    global all_seen_overlaps_deleted
    all_seen_overlaps_deleted = value


def set_all_allowed_overlaps_count(value):
    global all_allowed_overlaps_count
    all_allowed_overlaps_count = value



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
