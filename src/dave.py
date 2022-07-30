from analyse import analyse
from trace import Trace
from parse import parse_traces
from cross_traces import trim_out_additional_agents_over_long_traces, put_traces_together, track_reappearence
from visualise import scatter_detection
from single_trace import single_trace_checker

if __name__ == "__main__":
    # i = 0
    # with open('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv',
    #           newline='') as csv_file:
    #     reader = csv.DictReader(csv_file)
    #     for row in reader:
    #         i = i + 1
    #         print(row['date'], row['err'], row['frame_count'], row['frame_number'], row['frame_timestamp'], row['name'], row['oid'], row['type'], row['x'], row['y'])
    #         print(row['oid'])

    #
    # with open('../data/Video_tracking/190823/20190823_115857275_2BEES_generated_20210507_083510_nn.csv',
    #           newline='') as csv_file:
    #     scraped_traces = parse_traces(csv_file)
    #     traces = []
    #     for index, trace in enumerate(scraped_traces.keys()):
    #         traces.append(Trace(scraped_traces[trace], index))
    #
    #     ## INDEPENDENT TRACE-LIKE ANALYSIS
    #     for index, trace in enumerate(traces):
    #         print("Agent number", index,
    #               ". Number_of_frames, frame_range_len, trace_length, max_step_len, max_step_len_index, max_step_len_line:",
    #               trace)
    #         if trace.trace_length == 0:
    #             print("This trace has length of 0. Consider deleting this agent")  ## this can be FP
    #         if trace.max_step_len > bee_max_step_len:
    #             print("This agent has moved", bee_max_step_len, "in a single step, you might consider deleting it.")
    #
    #         # trace.show_step_lengths_hist()
    #
    #     ## SCATTER PLOT OF DETECTIONS
    #     scatter_detection(traces)

    ## SINGLE BEE xxxx22
    # with open('../data/Video_tracking/190822/20190822_111607344_1BEE_generated_20210430_080914_nn.csv',
    #           newline='') as csv_file:
    #     ## PARSER
    #     scraped_traces = parse_traces(csv_file)
    #     traces = []
    #     for index, trace in enumerate(scraped_traces.keys()):
    #         # print(trace)
    #         # print(scraped_traces[trace])
    #         traces.append(Trace(scraped_traces[trace], index))
    #
    #     trace = traces[0]
    #     assert isinstance(trace, Trace)
    #     print("single bee always tracked max step", trace.max_step_len)
    #     trace.show_trace_in_xy()

    ## SINGLE BEE xxxx23
    analyse('../data/Video_tracking/190823/20190823_114450691_1BEE_generated_20210506_100518_nn.csv')
