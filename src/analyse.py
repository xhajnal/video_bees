import os.path

from termcolor import colored

from cross_traces import put_traces_together, track_reappearance, cross_trace_analyse,\
    trim_out_additional_agents_over_long_traces2, merge_overlapping_traces
from misc import dictionary_of_m_overlaps_of_n_intervals
from parse import parse_traces
from save import save_traces, pickle_traces
from single_trace import single_trace_checker, check_inside_of_arena
from trace import Trace
from visualise import scatter_detection, show_all_traces


global silent
global debug
silent = False
debug = False


def set_silent(is_silent):
    global silent
    silent = is_silent


def set_debug(is_debug):
    global debug
    debug = is_debug


def analyse(file_path, population_size):
    """ Runs the whole file analysis

    :arg file_path: (str): path to csv file
    :arg population_size: (int): expected number of agents
    """
    with open(file_path, newline='') as csv_file:
        ## PARSER
        scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            # print(trace)
            # print(scraped_traces[trace])
            traces.append(Trace(scraped_traces[trace], index))

        # for trace in traces:
        #     print(trace.frame_range)
        # show_all_traces(traces)

        ## FIND TRACES OUTSIDE OF THE ARENA
        check_inside_of_arena(traces)
        # show_all_traces(traces)

        ## FIND TRACES OF ZERO LENGTH
        scatter_detection(traces, subtitle="Initial.")
        single_trace_checker(traces, silent=silent, debug=debug)
        scatter_detection(traces, subtitle="After deleting traces with zero len in xy.")

        if population_size > 1:
            ## CHOSEN TRACE SHOW - choose i, index of trace
            i = 0
            # TODO uncomment the following line to show the selected trace
            # traces[i].show_trace_in_xy()

        ## CROSS-TRACE ANALYSIS
        cross_trace_analyse(traces, scraped_traces, silent=silent, debug=debug)

        ## ALL TRACES SHOW
        # show_all_traces(traces)

        ## TRIM TRACES AND PUT NOT OVERLAPPING ONES TOGETHER
        before_number_of_traces = len(traces)
        after_number_of_traces = 0
        while (not before_number_of_traces == after_number_of_traces) and (len(traces) > population_size):
            before_number_of_traces = len(traces)
            traces = trim_out_additional_agents_over_long_traces2(traces, population_size, silent=silent, debug=debug)
            scatter_detection(traces, subtitle="after trimming")
            traces = put_traces_together(traces, population_size, silent=silent, debug=debug)
            scatter_detection(traces, subtitle="after putting traces together")
            after_number_of_traces = len(traces)

        print(colored(f"After trimming and putting not overlapping traces together there are {len(traces)} left:", "yellow"))
        if not silent:
            for index, trace in enumerate(traces):
                print(f"Trace {index} with id {trace.trace_id} of range {trace.frame_range}")

        ## ALL TRACES SHOW
        show_all_traces(traces)

        track_reappearance(traces, show=debug)
        print()

        ## MERGE OVERLAPPING TRACES
        merge_overlapping_traces(traces, population_size, silent=silent, debug=debug, show=True)
        print()
        if len(traces) >= 2:
            print(colored(f"Pairs of overlapping traces after merging overlapping traces: {dictionary_of_m_overlaps_of_n_intervals(2, list(map(lambda x: x.frame_range, traces)), while_not_in=True)}", "yellow"))
        else:
            pass
            # show_all_traces(traces)

        ## ALL TRACES SHOW
        show_all_traces(traces)

        # save_traces(traces, os.path.basename(file_path), silent=silent, debug=debug)
        pickle_traces(traces, os.path.basename(file_path), silent=silent, debug=debug)
