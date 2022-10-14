import sys
from copy import copy
import numpy as np
from interval import Interval
from mpmath import mpi
import pandas as pd
from itertools import islice

from scipy import spatial
from termcolor import colored


def calculate_cosine_distance(a, b):
    return float(spatial.distance.cosine(a, b))


def calculate_cosine_similarity(a, b):
    return 1 - calculate_cosine_distance(a, b)


def to_vect(point1, point2):
    """ Returns a vector of two given points"""
    return [y - x for x, y in zip(point1, point2)]


def nice_range_print(interval):
    """ Prints the shortest frame range

    Eg. 605 - 610  ->  605-10

    :arg interval: (pair of numbers): range to print
    """
    a = f"{interval[0]}"
    b = f"{interval[1]}"

    # if the ranges are different in magnitude
    if len(a) != len(b):
        return f"{interval[0]} - {interval[1]}"
    else:
        i = 0
        # compute number of same digits from left
        for index in range(len(a)):
            if a[index] == b[index]:
                i = i + 1
            else:
                break

        if i == 0:
            return f"{interval[0]} - {interval[1]}"

        return f"{interval[0]}-{str(interval[1])[i:]}"


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


def flatten(data):
    if isinstance(data, tuple):
        if len(data) == 0:
            return ()
        else:
            return flatten(data[0]) + flatten(data[1:])
    else:
        return (data,)


def range_len(interval):
    """ Returns the length of the range.

    :arg interval: (tuple or list): range to compute its length
    """
    assert len(interval) == 2
    return interval[1] - interval[0]


def is_in(range1, range2, strict=False):
    """ Returns whether the range1 is in range2.

    :arg range1: (tuple or list): first interval
    :arg range2: (tuple or list): second interval
    :arg strict: (bool): flag whether use >,< instead of >=, <=
    :returns: (bool): whether range1 is (strictly) inside range2
    """
    if strict:
        return range1[0] > range2[0] and range1[1] < range2[1]
    else:
        return mpi(range1) in mpi(range2)

#
# def get_submatrix(matrix, indices):
#     """ Return submatrix/item such as matrix[indices[0]][indices[1]]...
#
#     :arg matrix: (np.array): array to get the submatrix/item from
#     :arg indices: (list of int): list of indices to obtain the submatrix/item
#     """
#     if len(indices) == 1:
#         return matrix[indices[0]]
#     else:
#         matrix2 = matrix[indices[0]]
#         indices = indices[1:]
#         return get_submatrix(matrix2, indices)

#
# def set_submatrix(matrix, indices, value):
#     """ Return matrix such that submatrix/value, matrix[indices[0]][indices[1]]..., is equal to value
#
#     :arg matrix: (np.array): array to change
#     :arg indices: (list of int): list of indices to change submatrix/item
#     :arg value: the value to set the submatrix/item to
#     """
#     if len(indices) == 1:
#         matrix[indices[0]] = value
#         return matrix
#     else:
#         matrix2 = matrix[indices[0]]
#         indices = indices[1:]
#         return get_submatrix(matrix2, indices)


## DEPRICATED
def m_overlaps_of_n_intervals(m, intervals, strict=False, debug=False):
    """ Returns a dictionary index -> m overlapping interval of n intervals.
        No key if there is no interval.

        :arg m: (int): degree of overlaps - how many overlaps
        :arg intervals: (list): list of intervals
        :arg strict: (bool): if True point intervals are not used
        :arg debug: (bool): if True extensive output is shown
        """
    dictionary = dict()
    matrix = matrix_of_m_overlaps_of_n_intervals(m, intervals, strict, debug)

    ## Iterate through the matrix
    for idx, x in np.ndenumerate(matrix):
        if tuple(sorted(idx)) in dictionary.keys():
            if debug:
                print(f"skipping index {idx} as the index is not sorted hence it is a duplicated pair")
            continue
        dictionary[tuple(sorted(idx))] = matrix[idx]

    ## Trim out non-intervals items
    dictionary2 = dict()
    for key in dictionary.keys():
        item = dictionary[key]
        if item is None or item == 0 or item == 9 or item is False:
            pass
        else:
            assert isinstance(item, list)
            dictionary2[key] = item

    print(dictionary2)
    return dictionary2


def dictionary_of_gaps(intervals, debug=False):
    """ Returns a dictionary a pair of traces -> range of its gap

        :arg intervals: (list): list of intervals
        :arg debug: (bool): if True extensive output is shown
        """


def dictionary_of_m_overlaps_of_n_intervals(m, intervals, skip_whole_in=False, debug=False):
    """ Returns a dictionary m-tuple of interval indices -> m-overlaps (m overlapping intervals) of n intervals

    :arg m: (int): degree of overlaps - how many overlaps
    :arg intervals: (list): list of intervals
    :arg skip_whole_in: (bool): if True skipping the intervals which are overlapping with whole range
    :arg debug: (bool): if True extensive output is shown
    """
    ## INTERN values:
    # False - no interval
    # 9     - index is not sorted hence it is a duplicated pair
    # 0     - skipped as default value
    try:
        assert m <= len(intervals)
    except AssertionError as err:
        print("m", m)
        print("intervals", intervals)
        raise err
    assert m > 1
    dictionary = {}

    for index1, range1 in enumerate(intervals):
        for index2, range2 in enumerate(intervals):
            if index1 >= index2:
                continue
            if has_overlap(range1, range2):
                # to skip the intervals which are overlapping with whole range
                if skip_whole_in:
                    if is_in(range1, range2) or is_in(range2, range1):
                        continue
                dictionary[(index1, index2)] = get_overlap(range1, range2)
    if debug:
        print("dictionary m=2", dictionary)

    for j in list(range(3, m + 1)):
        dictionary2 = copy(dictionary)
        del dictionary
        dictionary = {}
        for overlap_indices in dictionary2.keys():
            for index, rangee in enumerate(intervals):
                if index in overlap_indices:
                    continue
                elif has_overlap(rangee, dictionary2[overlap_indices]):
                    new_index = overlap_indices + (index,)
                    new_index = tuple(list(sorted(list(new_index))))
                    dictionary[new_index] = get_overlap(rangee, dictionary2[overlap_indices])
                if debug:
                    print(f"dictionary m={j}", dictionary)

    return dictionary


