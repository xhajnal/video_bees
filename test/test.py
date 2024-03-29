import math
import unittest
import matplotlib.pyplot as plt

import analyse
from cross_traces import track_swapping_loop, \
    trim_out_additional_agents_over_long_traces_by_partition_with_build_fallback, \
    merge_alone_overlapping_traces_by_partition, merge_alone_overlapping_traces, merge_overlapping_traces_brutto
from dave_io import parse_traces
from single_trace import single_trace_checker, remove_full_traces
from trace import Trace
from primal_traces_logic import get_traces_from_range
from traces_logic import swap_two_overlapping_traces, merge_two_traces_with_gap, compute_whole_frame_range, \
    partition_frame_range_by_number_of_traces, reverse_partition_frame_range_by_number_of_traces, compare_two_traces, \
    compare_two_traces_with_shift, merge_multiple_pairs_of_overlapping_traces, check_to_merge_two_overlapping_traces, \
    order_traces
from misc import *
from visualise import scatter_detection


class MyTestCase(unittest.TestCase):
    # def test(self):
    #     pass
    #
    # def defTestscatterPlot(self):
    #     with open('../test/test.csv', newline='') as csv_file:
    #         print("hello")
    #         traces = parse_traces(csv_file)

    ## NO TRACE TESTS
    def test_misc(self):
        self.assertEqual(get_last_digit(5), 5)
        self.assertEqual(get_last_digit(61), 1)
        self.assertEqual(get_last_digit(848745), 5)

        self.assertEqual(calculate_cosine_similarity([1, 0], [0, 1]), 0)
        self.assertNotAlmostEqual(calculate_cosine_similarity([1, 0], [1, 1]), 0.707)
        self.assertEqual(calculate_cosine_similarity([1, 1], [1, 1]), 1)
        self.assertEqual(calculate_cosine_similarity([2, 2], [3, 3]), 1)

        self.assertEqual(to_vect([5], [3]), [-2])
        self.assertEqual(to_vect([8, 5], [7, 3]), [-1, -2])
        self.assertEqual(to_vect([5, 8, 5], [10, 7, 3]), [5, -1, -2])

        self.assertEqual(nice_range_print([605, 610]), "605-10")
        self.assertEqual(nice_range_print([605, 710]), "605 - 710")
        self.assertEqual(nice_range_print([605, 1710]), "605 - 1710")
        self.assertEqual(nice_range_print([605, 1610]), "605 - 1610")

        self.assertEqual(delete_indices([], [8, 9]), [8, 9])
        self.assertEqual(delete_indices([0], [8, 9]), [9])
        self.assertEqual(delete_indices([1], [8, 9]), [8])
        self.assertEqual(delete_indices([0, 1], [8, 9]), [])
        self.assertEqual(delete_indices([0, 1], [8, 9, 10]), [10])
        self.assertEqual(delete_indices([1], [8, 9, 10]), [8, 10])
        self.assertEqual(delete_indices([1, 1], [8, 9, 10]), [8, 10])


        self.assertEqual(take(0, [8, 9, 10]), [])
        self.assertEqual(take(1, [8, 9, 10]), [8])
        self.assertEqual(take(2, [8, 9, 10]), [8, 9])
        self.assertEqual(take(3, [8, 9, 10]), [8, 9, 10])

        self.assertEqual(flatten([]), [])
        self.assertEqual(flatten([8]), (8,))
        self.assertEqual(flatten((8, 7)), (8, 7))
        self.assertEqual(flatten(((8, 7))), (8, 7))
        self.assertEqual(flatten(((8, 7))), (8, 7))
        self.assertEqual(flatten(((8, (7)))), (8, 7))
        self.assertEqual(flatten(((8, (7, 9)))), (8, 7, 9))
        self.assertEqual(flatten(((8, 9, (7)))), (8, 9, 7))

        self.assertEqual(range_len((7, 7)), 0)
        self.assertEqual(range_len((7, 8)), 1)
        self.assertEqual(range_len((0, 10)), 10)
        self.assertEqual(range_len((1, 11)), 10)

        self.assertEqual(margin_range((7, 7), 0), (7, 7))
        self.assertEqual(margin_range((5, 6), 0), (5, 6))
        self.assertEqual(margin_range((5, 6), 1), (4, 7))
        self.assertEqual(margin_range((5, 6), 4), (1, 10))

        self.assertTrue(is_in([1, 7], [8, 9]) is False)
        self.assertTrue(is_in([1, 7], [7, 9]) is False)
        self.assertTrue(is_in([8, 9], [1, 7]) is False)
        self.assertTrue(is_in([7, 9], [1, 7]) is False)
        self.assertTrue(is_in([1, 7], [2, 6]) is False)
        self.assertTrue(is_in([4, 6], [3, 9]) is True)
        self.assertTrue(is_in([1, 7], [2, 7]) is False)
        self.assertTrue(is_in([3, 6], [3, 9]) is True)
        self.assertTrue(is_in([1, 7], [1, 7]) is True)

        self.assertTrue(has_overlap([1, 7], [8, 9]) is False)
        self.assertTrue(has_overlap([1, 7], [7, 9]) is True)
        self.assertTrue(has_overlap([8, 9], [1, 7]) is False)
        self.assertTrue(has_overlap([7, 9], [1, 7]) is True)
        self.assertTrue(has_overlap([1, 7], [2, 6]) is True)
        self.assertTrue(has_overlap([4, 6], [3, 9]) is True)
        self.assertTrue(has_overlap([1, 7], [2, 7]) is True)
        self.assertTrue(has_overlap([3, 6], [3, 9]) is True)
        self.assertTrue(has_overlap([1, 7], [1, 7]) is True)
        self.assertTrue(has_overlap([1620, 1625], [1620, 1620]) is True)

        self.assertTrue(has_strict_overlap([1, 7], [8, 9]) is False)
        self.assertTrue(has_strict_overlap([5, 6], [6, 10]) is False)
        self.assertTrue(has_strict_overlap([1, 7], [7, 9]) is False)
        self.assertTrue(has_strict_overlap([8, 9], [1, 7]) is False)
        self.assertTrue(has_strict_overlap([7, 9], [1, 7]) is False)
        self.assertTrue(has_strict_overlap([1, 7], [2, 6]) is True)
        self.assertTrue(has_strict_overlap([4, 6], [3, 9]) is True)
        self.assertTrue(has_strict_overlap([1, 7], [2, 7]) is True)
        self.assertTrue(has_strict_overlap([3, 6], [3, 9]) is True)
        self.assertTrue(has_strict_overlap([1, 7], [1, 7]) is True)
        self.assertTrue(has_strict_overlap([1620, 1625], [1620, 1620]) is False)

        self.assertTrue(get_overlap([1, 7], [8, 9]) is False)
        self.assertEqual(get_overlap([1, 7], [7, 9]), [7, 7])
        self.assertTrue(get_overlap([8, 9], [1, 7]) is False)
        self.assertEqual(get_overlap([7, 9], [1, 7]), [7, 7])
        self.assertEqual(get_overlap([1, 7], [2, 6]), [2, 6])
        self.assertEqual(get_overlap([4, 6], [3, 9]), [4, 6])
        self.assertEqual(get_overlap([1, 7], [2, 7]), [2, 7])
        self.assertEqual(get_overlap([3, 6], [3, 9]), [3, 6])
        self.assertEqual(get_overlap([1, 7], [1, 7]), [1, 7])

        self.assertEqual(get_gap([1, 7], [8, 9]), [7, 8])
        self.assertEqual(get_gap([1, 7], [7, 9]), [7, 7])
        self.assertEqual(get_gap([8, 9], [1, 7]), [7, 8])
        self.assertEqual(get_gap([7, 9], [1, 7]), [7, 7])
        self.assertEqual(get_gap([1, 7], [2, 6]), False)
        self.assertEqual(get_gap([4, 6], [3, 9]), False)
        self.assertEqual(get_gap([1, 7], [2, 7]), False)
        self.assertEqual(get_gap([3, 6], [3, 9]), False)
        self.assertEqual(get_gap([1, 7], [1, 7]), False)

        self.assertEqual(get_strict_gap([1, 7], [8, 9]), [7, 8])
        self.assertEqual(get_strict_gap([1, 7], [7, 9]), False)
        self.assertEqual(get_strict_gap([8, 9], [1, 7]), [7, 8])
        self.assertEqual(get_strict_gap([7, 9], [1, 7]), False)
        self.assertEqual(get_strict_gap([1, 7], [2, 6]), False)
        self.assertEqual(get_strict_gap([4, 6], [3, 9]), False)
        self.assertEqual(get_strict_gap([1, 7], [2, 7]), False)
        self.assertEqual(get_strict_gap([3, 6], [3, 9]), False)
        self.assertEqual(get_strict_gap([1, 7], [1, 7]), False)

        self.assertTrue(get_strict_overlap([1, 7], [8, 9]) is False)
        self.assertTrue(get_strict_overlap([1, 7], [7, 9]) is False)
        self.assertTrue(get_strict_overlap([8, 9], [1, 7]) is False)
        self.assertTrue(get_strict_overlap([7, 9], [1, 7]) is False)
        self.assertEqual(get_strict_overlap([1, 7], [2, 6]), [2, 6])
        self.assertEqual(get_strict_overlap([4, 6], [3, 9]), [4, 6])
        self.assertEqual(get_strict_overlap([1, 7], [2, 7]), [2, 7])
        self.assertEqual(get_strict_overlap([3, 6], [3, 9]), [3, 6])
        self.assertEqual(get_strict_overlap([1, 7], [1, 7]), [1, 7])

        self.assertTrue(is_before([1, 7], [8, 9]) is True)
        self.assertTrue(is_before([1, 7], [7, 9]) is False)
        self.assertTrue(is_before([8, 9], [1, 7]) is False)
        self.assertTrue(is_before([7, 9], [1, 7]) is False)
        self.assertTrue(is_before([1, 7], [2, 6]) is False)
        self.assertTrue(is_before([4, 6], [3, 9]) is False)
        self.assertTrue(is_before([1, 7], [2, 7]) is False)
        self.assertTrue(is_before([3, 6], [3, 9]) is False)
        self.assertTrue(is_before([1, 7], [1, 7]) is False)

        self.assertEqual(get_index_of_shortest_range([]), -1)
        self.assertEqual(get_index_of_shortest_range([(1, 1)]), 0)
        self.assertTrue(get_index_of_shortest_range([(1, 1), (2, 2)]) == (0, 1))
        self.assertEqual(get_index_of_shortest_range([(1, 1), (2, 3)]), 0)
        self.assertEqual(get_index_of_shortest_range([(1, 1), (2, 3), (2, 2)]), (0, 2))
        self.assertEqual(get_index_of_shortest_range([(1, 5), (2, 3), (2, 2)]), 2)

        self.assertEqual(merge_dictionary({8: 1}, {9: 9}), {8: 1, 9: 9})
        self.assertEqual(merge_dictionary({7: 1, 8: 1}, {9: 9}), {7: 1, 8: 1, 9: 9})
        self.assertEqual(merge_dictionary({7: 1, 8: 1}, {7: 9}), {7: 10, 8: 1})
        self.assertEqual(merge_dictionary({7: 1, 8: 1}, {8: 9}), {7: 1, 8: 10})

        # strictly further
        self.assertEqual(merge_sorted_dictionaries({(6, 7): 1}, {(8, 9): 6}), {(6, 7): 1, (8, 9): 6})
        self.assertEqual(merge_sorted_dictionaries({(8, 9): 6}, {(6, 7): 1}), {(6, 7): 1, (8, 9): 6})
        self.assertEqual(merge_sorted_dictionaries({(8, 9): 6, (6, 7): 1}, {}), {(6, 7): 1, (8, 9): 6})
        self.assertEqual(merge_sorted_dictionaries({}, {(8, 9): 6, (6, 7): 1}), {(6, 7): 1, (8, 9): 6})
        # more left
        self.assertEqual(merge_sorted_dictionaries({(8, 7): 1}, {(9, 7): 9}), {(8, 7): 1, (9, 7): 9})
        self.assertEqual(merge_sorted_dictionaries({(9, 7): 9}, {(8, 7): 1}), {(8, 7): 1, (9, 7): 9})
        self.assertEqual(merge_sorted_dictionaries({(9, 7): 9, (8, 7): 1}, {}), {(8, 7): 1, (9, 7): 9})
        # more up
        self.assertEqual(merge_sorted_dictionaries({(8, 7): 1}, {(8, 8): 9}), {(8, 7): 1, (8, 8): 9})
        self.assertEqual(merge_sorted_dictionaries({(8, 8): 9}, {(8, 7): 1}), {(8, 7): 1, (8, 8): 9})
        self.assertEqual(merge_sorted_dictionaries({(8, 8): 9, (8, 7): 1}, {}), {(8, 7): 1, (8, 8): 9})
        #
        self.assertEqual(merge_sorted_dictionaries({(8, 8): 9, (10, 11): 0}, {(8, 7): 1}), {(8, 7): 1, (8, 8): 9, (10, 11): 0})
        self.assertEqual(merge_sorted_dictionaries({(8, 8): 9, (10, 11): 0}, {(8, 7): 1, (15, 16): 7}), {(8, 7): 1, (8, 8): 9, (10, 11): 0, (15, 16): 7})

        self.assertEqual(get_leftmost_point([[0, 0]]), ([0, 0], 0))
        self.assertEqual(get_leftmost_point([[0, 0], [1, 2]]), ([0, 0], 0))
        self.assertEqual(get_leftmost_point([[0, 0], [1, 2], [4, 5]]), ([0, 0], 0))
        self.assertEqual(get_leftmost_point([[1, 2], [4, 5], [0, 0]]), ([0, 0], 2))
        self.assertEqual(get_leftmost_point([[0, 0], [1, 0]]), ([0, 0], 0))
        self.assertEqual(get_leftmost_point([[0, 0], [1, 0], [4, 0]]), ([0, 0], 0))
        self.assertEqual(get_leftmost_point([[1, 0], [4, 0], [0, 0]]), ([0, 0], 2))

        # m = 2
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [[41621, 41663], [41688, 41699]], strict=True), {})
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [[41621, 41663], [41688, 41699]]), {})

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [(6, 8), (9, 11), (7, 10)], strict=True), {(0, 2): [7, 8], (1, 2): [9, 10]})
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [(9, 11), (6, 8), (7, 10)], strict=True), {(1, 2): [7, 8], (0, 2): [9, 10]})

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [(6, 8), (7, 10), (9, 11)], strict=True), {(0, 1): [7, 8], (1, 2): [9, 10]})
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [(7, 10), (6, 8), (9, 11)], strict=True), {(0, 1): [7, 8], (0, 2): [9, 10]})

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [(6, 8), (9, 11), (7, 10)], strict=True, skip_whole_in=True), {(0, 2): [7, 8], (1, 2): [9, 10]})

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [(6, 8), (9, 10), (7, 10)], strict=True, skip_whole_in=True), {(0, 2): [7, 8]})

        self.assertTrue(np.array_equal(matrix_of_m_overlaps_of_n_intervals(2, [(6, 8), (9, 11), (7, 10)]),
                                       [[None, False, list([7, 8])],
                                        [0, None, list([9, 10])],
                                        [0, 0, None]]))
        self.assertEqual(m_overlaps_of_n_intervals(2, [(6, 8), (9, 11), (7, 10)]), {(0, 2): [7, 8], (1, 2): [9, 10]})
        self.assertEqual(m_overlaps_of_n_intervals(3, [(6, 8), (9, 11), (7, 10)]), {})

        # m = 3
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(3, [(6, 8), (9, 11), (7, 10)], strict=True), {})
        self.assertTrue(np.array_equal(matrix_of_m_overlaps_of_n_intervals(3, [(6, 8), (9, 11), (7, 10)]),
                                       [[[None, None, None], [9, None, False], [9, 9, None]],
                                        [[9, 9, 9], [9, None, None], [9, 9, None]],
                                        [[9, 9, 9], [9, 9, 9], [9, 9, None]]]))

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(3, [(6, 8), (9, 11), (7, 10)], strict=True), {})
        self.assertTrue(np.array_equal(matrix_of_m_overlaps_of_n_intervals(3, [(6, 10), (9, 11), (7, 10)]),
                                       [[[None, None, None], [9, None, list([9, 10])], [9, 9, None]],
                                        [[9, 9, 9], [9, None, None], [9, 9, None]],
                                        [[9, 9, 9], [9, 9, 9], [9, 9, None]]]))

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(3, [(6, 10), (9, 11), (7, 10)], strict=True), {(0, 1, 2): [9, 10]})
        self.assertEqual(m_overlaps_of_n_intervals(3, [(6, 10), (9, 11), (7, 10)]), {(0, 1, 2): [9, 10]})
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(3, [(5, 10), (9, 11), (6, 10), (3, 7)], strict=True),
                         {(0, 1, 2): [9, 10], (0, 2, 3): [6, 7]})
        self.assertEqual(m_overlaps_of_n_intervals(3, [(5, 10), (9, 11), (6, 10), (3, 7)]), {(0, 1, 2): [9, 10], (0, 2, 3): [6, 7]})

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(3, [(5, 10), (9, 11), (9, 11)], strict=True, skip_whole_in=True), {})


        # m = 4
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(4, [(5, 10), (9, 11), (6, 10), (3, 7)], strict=True), {})
        self.assertEqual(m_overlaps_of_n_intervals(4, [(5, 10), (9, 11), (6, 10), (3, 7)]), {})
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(4, [(5, 10), (6, 11), (6, 10), (3, 7)], strict=True), {(0, 1, 2, 3): [6, 7]})
        self.assertEqual(m_overlaps_of_n_intervals(4, [(5, 10), (6, 11), (6, 10), (3, 7)]), {(0, 1, 2, 3): [6, 7]})

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(4, [(5, 10), (6, 11), (6, 10), (3, 7), (5, 6)], strict=True, skip_whole_in=True),
                         {(0, 1, 2, 3): [6, 7]})
        self.assertEqual(m_overlaps_of_n_intervals(4, [(5, 10), (6, 11), (6, 10), (3, 7), (5, 6)], strict=True), {(0, 1, 2, 3): [6, 7]})

        # self.assertTrue(np.array_equal(get_submatrix(np.arange(10)*2, [1]), 2))
        # self.assertTrue(np.array_equal(get_submatrix(np.array([[1, 2, 3], [4, 5, 6]]), [1]), [4, 5, 6]))
        # self.assertTrue(np.array_equal(get_submatrix(np.array([[1, 2, 3], [4, 5, 6]]), [1, 2]), 6))
        # self.assertTrue(np.array_equal(get_submatrix(np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]), [1, 1]), [10, 11, 12]))

        self.assertEqual(convert_frame_number_back(1620, '../test/test_converted.csv'), 1621)

    ## SINGLE TRACE TESTS
    def testTraces(self):
        with open('../test/test.csv', newline='') as csv_file:
            traces = parse_traces(csv_file)
            traces_lengths = []
            for index, trace in enumerate(traces.keys()):
                traces_lengths.append(Trace(traces[trace], index))

            fig = plt.figure()
            ax1 = fig.add_subplot(111)

            for index, trace in enumerate(traces_lengths):
                x = trace.frames_list
                y = [index] * len(x)
                ax1.scatter(x, y, alpha=0.5)
            plt.show()

            print(traces[0])
            trace0 = Trace(traces[0], 0)
            print(trace0)
            self.assertEqual(trace0.trace_id, 0)
            self.assertEqual(trace0.frame_range, [1620, 1622])
            self.assertEqual(trace0.get_number_of_frames_tracked(), 3)
            self.assertEqual(trace0.frame_range_len, 3)
            self.assertAlmostEqual(trace0.trace_length, 4.242640687119286)
            self.assertAlmostEqual(trace0.max_step_len, 2.8284271247461903)
            self.assertEqual(trace0.max_step_len_step_index, 1)
            self.assertEqual(trace0.max_step_len_line, 3)
            self.assertEqual(trace0.max_step_len_frame_number, 1621)
            self.assertEqual(trace0.trace_lengths, {1.414214: 1, 2.828427: 1})
            self.assertEqual(trace0.frames_list, [1620, 1621, 1622])
            self.assertEqual(trace0.locations, [[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]])

            self.assertEqual(trace0.get_gap_frame_range(), ())
            self.assertEqual(trace0.get_gap_locations(), [])
            self.assertEqual(trace0.get_overlap_frame_range(), ())
            self.assertEqual(trace0.get_overlap_locations(), [])
            self.assertEqual(trace0.get_location_from_frame(1620), [0.0, 0.0])
            self.assertEqual(trace0.get_location_from_frame(1621), [1.0, 1.0])
            self.assertEqual(trace0.get_location_from_frame(1622), [3.0, 3.0])
            self.assertEqual(trace0.get_locations_from_frame_range((1620, 1622)), [[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]])
            self.assertEqual(trace0.get_number_of_frames_tracked(), 3)
            trace0.check_trace_consistency()
            self.assertEqual(trace0.check_whether_is_done([1620, 1635]), False)
            self.assertEqual(trace0.check_whether_is_done([1620, 1622]), True)
            trace0.recalculate_trace_lengths()
            self.assertAlmostEqual(trace0.trace_length, 4.242640687119286)
            self.assertEqual(trace0.trace_lengths, {1.414214: 1, 2.828427: 1})
            self.assertAlmostEqual(trace0.max_step_len, 2.8284271247461903)


            trace1 = Trace(traces[1], 1)
            self.assertEqual(trace1.trace_id, 1)
            self.assertEqual(trace1.frame_range, [1620, 1622])
            self.assertEqual(trace1.get_number_of_frames_tracked(), 3)
            self.assertEqual(trace1.frame_range_len, 3)
            self.assertAlmostEqual(trace1.trace_length, 7.6212327846342935)
            self.assertAlmostEqual(trace1.max_step_len, 5.385164807134505)
            self.assertEqual(trace1.max_step_len_step_index, 0)
            self.assertEqual(trace1.max_step_len_line, 1)
            self.assertEqual(trace1.max_step_len_frame_number, 1620)
            self.assertDictEqual(trace1.trace_lengths, {5.385165: 1, 2.236068: 1})
            self.assertEqual(trace1.frames_list, [1620, 1621, 1622])
            self.assertEqual(trace1.locations, [[0.0, 0.0], [2.0, 5.0], [3.0, 7.0]])

            self.assertEqual(trace1.get_gap_frame_range(), ())
            self.assertEqual(trace1.get_gap_locations(), [])
            self.assertEqual(trace1.get_overlap_frame_range(), ())
            self.assertEqual(trace1.get_overlap_locations(), [])
            self.assertEqual(trace1.get_location_from_frame(1620), [0.0, 0.0])
            self.assertEqual(trace1.get_location_from_frame(1621), [2.0, 5.0])
            self.assertEqual(trace1.get_location_from_frame(1622), [3.0, 7.0])
            self.assertEqual(trace1.get_locations_from_frame_range((1620, 1622)), [[0.0, 0.0], [2.0, 5.0], [3.0, 7.0]])
            self.assertEqual(trace1.get_number_of_frames_tracked(), 3)
            trace1.check_trace_consistency()
            self.assertEqual(trace1.check_whether_is_done([1620, 1635]), False)
            self.assertEqual(trace1.check_whether_is_done([1620, 1622]), True)
            trace1.recalculate_trace_lengths()
            self.assertAlmostEqual(trace1.trace_length, 7.6212327846342935)
            self.assertEqual(trace1.trace_lengths, {5.385165: 1, 2.236068: 1})
            self.assertAlmostEqual(trace1.max_step_len, 5.385164807134505)

            # print(trace0.frames_tracked)

            trace0.show_step_lengths_hist()
            trace1.show_step_lengths_hist()

            trace0 = Trace(traces[0], 0)
            trace3 = Trace(traces[3], 3)
            self.assertTrue(np.array_equal(trace0.locations, [[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]]))
            self.assertTrue(np.array_equal(trace3.locations, [[0.0, 0.0], [2.0, 5.0], [3.0, 7.0]]))
            # print(trace0)
            # print(trace3)
            #
            # print(trace0.frame_range)
            # print(trace3.frame_range)

            merged_trace = merge_two_traces_with_gap(copy(trace0), copy(trace3))
            self.assertEqual(merged_trace.trace_id, 0)
            self.assertIsInstance(merged_trace, Trace)
            self.assertEqual(merged_trace.frame_range, [1620, 1625])
            self.assertEqual(merged_trace.gap_frames, [])
            self.assertEqual(merged_trace.get_number_of_frames_tracked(), 6)
            self.assertEqual(merged_trace.frame_range_len, 6)
            self.assertAlmostEqual(merged_trace.trace_length, 4.242640687119286 + 7.6212327846342935 + 4.24264068711928514)
            self.assertAlmostEqual(merged_trace.max_step_len, 5.3851648071)
            self.assertEqual(merged_trace.max_step_len_step_index, 0)
            self.assertEqual(merged_trace.max_step_len_line, 7)
            self.assertEqual(merged_trace.max_step_len_frame_number, 1623)
            # trace3.trace_lengths: {1.414214: 1, 2.828427: 1}
            # trace3.trace_lengths: {5.385165: 1, 2.236068: 1}
            # merge step: math.dist([3,3], [0,0])== 4.242640687119285
            self.assertDictEqual(merged_trace.trace_lengths, {1.414214: 1, 2.828427: 1, 5.385165: 1, 2.236068: 1, 4.242641: 1})
            self.assertEqual(merged_trace.frames_list, [1620, 1621, 1622, 1623, 1624, 1625])
            self.assertTrue(np.array_equal(merged_trace.locations, [[0.0, 0.0], [1.0, 1.0], [3.0, 3.0], [0.0, 0.0], [2.0, 5.0], [3.0, 7.0]]))

            self.assertEqual(merged_trace.get_gap_frame_range(), ())
            self.assertEqual(merged_trace.get_gap_locations(), [])
            self.assertEqual(merged_trace.get_overlap_frame_range(), ())
            self.assertEqual(merged_trace.get_overlap_locations(), [])
            self.assertEqual(merged_trace.get_location_from_frame(1620), [0.0, 0.0])
            self.assertEqual(merged_trace.get_location_from_frame(1621), [1.0, 1.0])
            self.assertEqual(merged_trace.get_location_from_frame(1622), [3.0, 3.0])
            self.assertEqual(merged_trace.get_locations_from_frame_range((1620, 1623)), [[0.0, 0.0], [1.0, 1.0], [3.0, 3.0], [0.0, 0.0]])
            self.assertEqual(merged_trace.get_number_of_frames_tracked(), 6)
            merged_trace.check_trace_consistency()
            self.assertEqual(merged_trace.check_whether_is_done([1620, 1635]), False)
            self.assertEqual(merged_trace.check_whether_is_done([1620, 1625]), True)
            merged_trace.recalculate_trace_lengths()
            self.assertAlmostEqual(merged_trace.trace_length, 4.242640687119286 + 7.6212327846342935 + 4.24264068711928514)
            self.assertEqual(merged_trace.trace_lengths, {1.414214: 1, 2.828427: 1, 5.385165: 1, 2.236068: 1, 4.242641: 1})
            self.assertAlmostEqual(merged_trace.max_step_len, 5.385164807134505)


            trace0 = Trace(traces[0], 0)
            trace4 = Trace(traces[4], 4)

            merged_trace = merge_two_traces_with_gap(trace4, trace0)
            self.assertEqual(merged_trace.trace_id, 0)
            self.assertIsInstance(merged_trace, Trace)
            self.assertEqual(merged_trace.frame_range, [1620, 1635])
            self.assertEqual(merged_trace.get_number_of_frames_tracked(), 6)
            self.assertEqual(merged_trace.frame_range_len, 16)
            self.assertAlmostEqual(merged_trace.trace_length, 4.242640687119286 + 7.6212327846342935 + 4.24264068711928514)
            self.assertAlmostEqual(merged_trace.max_step_len, 5.3851648071)
            self.assertEqual(merged_trace.max_step_len_step_index, 0)
            self.assertEqual(merged_trace.max_step_len_line, 10)
            self.assertEqual(merged_trace.max_step_len_frame_number, 1633)
            # trace3.trace_lengths: {1.414214: 1, 2.828427: 1}
            # trace3.trace_lengths: {5.385165: 1, 2.236068: 1}
            # merge step: math.dist([3,3], [0,0])== 4.242640687119285
            self.assertDictEqual(merged_trace.trace_lengths,
                                 {1.414214: 1, 2.828427: 1, 5.385165: 1, 2.236068: 1, 4.242641: 1})
            self.assertEqual(merged_trace.frames_list, [1620, 1621, 1622, 1623, 1624, 1625, 1626, 1627, 1628, 1629, 1630, 1631, 1632, 1633, 1634, 1635])
            # DEPRECATED
            # self.assertEqual(merged_trace.locations,
            #                  [[0.0, 0.0], [1.0, 1.0], [3.0, 3.0], [1.5, 1.5], [1.5, 1.5], [1.5, 1.5], [1.5, 1.5], [1.5, 1.5], [1.5, 1.5], [1.5, 1.5], [1.5, 1.5], [1.5, 1.5], [1.5, 1.5], [0.0, 0.0], [2.0, 5.0], [3.0, 7.0]])
            self.assertEqual(merged_trace.locations, [[0.0, 0.0], [1.0, 1.0], [3.0, 3.0], [2.7272727272727275, 2.7272727272727275], [2.4545454545454546, 2.4545454545454546], [2.1818181818181817, 2.1818181818181817], [1.9090909090909092, 1.9090909090909092], [1.6363636363636365, 1.6363636363636365], [1.3636363636363638, 1.3636363636363638], [1.090909090909091, 1.090909090909091], [0.8181818181818183, 0.8181818181818183], [0.5454545454545459, 0.5454545454545459], [0.27272727272727293, 0.27272727272727293], [0.0, 0.0], [2.0, 5.0], [3.0, 7.0]])

            self.assertEqual(merged_trace.get_gap_frame_range(), (1623, 1632))
            self.assertEqual(len(merged_trace.get_gap_locations()), 10)
            self.assertEqual(merged_trace.get_overlap_frame_range(), ())
            self.assertEqual(merged_trace.get_overlap_locations(), [])
            self.assertEqual(merged_trace.get_location_from_frame(1620), [0.0, 0.0])
            self.assertEqual(merged_trace.get_location_from_frame(1621), [1.0, 1.0])
            self.assertEqual(merged_trace.get_location_from_frame(1622), [3.0, 3.0])
            # self.assertEqual(merged_trace.get_locations_from_frame_range((1620, 1623)),
            #                  [[0.0, 0.0], [1.0, 1.0], [3.0, 3.0], [0.0, 0.0]])
            self.assertEqual(merged_trace.get_number_of_frames_tracked(), 6)
            merged_trace.check_trace_consistency()
            self.assertEqual(merged_trace.check_whether_is_done([1620, 1641]), False)
            self.assertEqual(merged_trace.check_whether_is_done([1620, 1635]), True)
            merged_trace.recalculate_trace_lengths()
            self.assertAlmostEqual(merged_trace.trace_length,
                                   4.242640687119286 + 7.6212327846342935 + 4.24264068711928514)
            self.assertEqual(len(merged_trace.trace_lengths), merged_trace.frame_range_len - len(merged_trace.gap_frames) - 1)
            self.assertAlmostEqual(merged_trace.max_step_len, 5.385164807134505)


            trace0 = Trace(traces[0], 0)
            trace5 = Trace(traces[5], 5)
            merged_trace = merge_two_traces_with_gap(trace5, trace0)
            spam = [[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]]
            spam.extend([[-1, -1]] * 502)
            spam.extend([[0.0, 0.0], [2.0, 5.0], [3.0, 7.0]])
            self.assertEqual(merged_trace.locations, spam)

    def testRemoveFullTraces(self):
        with open('../test/test.csv', newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
            traces = []
            for index, trace in enumerate(scraped_traces.keys()):
                # print(trace)
                # print(scraped_traces[trace])
                traces.append(Trace(scraped_traces[trace], index))

            self.assertEqual(compute_whole_frame_range(traces), [1620, 2127])

            removed_traces = []
            population_size = 8
            remove_full_traces(traces, removed_traces, population_size, silent=False, debug=False)
            self.assertEqual(len(traces), 8)
            self.assertEqual(len(removed_traces), 0)

        with open('../test/test2.csv', newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
            traces = []
            for index, trace in enumerate(scraped_traces.keys()):
                # print(trace)
                # print(scraped_traces[trace])
                traces.append(Trace(scraped_traces[trace], index))

            self.assertEqual(compute_whole_frame_range(traces), [1620, 1625])

            removed_traces = []
            population_size = 4
            remove_full_traces(traces, removed_traces, population_size, silent=False, debug=False)
            self.assertEqual(len(traces), 2)
            self.assertEqual(traces[0].trace_id, 2)
            self.assertEqual(traces[1].trace_id, 3)
            self.assertEqual(len(removed_traces), 2)

            self.assertEqual(removed_traces[0].trace_id, 0)
            self.assertEqual(removed_traces[1].trace_id, 1)

    ## TRACES LOGIC TESTS
    def test_order_traces(self):
        with open('../test/test.csv', newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
            traces = []
            for index, trace in enumerate(scraped_traces.keys()):
                traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(traces, [traces[0], traces[1], traces[2], traces[3], traces[4], traces[5], traces[6], traces[7]])
        spam = order_traces(traces, [traces[1], traces[2]])
        self.assertEqual(spam, [traces[1], traces[2], traces[0], traces[3], traces[4], traces[5], traces[6], traces[7]])

        spam = order_traces(traces, [traces[1], traces[2]], selected_range=(1620, 1622))
        self.assertEqual(spam, [traces[1], traces[2], traces[0], traces[6], traces[7]])


    def test_dictionary_of_m_overlaps_of_n_intervals(self):
        with open('../test/test.csv', newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        spam = dictionary_of_m_overlaps_of_n_intervals(2, list(map(lambda x: x.frame_range, traces)), strict=True, skip_whole_in=True)
        print(spam)

    def test_merge_multiple_traces(self):
        ## RAISE EXCEPTION
        with open('../test/test3.csv', newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 10)
        with self.assertRaises(Exception) as context:
            merge_multiple_pairs_of_overlapping_traces(traces, [(1, 7)], silent=False, debug=True)
        self.assertEqual(len(traces), 10)

        ## NO MERGE
        with open('../test/test3.csv', newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 10)
        merge_multiple_pairs_of_overlapping_traces(traces, [], silent=False, debug=True)
        self.assertEqual(len(traces), 10)

        ## 2 MERGES
        with open('../test/test3.csv', newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 10)
        merge_multiple_pairs_of_overlapping_traces(traces, [(1, 2), (2, 3)], silent=False, debug=True)
        self.assertEqual(len(traces), 8)
        self.assertEqual(list(map(lambda x: x.trace_id, traces)), [0, 1, 4, 5, 6, 7, 8, 9])


        with open('../test/test3.csv', newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 10)
        merge_multiple_pairs_of_overlapping_traces(traces, [(2, 3), (1, 2)], silent=False, debug=True)
        self.assertEqual(len(traces), 8)
        self.assertEqual(list(map(lambda x: x.trace_id, traces)), [0, 1, 4, 5, 6, 7, 8, 9])


        ## 6 MERGES
        with open('../test/test3_some_distant_traces.csv', newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 10)
        merge_multiple_pairs_of_overlapping_traces(traces, [(2, 3), (1, 2), (5, 6), (8, 9)], silent=False, debug=True)
        self.assertEqual(len(traces), 6)
        self.assertEqual(list(map(lambda x: x.trace_id, traces)), [0, 1, 4, 5, 7, 8])

    def testCompareTraces(self):
        ## NO PAIR
        with open('../test/test_b.csv', newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        distances = compare_two_traces(traces[0], traces[2], 0, 2, allow_inside=True, silent=False, debug=False, show_all_plots=None)
        self.assertAlmostEqual(distances, [0])

        distances = compare_two_traces(traces[0], traces[7], 0, 7, allow_inside=True, silent=False, debug=False, show_all_plots=None)
        self.assertAlmostEqual(distances, [0.0, 4.123105625617661, 4.0])

        distances, spam, shift = compare_two_traces_with_shift(traces[0], traces[2], 0, 2, allow_inside=True, silent=False, debug=False, show_all_plots=None)
        self.assertAlmostEqual(distances, [0])
        self.assertAlmostEqual(spam, [0])
        self.assertAlmostEqual(shift, 0)

        distances, spam, shift = compare_two_traces_with_shift(traces[0], traces[8], 0, 8, allow_inside=True, silent=False, debug=False, show_all_plots=None)
        self.assertAlmostEqual(distances, [4.123105625617661, 4.0])
        self.assertAlmostEqual(spam, [4.123105625617661, 4.0])
        self.assertAlmostEqual(shift, 0)

        with open('../test/test3_some_distant_traces.csv', newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        distances = compare_two_traces(traces[4], traces[5], 4, 5, allow_inside=True, silent=False, debug=False, show_all_plots=None)

        self.assertAlmostEqual(distances, [800, 761])

        distances, spam, shift = compare_two_traces_with_shift(traces[4], traces[5], 4, 5, allow_inside=True, silent=False, debug=False, show_all_plots=None)
        print("spam", spam)
        self.assertAlmostEqual(distances, [800, 761])
        self.assertAlmostEqual(spam, [800, 761])
        self.assertAlmostEqual(shift, 0)

    def testIntervalToCounts(self):
        with open('../test/test3.csv', newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        spam = partition_frame_range_by_number_of_traces(traces)
        self.assertEqual(spam, {(0, 1): 1, (1, 2): 2, (2, 3): 3, (3, 4): 2, (4, 5): 1, (5, 6): 2, (6, 7): 1, (7, 8): 2, (8, 9): 2, (9, 10): 3, (10, 11): 3, (11, 12): 2, (12, 13): 3, (13, 14): 2, (14, 15): 1})
        reverse_partition_frame_range_by_number_of_traces(spam)

        # print(list(map(str, get_traces_from_range(traces, [0, 2]))))
        # spam = get_traces_from_range(traces, [0, 2], are_inside=False)
        # for item in spam:
        #     print(str(item))

        self.assertEqual(get_traces_from_range(traces, [0, 2], fully_inside=True)[0], [traces[0]])
        self.assertEqual(get_traces_from_range(traces, [0, 2], fully_inside=False)[0], [traces[0], traces[1]])
        self.assertEqual(get_traces_from_range(traces, [0, 2], fully_inside=False, strict=False)[0], [traces[0], traces[1], traces[2], traces[3]])

        self.assertEqual(get_traces_from_range(traces, [5, 8], fully_inside=True)[0], [traces[4]])
        self.assertEqual(get_traces_from_range(traces, [5, 8], fully_inside=False)[0], [traces[3], traces[4], traces[5]])
        self.assertEqual(get_traces_from_range(traces, [5, 8], fully_inside=False, strict=False)[0], [traces[3], traces[4], traces[5], traces[6]])

        self.assertEqual(get_traces_from_range(traces, [0, 2], fully_inside=True)[1], [0])
        self.assertEqual(get_traces_from_range(traces, [0, 2], fully_inside=False)[1], [0, 1])
        self.assertEqual(get_traces_from_range(traces, [0, 2], fully_inside=False, strict=False)[1], [0, 1, 2, 3])

        self.assertEqual(get_traces_from_range(traces, [5, 8], fully_inside=True)[1], [4])
        self.assertEqual(get_traces_from_range(traces, [5, 8], fully_inside=False)[1], [3, 4, 5])
        self.assertEqual(get_traces_from_range(traces, [5, 8], fully_inside=False, strict=False)[1], [3, 4, 5, 6])

        with open('../test/test3_1.csv', newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(partition_frame_range_by_number_of_traces(traces), {(0, 1): 0, (1, 2): 2, (2, 3): 3, (3, 4): 2, (4, 5): 1, (5, 6): 2, (6, 7): 1, (7, 8): 2, (8, 9): 2, (9, 10): 3, (10, 11): 3, (11, 12): 2, (12, 13): 3, (13, 14): 2, (14, 15): 1})

    ## MULTIPLE TRACES TESTS
    def test_check_to_merge_two_overlapping_traces(self):
        with open('../test/test3.csv', newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        ## MERGES
        self.assertEqual(check_to_merge_two_overlapping_traces(traces, traces[0], traces[1], 0, 1, [1, 2],
                                                               shift=False, guided=False, silent=False, debug=True), (True, None))
        ## No MERGES, inside one another
        self.assertEqual(check_to_merge_two_overlapping_traces(traces, traces[2], traces[3], 2, 3, [2, 4],
                                                               shift=False, guided=False, silent=False, debug=False), (None, None))

        ## Exception, premise not holding - not overlapping traces
        with self.assertRaises(Exception) as context:
            check_to_merge_two_overlapping_traces(traces, traces[2], traces[9], 2, 9, [2, 4], shift=False, guided=False,
                                                  silent=False, debug=False)

        ## No MERGES, too far
        with open('../test/test3_some_distant_traces.csv', newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(check_to_merge_two_overlapping_traces(traces, traces[0], traces[1], 0, 1, [1, 2],
                                                               shift=False, guided=False, silent=False, debug=False), (False, None))

    def testTrimOut(self):
        csv_file_path = '../test/test2.csv'
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        traces, spam, ids_of_traces_to_be_deleted = merge_alone_overlapping_traces(traces, None, 1, silent=True, debug=False)
        self.assertEqual(len(traces), 2)
        self.assertEqual(ids_of_traces_to_be_deleted, [2, 3])


        csv_file_path = '../test/test2.csv'
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))
        traces, ids_of_traces_to_be_deleted = merge_alone_overlapping_traces_by_partition(traces, silent=True, debug=False)
        self.assertEqual(len(traces), 2)
        self.assertEqual(ids_of_traces_to_be_deleted, [2, 3])


        csv_file_path= '../test/test2.csv'
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))
        traces, ids_of_traces_to_be_deleted = trim_out_additional_agents_over_long_traces_by_partition_with_build_fallback(traces, population_size=1,
                                                                                                                           silent=False, debug=True)
        self.assertEqual(len(traces), 2)
        self.assertEqual(ids_of_traces_to_be_deleted, [2, 3])

    def testAloneOverlap_by_partition(self):
        ## NO PAIR
        csv_file_path = '../test/test.csv'
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 8)
        merge_alone_overlapping_traces_by_partition(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 8)

        ## NO OVERLAP
        csv_file_path = '../test/test_4overlap.csv'
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 4)
        merge_alone_overlapping_traces_by_partition(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 4)
        self.assertEqual(list(map(lambda x: x.trace_id, traces)), [0, 1, 2, 3])

        ## NO OVERLAP
        csv_file_path = '../test/test_4overlap_in_single_frame.csv'
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 4)
        merge_alone_overlapping_traces_by_partition(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 4)
        self.assertEqual(list(map(lambda x: x.trace_id, traces)), [0, 1, 2, 3])

        ## NO MERGE
        with open('../test/test2.csv', newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 4)
        merge_alone_overlapping_traces_by_partition(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 4)

        ## 6/6 MERGES
        csv_file_path = '../test/test3.csv'
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        analyse.set_curr_csv_file_path(csv_file_path)
        self.assertEqual(len(traces), 10)
        merge_alone_overlapping_traces_by_partition(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 4)
        self.assertEqual(list(map(lambda x: x.trace_id, traces)), [0, 2, 3, 7])

        ## 3/6 MERGES
        csv_file_path = '../test/test3_some_distant_traces.csv'
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 10)
        merge_alone_overlapping_traces_by_partition(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 7)
        self.assertEqual(list(map(lambda x: x.trace_id, traces)), [0, 1, 2, 3, 5, 6, 7])


    def testAloneOverlap_by_build(self):
        ## NO PAIR
        csv_file_path = '../test/test.csv'
        analyse.set_curr_csv_file_path(csv_file_path)
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 8)
        merge_alone_overlapping_traces(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 8)

        ## NO OVERLAP
        csv_file_path = '../test/test_4overlap.csv'
        analyse.set_curr_csv_file_path(csv_file_path)
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 4)
        merge_alone_overlapping_traces(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 4)
        self.assertEqual(list(map(lambda x: x.trace_id, traces)), [0, 1, 2, 3])

        ## NO OVERLAP
        csv_file_path = '../test/test_4overlap_in_single_frame.csv'
        analyse.set_curr_csv_file_path(csv_file_path)
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 4)
        merge_alone_overlapping_traces(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 4)
        self.assertEqual(list(map(lambda x: x.trace_id, traces)), [0, 1, 2, 3])

        ## NO MERGE
        csv_file_path = '../test/test2.csv'
        analyse.set_curr_csv_file_path(csv_file_path)
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 4)
        merge_alone_overlapping_traces(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 4)

        ## 6/6 MERGES
        csv_file_path = '../test/test3.csv'
        analyse.set_curr_csv_file_path(csv_file_path)
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 10)
        merge_alone_overlapping_traces(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 5)
        self.assertEqual(list(map(lambda x: x.trace_id, traces)), [0, 6, 7, 8, 9])

        ## 3/6 MERGES
        csv_file_path = '../test/test3_some_distant_traces.csv'
        analyse.set_curr_csv_file_path(csv_file_path)
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 10)
        merge_alone_overlapping_traces(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 9)
        self.assertEqual(list(map(lambda x: x.trace_id, traces)), [0, 1, 2, 3, 5, 6, 7, 8, 9])

    def testOverlap_by_build(self):
        # NO PAIR
        csv_file_path = '../test/test.csv'
        analyse.set_curr_csv_file_path(csv_file_path)
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 8)
        merge_overlapping_traces_brutto(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 8)

        ## NO OVERLAP
        csv_file_path = '../test/test_4overlap.csv'
        analyse.set_curr_csv_file_path(csv_file_path)
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 4)
        merge_overlapping_traces_brutto(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 4)
        self.assertEqual(list(map(lambda x: x.trace_id, traces)), [0, 1, 2, 3])

        ## NO OVERLAP
        csv_file_path = '../test/test_4overlap_in_single_frame.csv'
        analyse.set_curr_csv_file_path(csv_file_path)
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 4)
        merge_overlapping_traces_brutto(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 4)
        self.assertEqual(list(map(lambda x: x.trace_id, traces)), [0, 1, 2, 3])

        ## NO MERGE
        csv_file_path = '../test/test2.csv'
        analyse.set_curr_csv_file_path(csv_file_path)
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 4)
        merge_overlapping_traces_brutto(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 4)

        ## 6/6 MERGES
        csv_file_path = '../test/test3.csv'
        analyse.set_curr_csv_file_path(csv_file_path)
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 10)
        merge_overlapping_traces_brutto(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 7)
        self.assertEqual(list(map(lambda x: x.trace_id, traces)), [0, 2, 3, 6, 7, 8, 9])

        ## 3/6 MERGES
        csv_file_path = '../test/test3_some_distant_traces.csv'
        analyse.set_curr_csv_file_path(csv_file_path)
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))

        self.assertEqual(len(traces), 10)
        merge_overlapping_traces_brutto(traces, silent=False, debug=True)
        self.assertEqual(len(traces), 9)
        self.assertEqual(list(map(lambda x: x.trace_id, traces)), [0, 1, 2, 3, 5, 6, 7, 8, 9])

    def testCheckTraces(self):
        csv_file_path = '../test/test.csv'
        analyse.set_curr_csv_file_path(csv_file_path)
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
            traces = []
            for index, trace in enumerate(scraped_traces.keys()):
                # print(trace)
                # print(scraped_traces[trace])
                traces.append(Trace(scraped_traces[trace], index))
            scatter_detection(traces, [1620, 2127])
            # single_trace_checker(traces, min_range_len=2)
            # scatter_detection(traces, [1620, 2127])
            single_trace_checker(traces, min_trace_range_len=4, vicinity=6)
            # scatter_detection(traces, [1620, 2127])
            scatter_detection(traces, [1620, 1626])

    # TODO HAVE A LOOK HERE
    def testSwaps(self):
        csv_file_path = '../test/test2.csv'
        analyse.set_curr_csv_file_path(csv_file_path)
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
            traces = []
            for index, trace in enumerate(scraped_traces.keys()):
                # print(trace)
                # print(scraped_traces[trace])
                traces.append(Trace(scraped_traces[trace], index))

            a = track_swapping_loop(traces, silent=False, debug=True)
            print(a)
            #
            # self.assertEqual(len(traces), 2)
            # self.assertEqual(traces[0].trace_id, 2)
            # self.assertEqual(traces[1].trace_id, 3)
            # self.assertEqual(len(removed_traces), 2)
            #
            # self.assertEqual(removed_traces[0].trace_id, 0)
            # self.assertEqual(removed_traces[1].trace_id, 1)

    def testSwapTraces(self):
        csv_file_path = '../test/test.csv'
        analyse.set_curr_csv_file_path(csv_file_path)
        with open(csv_file_path, newline='') as csv_file:
            traces = parse_traces(csv_file)
            traces_lengths = []
            for index, trace in enumerate(traces.keys()):
                traces_lengths.append(Trace(traces[trace], index))

            # test swap_two_overlapping_traces
            trace0 = Trace(traces[6], 0)
            trace1 = Trace(traces[7], 1)

            swap_two_overlapping_traces(trace0, trace1, 1621, debug=True)

            self.assertEqual(trace0.trace_id, 0)
            self.assertEqual(trace0.frame_range, [1620, 1623])
            self.assertEqual(trace0.gap_frames, [])
            self.assertEqual(trace0.overlap_frames, [])
            self.assertEqual(trace0.frames_list, [1620, 1621, 1622, 1623])
            self.assertEqual(trace0.get_number_of_frames_tracked(), 4)
            self.assertEqual(trace0.frame_range_len, 3)
            self.assertEqual(trace0.locations, [[0.0, 0.0], [2.0, 5.0], [3.0, 7.0], [3.0, 4.0]])
            self.assertAlmostEqual(trace0.trace_length, sum([math.dist([0.0, 0.0], [2.0, 5.0]), math.dist([2.0, 5.0], [3.0, 7.0]), math.dist([3.0, 7.0], [3.0, 4.0])]))
            # 5.385164807134504, 2.23606797749979, 3.0
            self.assertAlmostEqual(trace0.max_step_len, max([math.dist([0.0, 0.0], [2.0, 5.0]), math.dist([2.0, 5.0], [3.0, 7.0]), math.dist([3.0, 7.0], [3.0, 4.0])]))
            self.assertEqual(trace0.max_step_len_step_index, 0)
            self.assertEqual(trace0.max_step_len_line, None)
            self.assertEqual(trace0.max_step_len_frame_number, 1620)
            self.assertEqual(trace0.trace_lengths, {5.385165: 1, 2.236068: 1, 3:1})


            self.assertEqual(trace1.trace_id, 1)
            self.assertEqual(trace1.frame_range, [1620, 1622])
            self.assertEqual(trace1.gap_frames, [])
            self.assertEqual(trace1.overlap_frames, [])
            self.assertEqual(trace1.frames_list, [1620, 1621, 1622])
            self.assertEqual(trace1.get_number_of_frames_tracked(), 3)
            self.assertEqual(trace1.frame_range_len, 2)
            self.assertEqual(trace1.locations, [[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]])
            self.assertAlmostEqual(trace1.trace_length, sum([math.dist([0.0, 0.0], [1.0, 1.0]), math.dist([1.0, 1.0], [3.0, 3.0])]))
            self.assertAlmostEqual(trace1.max_step_len, max([math.dist([0.0, 0.0], [1.0, 1.0]), math.dist([1.0, 1.0], [3.0, 3.0])]))
            self.assertEqual(trace1.max_step_len_step_index, 1)
            self.assertEqual(trace1.max_step_len_line, None)
            self.assertEqual(trace1.max_step_len_frame_number, 1621)
            self.assertDictEqual(trace1.trace_lengths, {1.414214: 1, 2.828427: 1})

            # test 2 of swap_two_overlapping_traces
            trace0 = Trace(traces[6], 0)
            trace1 = Trace(traces[7], 1)

            swap_two_overlapping_traces(trace0, trace1, 1622, debug=True)

            self.assertEqual(trace0.trace_id, 0)
            self.assertEqual(trace0.frame_range, [1620, 1623])
            self.assertEqual(trace0.gap_frames, [])
            self.assertEqual(trace0.overlap_frames, [])
            self.assertEqual(trace0.frames_list, [1620, 1621, 1622, 1623])
            self.assertEqual(trace0.get_number_of_frames_tracked(), 4)
            self.assertEqual(trace0.frame_range_len, 3)
            self.assertEqual(trace0.locations, [[0.0, 0.0], [1.0, 1.0], [3.0, 7.0], [3.0, 4.0]])
            self.assertAlmostEqual(trace0.trace_length,
                                   sum([math.dist([0.0, 0.0], [1.0, 1.0]), math.dist([1.0, 1.0], [3.0, 7.0]),
                                        math.dist([3.0, 7.0], [3.0, 4.0])]))
            # [1.4142135623730951, 6.324555320336759, 3.0]
            self.assertAlmostEqual(trace0.max_step_len,
                                   max([math.dist([0.0, 0.0], [1.0, 1.0]), math.dist([1.0, 1.0], [3.0, 7.0]),
                                        math.dist([3.0, 7.0], [3.0, 4.0])]))
            self.assertEqual(trace0.max_step_len_step_index, 1)
            self.assertEqual(trace0.max_step_len_line, None)
            self.assertEqual(trace0.max_step_len_frame_number, 1621)
            self.assertEqual(trace0.trace_lengths, {1.414214: 1, 6.324555: 1, 3: 1})

            self.assertEqual(trace1.trace_id, 1)
            self.assertEqual(trace1.frame_range, [1620, 1622])
            self.assertEqual(trace1.gap_frames, [])
            self.assertEqual(trace1.overlap_frames, [])
            self.assertEqual(trace1.frames_list, [1620, 1621, 1622])
            self.assertEqual(trace1.get_number_of_frames_tracked(), 3)
            self.assertEqual(trace1.frame_range_len, 2)
            self.assertEqual(trace1.locations, [[0.0, 0.0], [2.0, 5.0], [3.0, 3.0]])
            self.assertAlmostEqual(trace1.trace_length,
                                   sum([math.dist([0.0, 0.0], [2.0, 5.0]), math.dist([2.0, 5.0], [3.0, 3.0])]))
            self.assertAlmostEqual(trace1.max_step_len,
                                   max([math.dist([0.0, 0.0], [2.0, 5.0]), math.dist([2.0, 5.0], [3.0, 3.0])]))
            # [5.385164807134504, 2.23606797749979]
            self.assertEqual(trace1.max_step_len_step_index, 0)
            self.assertEqual(trace1.max_step_len_line, 17)
            self.assertEqual(trace1.max_step_len_frame_number, 1620)
            self.assertDictEqual(trace1.trace_lengths, {5.385165: 1, 2.236068: 1})


if __name__ == '__main__':
    unittest.main()
