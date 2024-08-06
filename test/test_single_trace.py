import unittest
import matplotlib.pyplot as plt

from dave_io import parse_traces
from single_trace import remove_full_traces
from trace import Trace
from traces_logic import merge_two_traces_with_gap, compute_whole_frame_range
from misc import *
from visualise import scatter_detection


class MyTestCase(unittest.TestCase):
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
            self.assertEqual(trace0.get_frame_list(), [1620, 1621, 1622])

            self.assertEqual(trace0.get_gap_frame_range(), ())
            self.assertEqual(trace0.get_gap_locations(), [])
            self.assertEqual(trace0.get_overlap_frame_range(), ())
            self.assertEqual(trace0.get_overlap_locations(), [])
            self.assertEqual(trace0.get_location_from_frame(1620), [0.0, 0.0])
            self.assertEqual(trace0.get_location_from_frame(1621), [1.0, 1.0])
            self.assertEqual(trace0.get_location_from_frame(1622), [3.0, 3.0])
            self.assertEqual(trace0.get_locations_from_frame_range((1620, 1622)), [[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]])
            self.assertEqual(trace0.get_number_of_frames_tracked(), 3)
            trace0.assert_trace_consistency()
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
            self.assertEqual(trace1.get_frame_list(), [1620, 1621, 1622])

            self.assertEqual(trace1.get_gap_frame_range(), ())
            self.assertEqual(trace1.get_gap_locations(), [])
            self.assertEqual(trace1.get_overlap_frame_range(), ())
            self.assertEqual(trace1.get_overlap_locations(), [])
            self.assertEqual(trace1.get_location_from_frame(1620), [0.0, 0.0])
            self.assertEqual(trace1.get_location_from_frame(1621), [2.0, 5.0])
            self.assertEqual(trace1.get_location_from_frame(1622), [3.0, 7.0])
            self.assertEqual(trace1.get_locations_from_frame_range((1620, 1622)), [[0.0, 0.0], [2.0, 5.0], [3.0, 7.0]])
            self.assertEqual(trace1.get_number_of_frames_tracked(), 3)
            trace1.assert_trace_consistency()
            self.assertEqual(trace1.check_whether_is_done([1620, 1635]), False)
            self.assertEqual(trace1.check_whether_is_done([1620, 1622]), True)
            trace1.recalculate_trace_lengths()
            self.assertAlmostEqual(trace1.trace_length, 7.6212327846342935)
            self.assertEqual(trace1.trace_lengths, {5.385165: 1, 2.236068: 1})
            self.assertAlmostEqual(trace1.max_step_len, 5.385164807134505)

            print(traces[2])
            trace2 = Trace(traces[2], 2)
            print(trace2)
            self.assertEqual(trace2.get_frame_list(), [1620])
            trace2.assert_trace_consistency()


            print(traces[7])
            trace7 = Trace(traces[7], 7)
            print(trace7)
            spam0 = trace7.calculate_path_len_from_range((1620, 1621))
            spam1 = trace7.calculate_path_len_from_range((1621, 1622))
            spam2 = trace7.calculate_path_len_from_range((1622, 1623))
            self.assertEqual(trace0.get_frame_list(), [1620, 1621, 1622])
            self.assertAlmostEqual(math.sqrt(29), spam0)
            self.assertAlmostEqual(math.sqrt(5), spam1)
            self.assertEqual(3, spam2)
            self.assertAlmostEqual(spam1 + spam2, trace7.calculate_path_len_from_range((1621, 1623)))
            self.assertAlmostEqual(spam0 + spam1, trace7.calculate_path_len_from_range((1620, 1622)))
            self.assertAlmostEqual(spam0 + spam1 + spam2, trace7.calculate_path_len_from_range((1620, 1623)))
            trace7.frame_range = [1623, 1620]
            with self.assertRaises(AssertionError):
                trace7.assert_trace_consistency()

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
            merged_trace.assert_trace_consistency()
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
            merged_trace.assert_trace_consistency()
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


if __name__ == '__main__':
    unittest.main()