# DEPRECATED
def matrix_of_m_overlaps_of_n_intervals(m, intervals, strict=False, debug=False):
    """ Returns a matrix of flags of m-overlaps (m overlapping intervals) of n intervals

    :arg m: (int): degree of overlaps - how many overlaps
    :arg intervals: (list): list of intervals
    :arg strict: (bool): if True point intervals are not used
    :arg debug: (bool): if True extensive output is shown

    :returns matrix: matrix of flags of m-overlaps (m overlapping intervals) of n intervals
    """
    ## INTERN values:
    # False - no interval
    # 9     - index is not sorted hence it is a duplicated pair
    # 0     - skipped as default value

    try:
        assert m <= len(intervals)
    except AssertionError as err:
        print("m", m)
        print("intervals", intervals)
        raise err
    assert m > 1

    if m == 2:
        matrix = np.zeros([len(intervals), len(intervals)], dtype=object)
        foo = np.zeros([len(intervals), len(intervals)], dtype=object)
        for row in range(len(matrix)):
            for column in range(row, len(matrix)):
                # print(colored(f"row, column: {row}, {column}", "white"))
                if row == column:
                    matrix[row][column] = None
                # elif has_overlap(intervals[row], intervals[column]):
                else:
                    # print(colored(f"row, column: {row}, {column}", "yellow"))
                    matrix[row][column] = get_overlap(intervals[row], intervals[column])
    else:
        matrix2 = matrix_of_m_overlaps_of_n_intervals(m - 1, intervals, strict, debug)
        matrix = np.zeros([len(intervals)]*m, dtype=object)
        foo = np.zeros([len(intervals)]*m, dtype=object)

        if debug:
            print("matrix2.shape", matrix2.shape)
            print("matrix.shape", matrix.shape)

        # for index, x in enumerate(np.nditer(matrix2)):
        #     print(x, end=' ')

        # Gonna join each overlap of m-1 intervals with mth interval by overlap of these intervals
        for idx, x in np.ndenumerate(matrix):
            foo[idx] = idx
            # if the indices are not sorted - hence duplicated pair
            if list(sorted(idx)) != list(idx):
                if debug:
                    print(f"setting index {idx} as None because the index is not sorted hence it is a duplicated pair")
                matrix[idx] = 9
                continue
            # if there is a duplicate index
            if len(set(idx)) != len(idx):
                if debug:
                    print(f"setting index {idx} as None because it contains a duplicated interval index")
                matrix[idx] = None
                continue
            if debug:
                print(idx, x)
            spam = matrix2[idx[:-1]]
            if debug:
                print("spam", spam)
            # if the interval of the previous matrix has no overlap
            if spam is False:
                matrix[idx] = False
            elif isinstance(spam, int):
                if spam == 0:
                    matrix[idx] = 0
                if spam == 9:
                    matrix[idx] = 9
                else:
                    raise Exception("David, I am afraid I have done a mistake. After all, I am just a computer.")
            elif len(spam) >= 2:
                if len(spam) > 2:
                    print("spam", spam)
                    raise Exception("David, I am afraid I have done a mistake. After all, I am just a computer.")
                if debug:
                    print("intervals[idx[-1]]", intervals[idx[-1]])
                    print("type intervals[idx[-1]]", type(intervals[idx[-1]]))
                    print("idx[-1]", idx[-1])
                if strict:
                    matrix[idx] = get_strict_overlap(spam, intervals[idx[-1]])
                else:
                    matrix[idx] = get_overlap(spam, intervals[idx[-1]])
            else:
                raise Exception("David, I am afraid I have done a mistake. After all, I am just a computer.")

    if debug:
        print()
        print(foo)
        print()
        print(matrix)
    return matrix


def get_gap(range1, range2):
    """ Returns the gap of range1 and range2.

    :arg range1: (tuple or list): first interval
    :arg range2: (tuple or list): second interval
    :returns: (tuple): gap of range1 and range2
    """
    assert len(range1) == 2 or isinstance(range1, Interval)
    assert len(range2) == 2 or isinstance(range2, Interval)
    # if the range1 starts after range2 swap them
    if range2[0] < range1[0]:
        return get_gap(range2, range1)
    # if beginning of the range2 is inside of range1
    if range1[1] < range2[0]:
        return [range1[1], range2[0]]
    else:
        return False


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


def index_of_shortest_range(ranges):
    """ Return the index of the shortest interval from given list

    :arg ranges: (list): list of ranges
    """
    # TODO make tests
    shortest_index = -1
    shortest_range_len = sys.maxsize

    for index, range in enumerate(ranges):
        if range[1] - range[0] < shortest_range_len:
            shortest_index = index

    return shortest_index


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
