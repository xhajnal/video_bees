from cross_traces import trim_out_additional_agents_over_long_traces, put_traces_together, track_reappearence, \
    cross_trace_analyse
from parse import parse_traces
from single_trace import single_trace_checker
from trace import Trace
from visualise import scatter_detection


def analyse(file_path):
    """ Runs the whole file analysis

    :arg file_path: (str): path to csv file
    """
    with open(file_path, newline='') as csv_file:
        ## PARSER
        scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            # print(trace)
            # print(scraped_traces[trace])
            traces.append(Trace(scraped_traces[trace], index))

        single_trace_checker(traces)
        scatter_detection(traces)

        ## CHOSEN TRACE SHOW - choose i, index of trace
        i = 0
        traces[i].show_trace_in_xy()

        ## ALL TRACES SHOW
        for index, trace in enumerate(traces):
            if index == 0:
                figs = trace.show_trace_in_xy(show=False)
            elif index < len(traces):
                figs = trace.show_trace_in_xy(figs, show=False)
            else:
                figs = trace.show_trace_in_xy(figs, show=True)

        ## TRIM TRACES
        before_number_of_traces = len(traces)
        after_number_of_traces = 0
        while not before_number_of_traces == after_number_of_traces:
            before_number_of_traces = len(traces)
            traces = trim_out_additional_agents_over_long_traces(traces, 1)
            scatter_detection(traces)
            traces = put_traces_together(traces, 1)
            scatter_detection(traces)
            after_number_of_traces = len(traces)

        track_reappearence(traces)

        ## CROSS-TRACE ANALYSIS
        cross_trace_analyse(traces, scraped_traces)
