from copy import copy

from interval import Interval
from mpmath import mpi
import pandas as pd
from itertools import islice


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


def is_in(range1, range2, strict=False):
    """ Returns whether the range1 is in range2.

    :arg range1 (tuple or list) first interval
    :arg range2 (tuple or list) second interval
    :arg strict (bool) flag whether use >,< instead of >=, <=
    """
    if strict:
        return range1[0] > range2[0] and range1[1] < range2[1]
    else:
        return mpi(range1) in mpi(range2)


def has_overlap(range1, range2):
    assert len(range1) == 2 or isinstance(range1, Interval)
    assert len(range2) == 2 or isinstance(range2, Interval)
    interval1 = copy(range1)
    interval2 = copy(range2)
    return pd.Interval(interval1[0], interval1[1]).overlaps(pd.Interval(interval2[0], interval2[1]))


def is_before(range1, range2):
    assert len(range1) == 2 or isinstance(range1, Interval)
    assert len(range2) == 2 or isinstance(range2, Interval)
    return range1[1] < range2[0]


def merge_dictionary(dict_1, dict_2):
    dict_3 = {**dict_1, **dict_2}
    for key, value in dict_3.items():
        if key in dict_1 and key in dict_2:
            dict_3[key] = value + dict_1[key]
    return dict_3
