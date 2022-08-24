from cross_traces import trim_out_additional_agents_over_long_traces, put_traces_together, track_reappearance, \
    cross_trace_analyse, trim_out_additional_agents_over_long_traces2, compare_two_traces
from parse import parse_traces
from single_trace import single_trace_checker
from trace import Trace
from visualise import scatter_detection, show_all_traces


global silent
global debug
silent = True
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

        scatter_detection(traces, subtitle="Initial.")
        single_trace_checker(traces, silent=silent, debug=debug)
        scatter_detection(traces, subtitle="After deleting traces with zero len in xy.")

        if population_size > 1:
            ## CHOSEN TRACE SHOW - choose i, index of trace
            i = 0
            traces[i].show_trace_in_xy()

        ## CROSS-TRACE ANALYSIS
        cross_trace_analyse(traces, scraped_traces, silent=silent, debug=debug)

        ## ALL TRACES SHOW
        show_all_traces(traces)

        ## TRIM TRACES
        before_number_of_traces = len(traces)
        after_number_of_traces = 0
        while (not before_number_of_traces == after_number_of_traces) and (len(traces) > population_size):
            before_number_of_traces = len(traces)
            traces = trim_out_additional_agents_over_long_traces2(traces, population_size, silent=silent, debug=debug)
            scatter_detection(traces, subtitle="after trimming")
            traces = put_traces_together(traces, population_size, silent=silent, debug=debug)
            scatter_detection(traces, subtitle="after putting traces together")
            after_number_of_traces = len(traces)

        if not silent:
            for index, trace in enumerate(traces):
                print(f"trace {index} with id {trace.trace_id} of range {trace.frame_range}")

        ## ALL TRACES SHOW
        show_all_traces(traces)

        track_reappearance(traces, show=True)
        print()
        compare_two_traces(traces[4], traces[5])
