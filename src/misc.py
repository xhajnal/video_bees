from copy import copy

from interval import Interval
from mpmath import mpi
import pandas as pd


def is_in(range1, range2):
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
