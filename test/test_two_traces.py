import unittest
import analyse
from dave_io import parse_traces
from trace import Trace
from primal_traces_logic import get_traces_from_range
from traces_logic import swap_two_overlapping_traces, merge_two_traces_with_gap, compute_whole_frame_range, \
    partition_frame_range_by_number_of_traces, reverse_partition_frame_range_by_number_of_traces, compare_two_traces, \
    compare_two_traces_with_shift, merge_multiple_pairs_of_overlapping_traces, check_to_merge_two_overlapping_traces, \
    order_traces
from misc import *


class MyTestCase(unittest.TestCase):
    ## TWO TRACES LOGIC TESTS
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

if __name__ == '__main__':
    unittest.main()