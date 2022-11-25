import os.path
from pathlib import Path
from time import time
import glob
from _socket import gethostname
from termcolor import colored

from video import annotate_video, show_video
from config import get_min_trace_len, get_vicinity_of_short_traces
from trace import Trace
from misc import dictionary_of_m_overlaps_of_n_intervals
from single_trace import single_trace_checker, check_inside_of_arena, track_jump_back_and_forth, remove_full_traces
from cross_traces import put_gaping_traces_together, track_reappearance, cross_trace_analyse, \
    trim_out_additional_agents_over_long_traces2, merge_overlapping_traces, get_whole_frame_range, \
    track_swapping_loop, get_video_whole_frame_range
from dave_io import pickle_traces, save_traces, save_setting, convert_results_from_json_to_csv, is_new_config, parse_traces, \
    get_video_path
from triplets import merge_overlapping_triplets_of_traces
from visualise import scatter_detection, show_plot_locations, show_overlaps, show_gaps

global batch_run
global silent
global debug
global show_plots
global show_all_plots
global guided
global rerun

# USER - please set up the following 6 flags
batch_run = False       # sets silent, not debug, not show_plots, rerun
silent = False          # minimal print
debug = False           # maximal print
show_plots = True       # showing plots
show_all_plots = False  # showing all plots - also those in the loops
guided = False          # human guided version (in progress)
rerun = True            # will execute also files with a setting which is already in the results


def set_show_plots(do_show_plots):
    global show_plots
    show_plots = do_show_plots


def set_show_all_plots(do_show_all_plots):
    global show_all_plots
    show_all_plots = do_show_all_plots


def set_silent(is_silent):
    global silent
    silent = is_silent


def set_debug(is_debug):
    global debug
    debug = is_debug


def set_rerun(do_rerun):
    global rerun
    rerun = do_rerun


