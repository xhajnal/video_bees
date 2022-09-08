import os.path
from termcolor import colored

from trace import Trace
from misc import dictionary_of_m_overlaps_of_n_intervals
from single_trace import single_trace_checker, check_inside_of_arena
from cross_traces import put_traces_together, track_reappearance, cross_trace_analyse, \
    trim_out_additional_agents_over_long_traces2, merge_overlapping_traces, get_whole_frame_range
from parse import parse_traces
from save import pickle_traces
from visualise import scatter_detection, show_all_traces, show_overlaps, show_gaps

global silent
global debug
global show_plots
silent = False
debug = False
show_plots = False


def set_show_plots(do_show_plots):
    global show_plots
    show_plots = do_show_plots


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

        real_whole_frame_range = get_whole_frame_range(traces)
        whole_frame_range = [real_whole_frame_range[0]-2000, real_whole_frame_range[1]+2000]

        # for trace in traces:
        #     print(trace.frame_range)
        # show_all_traces(traces, whole_frame_range)
        scatter_detection(traces, whole_frame_range)
        for trace in traces:
            print("trace", trace.trace_id, trace.frame_range)
        show_gaps(traces, whole_frame_range)
        show_overlaps(traces, whole_frame_range)

        raise Exception

        ## FIND TRACES OUTSIDE OF THE ARENA
        check_inside_of_arena(traces)
        if show_plots:
            show_all_traces(traces, whole_frame_range)

        ## FIND TRACES OF ZERO LENGTH
        if show_plots:
            scatter_detection(traces, whole_frame_range, subtitle="Initial.")
        single_trace_checker(traces, silent=silent, debug=debug)
        if show_plots:
            scatter_detection(traces, whole_frame_range, subtitle="After deleting traces with zero len in xy.")

        # show_gaps(traces, whole_frame_range)

        if population_size > 1:
            ## CHOSEN TRACE SHOW - choose i, index of trace
            i = 0
            # TODO uncomment the following line to show the selected trace
            # traces[i].show_trace_in_xy()

        ## CROSS-TRACE ANALYSIS
        cross_trace_analyse(traces, scraped_traces, silent=silent, debug=debug)

        ## ALL TRACES SHOW
        if show_plots:
            show_all_traces(traces, whole_frame_range)

        ## TRIM TRACES AND PUT NOT OVERLAPPING ONES TOGETHER
        before_number_of_traces = len(traces)
        after_number_of_traces = 0
        while (not before_number_of_traces == after_number_of_traces) and (len(traces) > population_size):
            before_number_of_traces = len(traces)
            traces = trim_out_additional_agents_over_long_traces2(traces, population_size, silent=silent, debug=debug)
            if show_plots:
                scatter_detection(traces, whole_frame_range, subtitle="after trimming")
            traces = put_traces_together(traces, population_size, silent=silent, debug=debug)
            if show_plots:
                scatter_detection(traces, whole_frame_range, subtitle="after putting traces together")
            after_number_of_traces = len(traces)

        print(colored(f"After trimming and putting not overlapping traces together there are {len(traces)} left:", "yellow"))
        if not silent:
            for index, trace in enumerate(traces):
                print(f"Trace {index} with id {trace.trace_id} of range {trace.frame_range}")

        scatter_detection(traces, whole_frame_range)
        for trace in traces:
            print("trace", trace.trace_id, trace.frame_range)

        # show_gaps(traces, whole_frame_range)

        ## ALL TRACES SHOW
        # if show_plots:
        show_all_traces(traces, whole_frame_range)

        if show_plots:
            track_reappearance(traces, show=debug)
        print()

        ## MERGE OVERLAPPING TRACES
        before_number_of_traces = len(traces)
        after_number_of_traces = -9
        while before_number_of_traces != after_number_of_traces:
            before_number_of_traces = len(traces)
            merge_overlapping_traces(traces, population_size, silent=silent, debug=debug, show=show_plots)
            after_number_of_traces = len(traces)

        print()
        if len(traces) >= 2:
            print(colored(f"Pairs of overlapping traces after merging overlapping traces: {dictionary_of_m_overlaps_of_n_intervals(2, list(map(lambda x: x.frame_range, traces)), skip_whole_in=False)}", "yellow"))
        else:
            pass
            # show_all_traces(traces)

        print(colored(f"After merging overlapping traces together there are {len(traces)} left:",
                      "yellow"))
        if not silent:
            for index, trace in enumerate(traces):
                print(f"Trace {index} with id {trace.trace_id} of range {trace.frame_range}")

        ## ALL TRACES
        # if show_plots:
        track_reappearance(traces, show=True)
        scatter_detection(traces, whole_frame_range, subtitle="after merging overlapping traces")
        show_overlaps(traces, whole_frame_range)
        show_gaps(traces, whole_frame_range)
        show_all_traces(traces, whole_frame_range)

        # save_traces(traces, os.path.basename(file_path), silent=silent, debug=debug)
        pickle_traces(traces, os.path.basename(file_path), silent=silent, debug=debug)
