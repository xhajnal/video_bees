import os.path
from pathlib import Path
from time import time
import glob
from _socket import gethostname
from termcolor import colored

from trace import Trace
from misc import dictionary_of_m_overlaps_of_n_intervals
from single_trace import single_trace_checker, check_inside_of_arena, track_jump_back_and_forth, remove_full_traces
from cross_traces import put_gaping_traces_together, track_reappearance, cross_trace_analyse, \
    trim_out_additional_agents_over_long_traces2, merge_overlapping_traces, get_whole_frame_range, \
    track_swapping_loop, get_video_whole_frame_range
from dave_io import pickle_traces, save_traces, save_setting, convert_results_from_json_to_csv, is_new_config, parse_traces, \
    get_video_path
from visualise import scatter_detection, show_plot_locations, show_overlaps, show_gaps

global silent
global debug
global show_plots

# USER - please set up the following three flags
silent = True
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


def analyse(file_path, population_size, swaps=False, has_video=False, has_tracked_video=False):
    """ Runs the whole file analysis.

    :arg file_path: (str): path to csv file
    :arg population_size: (int): expected number of agents
    :arg swaps: (list of int): list of frame number of swaps to auto-pass
    :arg has_video: (bool): flag whether any video is available
    :arg has_tracked_video: (bool): flag whether a video with tracking is available
    """
    print(colored(f"Gonna analyse {file_path}", "magenta"))

    #################
    # Internal params
    #################
    counts = []
    removed_traces = []

    ############
    # I/O stuff
    ############
    video_file, output_video_file = get_video_path(file_path)

    ####################
    # PARSE CSV & CONFIG
    ####################
    try:
        with open(file_path, newline='') as csv_file:
            #################
            # Check whether this is new setting
            #################
            if not is_new_config(file_name=file_path):
                return
            # parse traces from csv file
            scraped_traces = parse_traces(csv_file)
    except FileNotFoundError:
        print(colored(f"File not found!", "magenta"))
        return

    # store traces as list of Traces
    traces = []
    for index, trace in enumerate(scraped_traces.keys()):
        # print(trace)
        # print(scraped_traces[trace])
        traces.append(Trace(scraped_traces[trace], index))

    # Storing the number of loaded traces
    counts.append(len(traces) + len(removed_traces))

    ### AUXILIARY COMPUTATION
    ## FRAME RANGE
    # obtain the frame range of the video
    real_whole_frame_range = get_whole_frame_range(traces)
    # compute frame range margins for visualisation
    whole_frame_range = get_video_whole_frame_range(traces)

    ### ANALYSIS
    if show_plots:
        scatter_detection(traces, whole_frame_range, subtitle="Initial.")
        show_plot_locations(traces, whole_frame_range, subtitle="Initial.")

    ##################################
    # FIND TRACES OUTSIDE OF THE ARENA
    ##################################
    check_inside_of_arena(traces)
    # Storing the number of traces inside of arena
    counts.append(len(traces) + len(removed_traces))

    # TODO uncomment the following
    # if show_plots:
    #     show_plot_locations(traces, whole_frame_range, subtitle="Traces outside of arena gone.")
    #     scatter_detection(traces, whole_frame_range, subtitle="Traces outside of arena gone.")

    ########################################
    # FIND TRACES OF ZERO LENGTH, TRACE INFO
    ########################################
    single_trace_checker(traces, silent=silent, debug=debug)
    # TODO uncomment the following
    # if show_plots:
    #     scatter_detection(traces, whole_frame_range, subtitle="After deleting traces with zero len in xy.")

    ############################
    # TRACK JUMPS BACK AND FORTH
    ############################
    start_time = time()
    print(colored(f"TRACE JUMP BACK AND FORTH CHECKER", "blue"))
    number_of_jump_detected = 0
    for index, trace in enumerate(traces):
        number_of_jump_detected = number_of_jump_detected + track_jump_back_and_forth(trace, index, whole_frame_range, show_plots=True, silent=silent, debug=debug)
    print(colored(f"We have found and fixed {number_of_jump_detected} jumps. It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "yellow"))
    # if show_plots:
    #     scatter_detection(traces, whole_frame_range, subtitle="After dealing with fake jumps there and back.")
    # Storing the number of jumps detected
    counts.append(number_of_jump_detected)

    if population_size > 1:
        ## CHOSEN TRACE SHOW - choose i, index of trace
        i = 0
        # TODO uncomment the following line to show selected trace
        # traces[i].show_trace_in_xy()

    ## CROSS-TRACE ANALYSIS
    cross_trace_analyse(traces, scraped_traces, silent=silent, debug=debug)

    #############################
    # CHECK FOR SWAPPING THE BEES
    #############################
    ## TODO uncomment the following
    # if show_plots:
    #     show_overlaps(traces, whole_frame_range)

    if has_tracked_video:
        number_of_swaps = track_swapping_loop(traces, whole_frame_range, automatically_swap=swaps, silent=silent, debug=debug)
        # Storing the number of swaps done
        counts.append(number_of_swaps)
    else:
        counts.append(0)

    ## TODO uncomment the following
    # ## ALL TRACES SHOW
    # if show_plots:
    #     show_plot_locations(traces, whole_frame_range, subtitle="After swapping.")
    #     scatter_detection(traces, whole_frame_range, subtitle="After swapping.")

    ##################################################################
    # TRIM REDUNDANT OVERLAPPING TRACES AND PUT GAPING TRACES TOGETHER
    ##################################################################
    if show_plots:
        show_plot_locations(traces, whole_frame_range, subtitle="before TRIM REDUNDANT OVERLAPPING TRACES AND PUT GAPING TRACES TOGETHER")
    before_number_of_traces = len(traces)
    after_number_of_traces = 0
    while (not before_number_of_traces == after_number_of_traces) and (len(traces) > population_size):
        before_number_of_traces = len(traces)
        traces = trim_out_additional_agents_over_long_traces2(traces, population_size, silent=silent, debug=debug)
        if show_plots:
            scatter_detection(traces, whole_frame_range, subtitle="After trimming redundant overlapping traces.")
        traces = put_gaping_traces_together(traces, population_size, silent=silent, debug=debug)
        if show_plots:
            scatter_detection(traces, whole_frame_range, subtitle="After putting gaping traces together.")
        after_number_of_traces = len(traces)

    # Storing the number of traces after TRIM REDUNDANT OVERLAPPING TRACES AND PUT GAPING TRACES TOGETHER
    counts.append(len(traces) + len(removed_traces))
    if not silent:
        print(colored(f"After trimming and putting not overlapping traces together there are {len(traces)} left:", "yellow"))
        for index, trace in enumerate(traces):
            print(f"Trace {index}({trace.trace_id}) of range {trace.frame_range}")

    if show_plots:
        # scatter_detection(traces, whole_frame_range)
        show_gaps(traces, whole_frame_range, silent=silent, debug=debug)
        show_overlaps(traces, whole_frame_range, silent=silent, debug=debug)

    # show_gaps(traces, whole_frame_range)

    ## ALL TRACES SHOW
    if show_plots:
        show_plot_locations(traces, whole_frame_range)
        track_reappearance(traces, show=debug)

    ###########################
    ## MERGE OVERLAPPING TRACES
    ###########################
    # run `merge_overlapping_traces` until no traces are merged
    before_number_of_traces = len(traces)
    after_number_of_traces = -9
    while before_number_of_traces != after_number_of_traces:
        before_number_of_traces = len(traces)
        merge_overlapping_traces(traces, whole_frame_range, population_size, silent=silent, debug=debug, show=False)
        after_number_of_traces = len(traces)

    # Storing the number of traces after MERGE OVERLAPPING TRACES
    counts.append(len(traces) + len(removed_traces))
    # QA of `merge_overlapping_traces`
    if len(traces) >= 2:
        if not silent:
            print(colored(f"Pairs of overlapping traces after merging overlapping traces: {dictionary_of_m_overlaps_of_n_intervals(2, list(map(lambda x: x.frame_range, traces)), skip_whole_in=False)}", "yellow"))
    else:
        pass
        # show_plot_locations(traces)

    if not silent:
        print(colored(f"After merging overlapping traces together there are {len(traces)} left:", "yellow"))
        for index, trace in enumerate(traces):
            print(f"Trace {index} ({trace.trace_id}) of range {trace.frame_range}")

    if len(traces) > 1:
        traces, removed_traces, new_population_size = remove_full_traces(traces, removed_traces, real_whole_frame_range, population_size)
    else:
        new_population_size = population_size

    if show_plots:
        scatter_detection(traces, whole_frame_range, subtitle="After merging overlapping traces.")

    print("SECOND Gaping traces analysis")
    before_number_of_traces = len(traces)
    after_number_of_traces = 0
    while (not before_number_of_traces == after_number_of_traces) and (len(traces) > new_population_size):
        before_number_of_traces = len(traces)
        traces = trim_out_additional_agents_over_long_traces2(traces, new_population_size, silent=silent, debug=debug)
        if show_plots:
            scatter_detection(traces, whole_frame_range, subtitle="After trimming redundant overlapping traces.")
        traces = put_gaping_traces_together(traces, new_population_size, silent=silent, debug=debug)
        if show_plots:
            scatter_detection(traces, whole_frame_range, subtitle="After putting gaping traces together.")
        after_number_of_traces = len(traces)

    # Storing the number of traces after second TRIM REDUNDANT OVERLAPPING TRACES AND PUT GAPING TRACES TOGETHER
    counts.append(len(traces) + len(removed_traces))

    ## VISUALISATIONS
    if show_plots:
        track_reappearance(traces, show=True)
        scatter_detection(traces, whole_frame_range, subtitle="Final.")
        show_overlaps(traces, whole_frame_range, subtitle="Final.", silent=silent, debug=debug)
        show_gaps(traces, whole_frame_range, subtitle="Final.", silent=silent, debug=debug)
        show_plot_locations(traces, whole_frame_range, subtitle="Final.")

    ## SAVE RESULTS
    is_new = save_setting(counts, file_name=file_path, population_size=population_size, silent=silent, debug=debug)
    if is_new:
        convert_results_from_json_to_csv(silent=silent, debug=debug)
        save_traces(traces, os.path.basename(file_path), silent=silent, debug=debug)
        pickle_traces(traces, os.path.basename(file_path), silent=silent, debug=debug)
    # raise Exception
    # ### ANNOTATE THE VIDEO
    # annotate_video(video_file, output_video_file, traces, traces[0].frame_range[0])
