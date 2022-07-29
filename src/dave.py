from trace import Trace
from parse import parse_traces
from analyse import trim_out_additional_agents_over_long_traces, put_traces_together, scatter_detection, \
    track_reappearence

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
    with open('../data/Video_tracking/190823/20190823_114450691_1BEE_generated_20210506_100518_nn.csv', newline='') as csv_file:
        ## PARSER
        scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            # print(trace)
            # print(scraped_traces[trace])
            traces.append(Trace(scraped_traces[trace], index))

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
        raise Exception()

    # with open('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv', newline='') as csv_file:
        # TODO uncomment the following line
        # print(dummy_collision_finder(csv_file, 2))

        ## PARSER
        scraped_traces = parse_traces(csv_file)
        traces = []
        for index, trace in enumerate(scraped_traces.keys()):
            # print(trace)
            # print(scraped_traces[trace])
            traces.append(Trace(scraped_traces[trace], index))

        ## INDEPENDENT TRACE-LIKE ANALYSIS
        # TODO uncomment the following line
        # single_trace_checker(traces)

        # TODO uncomment the following line
        # for trace in traces:
        #     trace.show_step_lengths_hist(bins=5000)

        # TODO uncomment the following line
        # traces[0].show_step_lengths_hist(bins=5000)

        ## SCATTER PLOT OF DETECTIONS
        scatter_detection(traces)

        ## TRIM TRACES
        before_number_of_traces = len(traces)
        after_number_of_traces = 0
        while not before_number_of_traces == after_number_of_traces:
            before_number_of_traces = len(traces)
            traces = trim_out_additional_agents_over_long_traces(traces, 2)
            scatter_detection(traces)
            traces = put_traces_together(traces, 2)
            scatter_detection(traces)
            after_number_of_traces = len(traces)

        track_reappearence(traces)
        raise Exception()

        ## CROSS-TRACE ANALYSIS
        for index, trace in enumerate(traces):
            for index2, trace2 in enumerate(traces):
                if index == index2:
                    continue
                if abs(trace.frame_range[1] - trace2.frame_range[0]) < 100:
                    # print(traces[index])
                    # print(traces[index]["23325"])
                    # print()
                    # print(traces[index][str(trace.frame_range[1])][1])
                    # print(traces[index2][str(trace2.frame_range[0])][1])
                    point_distance = math.dist(list(map(float, (scraped_traces[index][str(trace.frame_range[1])][1]))),
                                               list(map(float, (scraped_traces[index2][str(trace2.frame_range[0])][1]))))
                    message = "The beginning of trace", index2, "is close to end of trace", index, "by", abs(
                        trace.frame_range[1] - trace2.frame_range[0]), "while the x,y distance is ", point_distance, "Consider joining them."

                    if index2 == index + 1:
                        if point_distance < 10:
                            print(colored(message, "blue"))
                        else:
                            print(colored(message, "yellow"))
                    else:
                        print(message)
