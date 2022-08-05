from copy import copy

import numpy as np
from interval import Interval
from mpmath import mpi
import pandas as pd
from itertools import islice
from termcolor import colored


def delete_indices(indices, iterable, debug=False):
    """ Deletes given indices from given iterable

    :arg indices: (int): number of items to take
    :arg iterable: (iterable): iterable to delete the items from
    :arg debug: (bool): if True extensive output is shown
    :returns: (list): iterable with deleted items
    """
    indices = set(indices)
    indices = list(reversed(sorted(list(indices))))

    for index in indices:
        if debug:
            name = f'{iterable=}'.split('=')[0]
            print(colored(f"Deleting item {index} from {name}.", "red"))
        del iterable[index]

    return iterable


def take(n, iterable):
    """ Returns first n items of the iterable as a list.

    :arg n: (int): number of items to take
    :arg iterable: (iterable): iterable to take the items from
    :returns: (list): list of n first items
    """
    return list(islice(iterable, n))


def is_in(range1, range2, strict=False):
    """ Returns whether the range1 is in range2.

    :param range1: (tuple or list): first interval
    :arg range2: (tuple or list): second interval
    :arg strict: (bool): flag whether use >,< instead of >=, <=
    :returns: (bool): whether range1 is (strictly) inside range2
    """
    if strict:
        return range1[0] > range2[0] and range1[1] < range2[1]
    else:
        return mpi(range1) in mpi(range2)


def m_overlaps_of_n_intervals(m, intervals):
    """ Returns a matrix of flags of m-overlaps (m overlapping intervals) of n intervals

    :arg m: (int): degree of overlaps - how many overlaps
    :arg intervals: (list): list of intervals
    """
    assert m <= len(intervals)
    if m == 1:
        matrix = np.zeros([len(intervals), len(intervals)])
        for row in range(len(matrix)):
            for column in range(row, len(matrix[0])):
                if has_overlap(intervals[row], intervals[column]):
                    matrix[row][column] = 1
    else:
        matrix = m_overlaps_of_n_intervals(m - 1, intervals)
        for index, x in enumerate(np.nditer(matrix)):
            print(x, end=' ')

    return matrix


def get_overlap(range1, range2):
    """ Returns the overlap of range1 and range2.

    :arg range1: (tuple or list): first interval
    :arg range2: (tuple or list): second interval
    :returns: (tuple): overlap of range1 and range2
    """
    assert len(range1) == 2 or isinstance(range1, Interval)
    assert len(range2) == 2 or isinstance(range2, Interval)
    # if the range1 starts after range2 swap them
    if range2[0] < range1[0]:
        return get_overlap(range2, range1)
    # if beginning of the range2 is inside of range1
    if range1[0] <= range2[0] <= range1[1]:
        return [max(range1[0], range2[0]), min(range1[1], range2[1])]
    else:
        return False


def get_strict_overlap(range1, range2):
    """ Returns the overlap of range1 and range2 only if it is a range of nonzero length.

    :arg range1: (tuple or list): first interval
    :arg range2: (tuple or list): second interval
    :returns: (tuple): overlap of range1 and range2
    """
    spam = get_overlap(range1, range2)
    if spam is False:
        return spam
    if spam[0] == spam[1]:
        return False
    return spam


def has_overlap(range1, range2):
    """ Returns whether the range1 has an overlap with range2.

    :arg range1: (tuple or list): first interval
    :arg range2: (tuple or list): second interval
    :returns: (bool): whether range1 has overlap with range2
    """
    assert len(range1) == 2 or isinstance(range1, Interval)
    assert len(range2) == 2 or isinstance(range2, Interval)
    interval1 = copy(range1)
    interval2 = copy(range2)
    return pd.Interval(interval1[0], interval1[1]).overlaps(pd.Interval(interval2[0], interval2[1]))


def is_before(range1, range2):
    """ Returns whether the range1 is before range2 in whole range.

    :param range1: (tuple or list): first interval
    :arg range2: (tuple or list): second interval
    :returns: (bool): whether range1 is before range2
    """
    assert len(range1) == 2 or isinstance(range1, Interval)
    assert len(range2) == 2 or isinstance(range2, Interval)
    return range1[1] < range2[0]


def merge_dictionary(dict_1, dict_2):
    """ Merges two dictionaries, dict_1 and dict_2, while updating the common keys by summing the values.

    :arg dict_1: (dict): first dictionary
    :arg dict_2: (dict): second dictionary
    :returns: (dict): merged dictionary
    """
    dict_3 = {**dict_1, **dict_2}
    for key, value in dict_3.items():
        if key in dict_1 and key in dict_2:
            dict_3[key] = value + dict_1[key]
    return dict_3
