from src.parse import parse_traces
from trace import merge_two_traces, Trace
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

        self.assertTrue(np.array_equal(m_overlaps_of_n_intervals(1, [(6, 8), (9, 11), (7, 10)]),
                                       [[list([6, 8]), 0, list([7, 8])],
                                        [0, list([9, 11]), list([9, 10])],
                                        [0, 0, list([7, 10])]]))
        self.assertTrue(np.array_equal(m_overlaps_of_n_intervals(2, [(6, 8), (9, 11), (7, 10)]),
                                       [[list([6, 8]), 0, list([7, 8])],
                                        [0, list([9, 11]), list([9, 10])],
                                       [0, 0, list([7, 10])]]))
        m_overlaps_of_n_intervals(2, [(6, 8), (9, 11), (7, 10)])
        #
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
                x = trace.frames_tracked
                y = [index] * len(x)
                ax1.scatter(x, y, alpha=0.5)
            plt.show()

            print(traces[0])
            trace0 = Trace(traces[0], 0)
            print(trace0)
            self.assertEqual(trace0.trace_id, 0)
            self.assertEqual(trace0.frame_range, (1620, 1622))
            self.assertEqual(trace0.number_of_frames, 3)
            self.assertEqual(trace0.frame_range_len, 2)
            self.assertAlmostEqual(trace0.trace_length, 4.242640687119286)
            self.assertAlmostEqual(trace0.max_step_len, 2.8284271247461903)
            self.assertEqual(trace0.max_step_len_step_index, 1)
            self.assertEqual(trace0.max_step_len_line, 3)
            self.assertEqual(trace0.max_step_len_frame_number, 1621)
            self.assertEqual(trace0.trace_lengths, {1.414214: 1, 2.828427: 1})
            self.assertEqual(trace0.frames_tracked, [1620, 1621, 1622])
            self.assertEqual(trace0.locations, [[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]])

            trace1 = Trace(traces[1], 1)
            self.assertEqual(trace1.trace_id, 1)
            self.assertEqual(trace1.frame_range, (1620, 1622))
            self.assertEqual(trace1.number_of_frames, 3)
            self.assertEqual(trace1.frame_range_len, 2)
            self.assertAlmostEqual(trace1.trace_length, 7.6212327846342935)
            self.assertAlmostEqual(trace1.max_step_len, 5.385164807134505)
            self.assertEqual(trace1.max_step_len_step_index, 0)
            self.assertEqual(trace1.max_step_len_line, 1)
            self.assertEqual(trace1.max_step_len_frame_number, 1620)
            self.assertDictEqual(trace1.trace_lengths, {5.385165: 1, 2.236068: 1})
            self.assertEqual(trace1.frames_tracked, [1620, 1621, 1622])
            self.assertEqual(trace1.locations, [[0.0, 0.0], [2.0, 5.0], [3.0, 7.0]])

            # print(trace0.frames_tracked)

            trace0.show_step_lengths_hist()
            trace1.show_step_lengths_hist()

            trace3 = Trace(traces[3], 3)
            # print(trace0)
            # print(trace3)
            #
            # print(trace0.frame_range)
            # print(trace3.frame_range)

            merged_trace = merge_two_traces(copy(trace0), copy(trace3))
            self.assertEqual(merged_trace.trace_id, 0)
            self.assertIsInstance(merged_trace, Trace)
            self.assertEqual(merged_trace.frame_range, (1620, 1625))
            self.assertEqual(merged_trace.number_of_frames, 6)
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
            self.assertEqual(merged_trace.frames_tracked, [1620, 1621, 1622, 1623, 1624, 1625])
            self.assertEqual(merged_trace.locations, [[0.0, 0.0], [1.0, 1.0], [3.0, 3.0], [0.0, 0.0], [2.0, 5.0], [3.0, 7.0]])

            trace0 = Trace(traces[0], 0)
            trace3 = Trace(traces[3], 3)

            merged_trace = merge_two_traces(trace3, trace0)
            self.assertEqual(merged_trace.trace_id, 0)
            self.assertIsInstance(merged_trace, Trace)
            self.assertEqual(merged_trace.frame_range, (1620, 1625))
            self.assertEqual(merged_trace.number_of_frames, 6)
            self.assertEqual(merged_trace.frame_range_len, 5)
            self.assertAlmostEqual(merged_trace.trace_length, 4.242640687119286 + 7.6212327846342935 + 4.24264068711928514)
            self.assertAlmostEqual(merged_trace.max_step_len, 5.3851648071)
            self.assertEqual(merged_trace.max_step_len_step_index, 0)
            self.assertEqual(merged_trace.max_step_len_line, 7)
            self.assertEqual(merged_trace.max_step_len_frame_number, 1623)
            # trace3.trace_lengths: {1.414214: 1, 2.828427: 1}
            # trace3.trace_lengths: {5.385165: 1, 2.236068: 1}
            # merge step: math.dist([3,3], [0,0])== 4.242640687119285
            self.assertDictEqual(merged_trace.trace_lengths,
                                 {1.414214: 1, 2.828427: 1, 5.385165: 1, 2.236068: 1, 4.242641: 1})
            self.assertEqual(merged_trace.frames_tracked, [1620, 1621, 1622, 1623, 1624, 1625])
            self.assertEqual(merged_trace.locations,
                             [[0.0, 0.0], [1.0, 1.0], [3.0, 3.0], [0.0, 0.0], [2.0, 5.0], [3.0, 7.0]])


if __name__ == '__main__':
    unittest.main()
