import unittest

import analyse
from cross_traces import track_swapping_loop, \
    trim_out_additional_agents_over_long_traces_by_partition_with_build_fallback, \
    merge_alone_overlapping_traces_by_partition, merge_alone_overlapping_traces, merge_overlapping_traces_brutto
from dave_io import parse_traces, load_decisions
from single_trace import single_trace_checker, remove_full_traces
from trace import Trace
from traces_logic import swap_two_overlapping_traces, merge_two_traces_with_gap, compute_whole_frame_range, \
    partition_frame_range_by_number_of_traces, reverse_partition_frame_range_by_number_of_traces, compare_two_traces, \
    compare_two_traces_with_shift, merge_multiple_pairs_of_overlapping_traces, check_to_merge_two_overlapping_traces, \
    order_traces
from misc import *
from visualise import scatter_detection


class MyTestCase(unittest.TestCase):
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

        merge_alone_overlapping_traces(traces, None, 1, silent=False, debug=True)
        self.assertEqual(len(traces), 2)


        csv_file_path = '../test/test2.csv'
        with open(csv_file_path, newline='') as csv_file:
            scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            traces.append(Trace(scraped_traces[trace], index))
        pairs_of_traces_indices_to_merge, ids_of_traces_to_be_merged = merge_alone_overlapping_traces_by_partition(traces, silent=True, debug=False)
        self.assertEqual(len(traces), 2)


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
        analyse.decisions = load_decisions()
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