def set_guided(do_guided):
    global guided
    guided = do_guided


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
    # Set run setting
    #################
    if batch_run:  # sets silent, not debug, not show_plots, not guided, rerun
        set_silent(True)
        set_debug(False)
        set_show_plots(False)
        set_show_all_plots(False)
        set_rerun(True)
        set_guided(False)

    if guided:
        set_rerun(True)
        set_show_plots(True)
        set_silent(False)

    if show_plots is False:
        set_show_all_plots(False)

    # set_show_plots(False)

    #################
    # Internal params
    #################
    counts = []
    removed_short_traces = []
    removed_full_traces = []
    original_population_size = population_size

    ############
    # I/O stuff
    ############
    video_file, output_video_file = get_video_path(file_path)
    # print(output_video_file)

    ####################
    # PARSE CSV & CONFIG
    ####################
    try:
        with open(file_path, newline='') as csv_file:
            #################
            # Check whether this is new setting
            #################
            if not rerun:
                if not is_new_config(file_name=file_path):
                    return
            # parse traces from csv file
            scraped_traces = parse_traces(csv_file)
    except FileNotFoundError:
        print(colored(f"File not found!", "magenta"))
        return

    # Store traces as list of Traces
    traces = []
    for index, trace in enumerate(scraped_traces.keys()):
        # print(trace)
        # print(scraped_traces[trace])
        traces.append(Trace(scraped_traces[trace], index))

    # Storing the number of loaded traces
    counts.append(len(traces) + len(removed_full_traces))

    ### AUXILIARY COMPUTATION
    ## FRAME RANGE
    # obtain the frame range of the video
    real_whole_frame_range = get_whole_frame_range(traces)
    # compute frame range margins for visualisation
    whole_frame_range = get_video_whole_frame_range(traces)

    ### ANALYSIS
    if show_plots:
        # scatter_detection(traces, whole_frame_range, from_to_frame=[0, 2000], subtitle="Initial.")
        # show_plot_locations(traces, whole_frame_range, from_to_frame=[0, 1800], subtitle="Initial.")
        scatter_detection(traces, whole_frame_range, subtitle="Initial.")
        show_plot_locations(traces, whole_frame_range, subtitle="Initial.")

    ##################################
    # FIND TRACES OUTSIDE OF THE ARENA
    ##################################
    check_inside_of_arena(traces)
    # Storing the number of traces inside of arena
    counts.append(len(traces) + len(removed_full_traces))

    # TODO uncomment the following
    # if show_plots:
    #     show_plot_locations(traces, whole_frame_range, subtitle="Traces outside of arena gone.")
    #     scatter_detection(traces, whole_frame_range, subtitle="Traces outside of arena gone.")

    #####################################################################
    # FIND TRACES OF ZERO LENGTH and SHORT FRAME RANGE TRACES, TRACE INFO
    #####################################################################
    traces, removed_short_traces = single_trace_checker(traces, min_range_len=get_min_trace_len(), vicinity=get_vicinity_of_short_traces(), silent=silent, debug=debug)
    counts.append(len(traces) + len(removed_full_traces))
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

    if has_tracked_video and guided:
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
    ## TODO uncomment the following if want the plot
    # if show_plots:
    #     show_plot_locations(traces, whole_frame_range, subtitle="before TRIM REDUNDANT OVERLAPPING TRACES AND PUT GAPING TRACES TOGETHER")
    before_number_of_traces = len(traces)
    after_number_of_traces = 0
    while (not before_number_of_traces == after_number_of_traces) and (len(traces) > population_size):
        before_number_of_traces = len(traces)
        traces = trim_out_additional_agents_over_long_traces2(traces, population_size, silent=silent, debug=debug)
        if show_all_plots:
            scatter_detection(traces, whole_frame_range, subtitle="After trimming redundant overlapping traces.")
        traces = put_gaping_traces_together(traces, population_size, silent=silent, debug=debug)
        if show_all_plots:
            scatter_detection(traces, whole_frame_range, subtitle="After putting gaping traces together.")
        after_number_of_traces = len(traces)

    # Storing the number of traces after TRIM REDUNDANT OVERLAPPING TRACES AND PUT GAPING TRACES TOGETHER
    counts.append(len(traces) + len(removed_full_traces))
    if not silent:
        print(colored(f"After trimming overlapping redundant traces and putting gaping traces together there are {len(traces)} left:", "yellow"))
        for index, trace in enumerate(traces):
            print(f"Trace {index}({trace.trace_id}) of range {trace.frame_range}")

    ## ALL TRACES SHOW
    if show_plots:
        # scatter_detection(traces, whole_frame_range)
        show_gaps(traces, whole_frame_range, silent=silent, debug=debug, subtitle="After Cross analysis phase 1.")
        show_overlaps(traces, whole_frame_range, silent=silent, debug=debug, subtitle="After Cross analysis phase 1.")
        show_plot_locations(traces, whole_frame_range, subtitle="After Cross analysis phase 1.")
        # track_reappearance(traces, show=True)

    # set_show_plots(True)

    ###########################
    ## MERGE OVERLAPPING TRACES
    ###########################
    # run until no traces are merged
    before_before_number_of_traces = len(traces)
    after_after_number_of_traces = -9
    while before_before_number_of_traces != after_after_number_of_traces:
        before_before_number_of_traces = len(traces)
        ## MERGE OVERLAPPING PAIRS
        before_number_of_traces = len(traces)
        after_number_of_traces = -9
        while before_number_of_traces != after_number_of_traces:
            before_number_of_traces = len(traces)
            merge_overlapping_traces(traces, whole_frame_range, population_size, silent=silent, debug=debug, show=show_all_plots)
            after_number_of_traces = len(traces)

        ## MERGE OVERLAPPING TRIPLETS
        before_number_of_traces = len(traces)
        after_number_of_traces = -9
        while before_number_of_traces != after_number_of_traces:
            before_number_of_traces = len(traces)
            merge_overlapping_triplets_of_traces(traces, whole_frame_range, population_size, guided=guided,
                                                 input_video=video_file, silent=silent, debug=debug, show=show_all_plots)
            after_number_of_traces = len(traces)
        if len(traces) > population_size:
            traces = trim_out_additional_agents_over_long_traces2(traces, population_size, silent=silent, debug=debug)
        ## RECOLLECT NUMBER OF TRACES
        after_after_number_of_traces = len(traces)

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

    # set_show_plots(True)
    # scatter_detection(traces, whole_frame_range, subtitle="After merging overlapping traces.")

    # Storing the number of traces after MERGE OVERLAPPING TRACES and OVERLAPPING TRIPLETS
    counts.append(len(traces) + len(removed_full_traces))

    ############################
    ## REMOVE TRACES OF FULL LEN
    ############################
    if len(traces) > 1:
        traces, removed_full_traces, new_population_size = remove_full_traces(traces, removed_full_traces, real_whole_frame_range, population_size)
    else:
        new_population_size = population_size

    # if show_plots:
    #     scatter_detection(traces, whole_frame_range, subtitle="After merging overlapping traces.")

    # print("SECOND Gaping traces analysis")
    # before_number_of_traces = len(traces)
    # after_number_of_traces = 0
    # while (not before_number_of_traces == after_number_of_traces) and (len(traces) > new_population_size):
    #     before_number_of_traces = len(traces)
    #     traces = trim_out_additional_agents_over_long_traces2(traces, new_population_size, silent=silent, debug=debug)
    #     if show_all_plots:
    #         scatter_detection(traces, whole_frame_range, subtitle="After trimming redundant overlapping traces.")
    #     traces = put_gaping_traces_together(traces, new_population_size, silent=silent, debug=debug)
    #     if show_all_plots:
    #         scatter_detection(traces, whole_frame_range, subtitle="After putting gaping traces together.")
    #     after_number_of_traces = len(traces)
    #
    # # Storing the number of traces after second TRIM REDUNDANT OVERLAPPING TRACES AND PUT GAPING TRACES TOGETHER
    # counts.append(len(traces) + len(removed_traces))

    ## VISUALISATIONS
    if show_plots:
        track_reappearance(traces, show=True)
        scatter_detection(traces, whole_frame_range, subtitle="Final.")
        show_overlaps(traces, whole_frame_range, subtitle="Final.", silent=silent, debug=debug)
        show_gaps(traces, whole_frame_range, subtitle="Final.", silent=silent, debug=debug)
        show_plot_locations(traces, whole_frame_range, subtitle="Final.")

    ## SAVE RESULTS
    is_new = save_setting(counts, file_name=file_path, population_size=original_population_size, silent=silent, debug=debug)
    if is_new:
        convert_results_from_json_to_csv(silent=silent, debug=debug)
        # TODO uncomment the following
        # save_traces(traces, os.path.basename(file_path), silent=silent, debug=debug)
        # pickle_traces(traces, os.path.basename(file_path), silent=silent, debug=debug)
    # raise Exception

    # ### ANNOTATE THE VIDEO
    # if has_video or has_tracked_video:
    #     all_traces = removed_full_traces
    #     all_traces.extend(traces)
    #     annotate_video(video_file, output_video_file, all_traces, min(traces[0].frame_range[0], removed_full_traces[0].frame_range[0]))
