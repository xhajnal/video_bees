import math

from src.parse import parse_traces
from trace import merge_two_traces_with_gap, Trace
from traces_logic import swap_two_overlapping_traces
import unittest
import matplotlib.pyplot as plt
from misc import *


class MyTestCase(unittest.TestCase):
    # def test(self):
    #     pass
    #
    # def defTestscatterPlot(self):
    #     with open('../test/test.csv', newline='') as csv_file:
    #         print("hello")
    #         traces = parse_traces(csv_file)
    def test_misc(self):
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

        self.assertEqual(take(0, [8, 9, 10]), [])
        self.assertEqual(take(1, [8, 9, 10]), [8])
        self.assertEqual(take(2, [8, 9, 10]), [8, 9])
        self.assertEqual(take(3, [8, 9, 10]), [8, 9, 10])

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
        self.assertTrue(has_overlap([1, 7], [7, 9]) is False)
        self.assertTrue(has_overlap([8, 9], [1, 7]) is False)
        self.assertTrue(has_overlap([7, 9], [1, 7]) is False)
        self.assertTrue(has_overlap([1, 7], [2, 6]) is True)
        self.assertTrue(has_overlap([4, 6], [3, 9]) is True)
        self.assertTrue(has_overlap([1, 7], [2, 7]) is True)
        self.assertTrue(has_overlap([3, 6], [3, 9]) is True)
        self.assertTrue(has_overlap([1, 7], [1, 7]) is True)

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
        self.assertEqual(get_gap([1, 7], [7, 9]), False)
        self.assertEqual(get_gap([8, 9], [1, 7]), [7, 8])
        self.assertEqual(get_gap([7, 9], [1, 7]), False)
        self.assertEqual(get_gap([1, 7], [2, 6]), False)
        self.assertEqual(get_gap([4, 6], [3, 9]), False)
        self.assertEqual(get_gap([1, 7], [2, 7]), False)
        self.assertEqual(get_gap([3, 6], [3, 9]), False)
        self.assertEqual(get_gap([1, 7], [1, 7]), False)

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

        self.assertEqual(merge_dictionary({8: 1}, {9: 9}), {8: 1, 9: 9})
        self.assertEqual(merge_dictionary({7: 1, 8: 1}, {9: 9}), {7: 1, 8: 1, 9: 9})
        self.assertEqual(merge_dictionary({7: 1, 8: 1}, {7: 9}), {7: 10, 8: 1})
        self.assertEqual(merge_dictionary({7: 1, 8: 1}, {8: 9}), {7: 1, 8: 10})

        # m = 2
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(2, [(6, 8), (9, 11), (7, 10)]), {(0, 2): [7, 8], (1, 2): [9, 10]})

        self.assertTrue(np.array_equal(matrix_of_m_overlaps_of_n_intervals(2, [(6, 8), (9, 11), (7, 10)]),
                                       [[None, False, list([7, 8])],
                                        [0, None, list([9, 10])],
                                        [0, 0, None]]))
        self.assertEqual(m_overlaps_of_n_intervals(2, [(6, 8), (9, 11), (7, 10)]), {(0, 2): [7, 8], (1, 2): [9, 10]})
        self.assertEqual(m_overlaps_of_n_intervals(3, [(6, 8), (9, 11), (7, 10)]), {})

        # m = 3
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(3, [(6, 8), (9, 11), (7, 10)]), {})
        self.assertTrue(np.array_equal(matrix_of_m_overlaps_of_n_intervals(3, [(6, 8), (9, 11), (7, 10)]),
                                       [[[None, None, None], [9, None, False], [9, 9, None]],
                                        [[9, 9, 9], [9, None, None], [9, 9, None]],
                                        [[9, 9, 9], [9, 9, 9], [9, 9, None]]]))

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(3, [(6, 8), (9, 11), (7, 10)]), {})
        self.assertTrue(np.array_equal(matrix_of_m_overlaps_of_n_intervals(3, [(6, 10), (9, 11), (7, 10)]),
                                       [[[None, None, None], [9, None, list([9, 10])], [9, 9, None]],
                                        [[9, 9, 9], [9, None, None], [9, 9, None]],
                                        [[9, 9, 9], [9, 9, 9], [9, 9, None]]]))

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(3, [(6, 10), (9, 11), (7, 10)]), {(0, 1, 2): [9, 10]})
        self.assertEqual(m_overlaps_of_n_intervals(3, [(6, 10), (9, 11), (7, 10)]), {(0, 1, 2): [9, 10]})
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(3, [(5, 10), (9, 11), (6, 10), (3, 7)]),
                         {(0, 1, 2): [9, 10], (0, 2, 3): [6, 7]})
        self.assertEqual(m_overlaps_of_n_intervals(3, [(5, 10), (9, 11), (6, 10), (3, 7)]), {(0, 1, 2): [9, 10], (0, 2, 3): [6, 7]})

        # m = 4
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(4, [(5, 10), (9, 11), (6, 10), (3, 7)]), {})
        self.assertEqual(m_overlaps_of_n_intervals(4, [(5, 10), (9, 11), (6, 10), (3, 7)]), {})
        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(4, [(5, 10), (6, 11), (6, 10), (3, 7)]), {(0, 1, 2, 3): [6, 7]})
        self.assertEqual(m_overlaps_of_n_intervals(4, [(5, 10), (6, 11), (6, 10), (3, 7)]), {(0, 1, 2, 3): [6, 7]})

        self.assertEqual(dictionary_of_m_overlaps_of_n_intervals(4, [(5, 10), (6, 11), (6, 10), (3, 7), (5, 6)], skip_whole_in=True),
                         {(0, 1, 2, 3): [6, 7]})
        self.assertEqual(m_overlaps_of_n_intervals(4, [(5, 10), (6, 11), (6, 10), (3, 7), (5, 6)], strict=True), {(0, 1, 2, 3): [6, 7]})

        # self.assertTrue(np.array_equal(get_submatrix(np.arange(10)*2, [1]), 2))
        # self.assertTrue(np.array_equal(get_submatrix(np.array([[1, 2, 3], [4, 5, 6]]), [1]), [4, 5, 6]))
        # self.assertTrue(np.array_equal(get_submatrix(np.array([[1, 2, 3], [4, 5, 6]]), [1, 2]), 6))
        # self.assertTrue(np.array_equal(get_submatrix(np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]), [1, 1]), [10, 11, 12]))

    def testParseTraces(self):
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
            self.assertEqual(trace0.frame_range_len, 2)
            self.assertAlmostEqual(trace0.trace_length, 4.242640687119286)
            self.assertAlmostEqual(trace0.max_step_len, 2.8284271247461903)
            self.assertEqual(trace0.max_step_len_step_index, 1)
            self.assertEqual(trace0.max_step_len_line, 3)
            self.assertEqual(trace0.max_step_len_frame_number, 1621)
            self.assertEqual(trace0.trace_lengths, {1.414214: 1, 2.828427: 1})
            self.assertEqual(trace0.frames_list, [1620, 1621, 1622])
            self.assertEqual(trace0.locations, [[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]])

            trace1 = Trace(traces[1], 1)
            self.assertEqual(trace1.trace_id, 1)
            self.assertEqual(trace1.frame_range, [1620, 1622])
            self.assertEqual(trace1.get_number_of_frames_tracked(), 3)
            self.assertEqual(trace1.frame_range_len, 2)
            self.assertAlmostEqual(trace1.trace_length, 7.6212327846342935)
            self.assertAlmostEqual(trace1.max_step_len, 5.385164807134505)
            self.assertEqual(trace1.max_step_len_step_index, 0)
            self.assertEqual(trace1.max_step_len_line, 1)
            self.assertEqual(trace1.max_step_len_frame_number, 1620)
            self.assertDictEqual(trace1.trace_lengths, {5.385165: 1, 2.236068: 1})
            self.assertEqual(trace1.frames_list, [1620, 1621, 1622])
            self.assertEqual(trace1.locations, [[0.0, 0.0], [2.0, 5.0], [3.0, 7.0]])

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
            self.assertEqual(merged_trace.frame_range_len, 5)
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

            trace0 = Trace(traces[0], 0)
            trace4 = Trace(traces[4], 4)

            merged_trace = merge_two_traces_with_gap(trace4, trace0)
            self.assertEqual(merged_trace.trace_id, 0)
            self.assertIsInstance(merged_trace, Trace)
            self.assertEqual(merged_trace.frame_range, [1620, 1635])
            self.assertEqual(merged_trace.get_number_of_frames_tracked(), 6)
            self.assertEqual(merged_trace.frame_range_len, 15)
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


            trace0 = Trace(traces[0], 0)
            trace5 = Trace(traces[5], 5)
            merged_trace = merge_two_traces_with_gap(trace5, trace0)
            spam = [[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]]
            spam.extend([[-sys.maxsize, -sys.maxsize]] * 502)
            spam.extend([[0.0, 0.0], [2.0, 5.0], [3.0, 7.0]])
            self.assertEqual(merged_trace.locations, spam)

    def testSwapTraces(self):
        with open('../test/test.csv', newline='') as csv_file:
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
