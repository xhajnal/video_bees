import os.path
from time import time
from _socket import gethostname
from termcolor import colored

from counts import *
from cross_traces import trim_out_additional_agents_over_long_traces_by_partition_with_build_fallback, \
    merge_alone_overlapping_traces_by_partition, merge_overlapping_traces_brutto
from guided_traces import full_guided
from video import annotate_video, parse_video_info, show_video
from config import get_min_trace_len, get_vicinity_of_short_traces, hash_config, get_max_shift
from trace import Trace
from misc import dictionary_of_m_overlaps_of_n_intervals
from single_trace import single_trace_checker, check_inside_of_arena, track_jump_back_and_forth, remove_full_traces
from cross_traces import put_gaping_traces_together, track_reappearance, cross_trace_analyse, \
    merge_alone_overlapping_traces, track_swapping_loop
from traces_logic import compute_whole_frame_range, get_video_whole_frame_range, delete_traces_from_saved_decisions, \
    smoothen_traces_from_saved_decisions, fix_decisions
from dave_io import pickle_traces, save_current_result, convert_results_from_json_to_csv, is_new_config, \
    parse_traces, get_video_path, pickle_load, load_result_traces, pickled_exist, save_traces_as_csv, load_traces, \
    load_decisions
from triplets import merge_overlapping_triplets_of_traces, merge_overlapping_triplets_brutto, \
    merge_triplets_by_partition
from visualise import scatter_detection, show_plot_locations, show_overlaps, show_gaps

global traces
global real_whole_frame_range
global whole_frame_range
global video_file
global video_params
global deleted_traces

# global batch_run
# global silent
# global debug
# global show_plots
# global show_all_plots
# global guided
# global allow_force_merge
# global rerun
# global just_annotate
just_annotate = False
# global just_align
just_align = False
# global force_new_video
force_new_video = False
traces = []

# USER - please set up the following 8 flags
batch_run = False               # sets silent, not debug, not show_plots, not guided, rerun
guided = False                  # human guided version
silent = True                   # minimal print
debug = False                   # maximal print
show_plots = True               # showing plots
show_all_plots = False          # showing all plots - also those in the loops
allow_force_merge = False       # allows force merge gaps and overlaps
rerun = True                    # will execute also files with a setting which is already in the results
save_parsed_as_pickle = True    # will automatically store the parsed files as pickle - should speed up the load, but unnecessarily uses the disk space
fast_run = True                 # will skip the least prominent parts


# def get_traces():
#     global traces
#     return traces

def set_batch_run(do_batch_run):
    global batch_run
    batch_run = do_batch_run


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


def set_allow_force_merge(do_allow_force_merge):
    global allow_force_merge
    allow_force_merge = do_allow_force_merge


def set_guided(do_guided):
    global guided
    guided = do_guided


def set_just_annotate(do_just_annotate):
    global just_annotate
    just_annotate = do_just_annotate


def set_just_align(do_just_align):
    global just_align
    just_align = do_just_align


def set_force_new_video(do_force_new_video):
    global force_new_video
    force_new_video = do_force_new_video


global real_whole_frame_range
global whole_frame_range

global curr_csv_file_path


def set_curr_csv_file_path(file_path):
    global curr_csv_file_path
    curr_csv_file_path = file_path


def get_curr_csv_file_path():
    global curr_csv_file_path
    return curr_csv_file_path


def analyse(csv_file_path, population_size, swaps=False, has_tracked_video=False, is_first_run=None):
    """ Runs the whole file analysis.

    :arg csv_file_path: (str): path to csv file
    :arg population_size: (int): expected number of agents
    :arg swaps: (list of int): list of frame number of swaps to auto-pass
    :arg has_tracked_video: (bool): flag whether a video with tracking is available
    :arg is_first_run: (bool): iff True, all guided mechanics are hidden, csv is stored in this folder
    ##:arg force_new_video: (bool): iff True, a new video will be created, even a video with the same amount of traces is there
    """
    global just_annotate
    global just_align
    global traces
    global video_file
    global video_params
    global deleted_traces
    deleted_traces = {}

    set_curr_csv_file_path(csv_file_path)

    if just_annotate:
        print(colored(f"Commencing just annotate: {csv_file_path}", "magenta"))
    elif just_align:
        print(colored(f"Commencing just align: {csv_file_path}", "magenta"))
    elif is_first_run is True:
        print(colored(f"Commencing first run: {csv_file_path}", "magenta"))
    elif is_first_run is False:
        print(colored(f"Commencing second run: {csv_file_path}", "magenta"))
    else:
        print(colored(f"Commencing analyse: {csv_file_path}", "magenta"))

    global force_new_video
    global guided

    #################
    # Set run setting
    #################
    if is_first_run is True:
        set_silent(True)
        set_debug(False)
        set_show_plots(False)
        set_show_all_plots(False)
        set_rerun(False)
        set_guided(False)
        traces_file = str(os.path.join(os.path.dirname(csv_file_path), "parsed", os.path.basename(csv_file_path).replace(".csv", ".p")))
    elif is_first_run is False:
        traces_file = str(os.path.join(os.path.dirname(csv_file_path), "after_first_run", str(hash_config()), os.path.basename(csv_file_path).replace(".csv", ".p")))
        set_show_all_plots(False)
        set_batch_run(False)
        set_guided(True)
    else:
        pass

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

    set_rerun(True)
    # set_silent(True)
    # set_debug(True)

    #################
    # Internal params
    #################
    counts = []
    removed_short_traces = []
    removed_full_traces = []
    original_population_size = population_size
    overlap_dictionary = None

    ############
    # I/O stuff
    ############
    video_file, output_video_file = get_video_path(csv_file_path)
    has_video = True if output_video_file else False
    # print(output_video_file)

    if not just_annotate:
        #########################
        # LOAD PICKLE / PARSE CSV
        #########################
        if is_first_run is False:
            traces = load_traces(traces_file)
        ## First run and the pickled file already exists, we can skip this
        elif is_first_run is True and pickled_exist(csv_file_path, is_first_run=is_first_run):
            print(colored("This file already has saved pickled file, hence was successfully run", "green"))
            return
        else:
            try:
                ## call the file as this is the file calling it
                with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), csv_file_path), newline='') as csv_file:
                    #################
                    # Check whether this is new setting
                    #################
                    if not rerun:
                        if not is_new_config(file_name=csv_file_path, is_guided=guided, is_force_merge_allowed=allow_force_merge, video_available=has_tracked_video, is_first_run=is_first_run):
                            return
                    # Check whether this csv was already parsed, used the parsed file, if yes
                    if save_parsed_as_pickle and pickled_exist(csv_file_path, parsed=True):
                        traces = load_traces(traces_file)
                    else:
                        # parse traces from csv file
                        scraped_traces = parse_traces(csv_file)

                        # Store traces as list of Traces
                        traces = []
                        for index, trace in enumerate(scraped_traces.keys()):
                            # print(trace)
                            # print(scraped_traces[trace])
                            traces.append(Trace(scraped_traces[trace], index))

                        # Save parsed traces
                        if save_parsed_as_pickle:
                            pickle_traces(traces, csv_file_path, silent=silent, debug=debug, just_parsed=True)

            except FileNotFoundError:
                print(colored(f"File not found!", "magenta"))
                return

        # Storing the number of loaded traces
        counts.append(len(traces) + len(removed_full_traces))

        #########################
        ### AUXILIARY COMPUTATION
        #########################
        ## FRAME RANGE
        # obtain the frame range of the video
        global real_whole_frame_range
        real_whole_frame_range = compute_whole_frame_range(traces)
        # compute frame range margins for visualisation
        global whole_frame_range
        whole_frame_range = get_video_whole_frame_range(traces)

        ## OBTAIN VIDEO PARAMETERS
        # VECT - to move the locations according the cropping the video
        # trace_offset - number of first frames of the video to skip
        crop_offset, trim_offset = parse_video_info(video_file, traces, csv_file_path)
        video_params = [trim_offset, crop_offset] if crop_offset is not None else True
        # video_params = [crop_offset, trim_offset] if crop_offset is not None else [0, [0, 0]]

        if just_align:
            return

        ####################################
        # DELETE TRACES FROM SAVED DECISIONS
        ####################################
        traces = delete_traces_from_saved_decisions(traces, debug=debug)

        # fix_decisions()
        traces = smoothen_traces_from_saved_decisions(traces, debug=debug)

        #################
        ## SHOW THE VIDEO
        #################
        # simple show
        # show_video(input_video=video_file, traces=(), frame_range=(), wait=True, points=(), video_params=True)
        # show slower
        # show_video(input_video=video_file, traces=(), frame_range=(), video_speed=0.1, wait=True, points=(), video_params=True)
        # show from given frame
        # show_video(input_video=video_file, frame_range=[8000, 8500], wait=True, video_params=True)
        # show alignment to the original video
        ## TODO uncomment to show the original video with original tracking
        # show_video(input_video=video_file, traces=traces, frame_range=(), wait=True, points=(), video_params=video_params, fix_x_first_colors=2)

        #########################
        ### SINGLE TRACE ANALYSIS
        #########################
        if show_all_plots:
            # scatter_detection(traces, from_to_frame=[0, 2000], subtitle="Initial.")
            # show_plot_locations(traces, from_to_frame=[0, 1800], subtitle="Initial.")
            scatter_detection(traces, subtitle="Initial.")
            show_plot_locations(traces, subtitle="Initial.")

        ##################################
        # FIND TRACES OUTSIDE OF THE ARENA
        ##################################
        ## BEE SPECIFIC
        # TODO set guided value to guides
        check_inside_of_arena(traces, csv_file_path, guided=False, silent=silent, debug=debug)

        # Storing the number of traces inside of arena
        counts.append(len(traces) + len(removed_full_traces))

        # TODO uncomment the following
        # if show_all_plots:
        #     show_plot_locations(traces, subtitle="Traces outside of arena gone.")
        #     scatter_detection(traces, subtitle="Traces outside of arena gone.")

        #####################################################################
        # FIND TRACES OF ZERO LENGTH and SHORT FRAME RANGE TRACES, TRACE INFO
        #####################################################################
        traces, removed_short_traces = single_trace_checker(traces, min_trace_range_len=get_min_trace_len(), vicinity=get_vicinity_of_short_traces(), silent=silent, debug=debug)
        counts.append(len(traces) + len(removed_full_traces))
        # TODO uncomment the following
        # if show_all_plots:
        #     scatter_detection(traces, subtitle="After deleting traces with zero len in xy.")

        ############################
        # TRACK JUMPS BACK AND FORTH
        ############################
        start_time = time()
        print(colored(f"TRACE JUMP BACK AND FORTH CHECKER", "blue"))
        number_of_jump_detected = 0
        for index, trace in enumerate(traces):
            # TODO set guided value back to guided
            number_of_jump_detected = number_of_jump_detected + track_jump_back_and_forth(trace, index, guided=False, show_plots=True, silent=silent, debug=debug)
        print(colored(f"We have found and fixed {number_of_jump_detected} jumps. "
                      f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
        # if show_all_plots:
        #     scatter_detection(traces, subtitle="After dealing with fake jumps there and back.")
        # Storing the number of jumps detected
        counts.append(number_of_jump_detected)

        # TODO uncomment the following lines to show selected trace
        # if population_size > 1:
        #     ## CHOSEN TRACE SHOW - choose i, index of trace
        #     i = 0
        #     traces[i].show_trace_in_xy()

        ## CROSS-TRACE ANALYSIS
        cross_trace_analyse(traces, silent=silent, debug=debug)

        ############################
        ### MULTIPLE TRACES ANALYSIS
        ############################

        #############################
        # CHECK FOR SWAPPING THE BEES
        #############################
        # TODO set guided value to guides
        number_of_swaps = track_swapping_loop(traces, guided=False, silent=silent, debug=debug)
        # Storing the number of swaps done
        counts.append(number_of_swaps)

        ## TODO uncomment the following to show plot of all traces
        # ## ALL TRACES SHOW
        # if show_all_plots:
        #     show_plot_locations(traces, subtitle="After swapping.")
        #     scatter_detection(traces, subtitle="After swapping.")

        ##################################################################
        # TRIM REDUNDANT OVERLAPPING TRACES AND PUT GAPING TRACES TOGETHER
        ##################################################################
        ## TODO uncomment the following if you want to see the plot
        # if show_all_plots:
        #     show_plot_locations(traces, subtitle="before TRIM REDUNDANT OVERLAPPING TRACES AND PUT GAPING TRACES TOGETHER")

        before_number_of_traces = len(traces)
        after_number_of_traces = 0
        while (not before_number_of_traces == after_number_of_traces) and (len(traces) > population_size):
            before_number_of_traces = len(traces)
            traces, ids_of_traces_to_be_deleted = trim_out_additional_agents_over_long_traces_by_partition_with_build_fallback(traces, population_size, silent=silent, debug=debug)

            # show_video(input_video=video_file, traces=traces, frame_range=(9530, 9989), wait=True, points=(),
            #            video_params=video_params, fix_x_first_colors=2)

            # if before_number_of_traces != len(traces):
            # with open("../auxiliary/first_count_of_trimming.txt", "a") as file:
            #     file.write(f"{csv_file_path}: {before_number_of_traces}, {len(traces)} \n")
            if show_all_plots:
                scatter_detection(traces, subtitle="After trimming redundant overlapping traces.")
            traces = put_gaping_traces_together(traces, population_size, allow_force_merge=allow_force_merge, guided=guided, silent=silent, debug=debug)
            if show_all_plots:
                scatter_detection(traces, subtitle="After putting gaping traces together.")
            after_number_of_traces = len(traces)

            # show_video(input_video=video_file, traces=traces, frame_range=(9530, 9989), wait=True, points=(),
            #            video_params=video_params, fix_x_first_colors=2)

        # Storing the number of traces after TRIM REDUNDANT OVERLAPPING TRACES AND PUT GAPING TRACES TOGETHER
        counts.append(len(traces) + len(removed_full_traces))
        if not silent:
            print(colored(f"After trimming overlapping redundant traces and putting gaping traces together there are {len(traces)} left:", "yellow"))
            for index, trace in enumerate(traces):
                print(f"trace {trace.trace_id} of range {trace.frame_range} and length {trace.frame_range_len}")
            print()

        ## ALL TRACES SHOW
        if show_all_plots:
            # scatter_detection(traces, whole_frame_range)
            show_gaps(traces, silent=silent, debug=debug, subtitle="After Cross analysis phase 1.")
            show_overlaps(traces, silent=silent, debug=debug, subtitle="After Cross analysis phase 1.")
            show_plot_locations(traces, subtitle="After Cross analysis phase 1.")
            # track_reappearance(traces, show=True)

        # set_show_plots(True)

        ###########################
        ## MERGE OVERLAPPING TRACES
        ###########################
        # run until no traces are merged
        number_of_traces_before_merging_overlapping_traces = len(traces)
        before_before_number_of_traces = len(traces)
        after_after_number_of_traces = -9

        # Counting part
        do_count = False
        reset_this_file_counts()

        shift_folder = 'no_shift' if get_max_shift() == 0 or get_max_shift() is False else f'shift_{get_max_shift()}'

        bees = "1"
        bees = "1to5"

        metric_logic = "both_and"

        algorithm = "by_build"
        algorithm = "by_build_brutto"
        # algorithm = "by_partition"
        algorithm = "mixed"

        single_run_filename = f"../auxiliary/{algorithm}/{metric_logic}/{shift_folder}/single_run_overlaps_count_{bees}.txt"
        filename = f"../auxiliary/{algorithm}/{metric_logic}/{shift_folder}/all_overlaps_count_{bees}.txt"
        cumulative_filename = f"../auxiliary/{algorithm}/{metric_logic}/{shift_folder}/cumulative_all_overlaps_count_{bees}.txt"

        # with open(filename, "a") as file:
        #     file.write(f"{csv_file_path} all_overlaps_count; get_all_seen_overlaps; all_allowed_overlaps_count; all_seen_overlaps_deleted\n")

        guided = True

        # todo UNCOMMENT THIS AFTER counts done
        if algorithm == "mixed":
            a, b = merge_alone_overlapping_traces_by_partition(traces, shift=get_max_shift(), guided=guided, silent=silent, debug=debug, do_count=do_count)
            trace_indices_to_merge, ids_of_traces_to_be_merged = a, b
            if do_count:
                update_this_file_counts()

        is_first_call = True
        ## TODO delete this return
        # return

        while before_before_number_of_traces != after_after_number_of_traces:
            before_before_number_of_traces = len(traces)
            ## MERGE OVERLAPPING PAIRS
            before_number_of_traces = len(traces)
            after_number_of_traces = -9
            while before_number_of_traces != after_number_of_traces and len(traces) >= 2:
                before_number_of_traces = len(traces)
                if algorithm == "by_partition":
                    trace_indices_to_merge, ids_of_traces_to_be_merged = merge_alone_overlapping_traces_by_partition(traces, shift=get_max_shift(), guided=guided, silent=silent, debug=debug, do_count=do_count)

                if algorithm == "by_build":
                    merge_alone_overlapping_traces(traces, shift=get_max_shift(), allow_force_merge=allow_force_merge, guided=guided,
                                                   silent=silent, debug=debug, show=show_all_plots,
                                                   do_count=do_count, is_first_call=is_first_call)
                if algorithm == "by_build_brutto" or algorithm == "mixed":
                    merge_overlapping_traces_brutto(traces, shift=get_max_shift(), allow_force_merge=allow_force_merge, guided=guided,
                                                    silent=silent, debug=debug, show=show_all_plots, do_count="is_first" if is_first_run else do_count,
                                                    is_first_call=is_first_call, alg=algorithm)
                if is_first_call and do_count:
                    is_first_call = False
                    if algorithm == "by_partition":
                        set_this_file_overlaps_count(get_single_run_seen_overlaps())
                    with open(single_run_filename, "a") as file:
                        file.write(print_single_call() + f" {before_number_of_traces} -> {len(traces)}\n")

                if do_count:
                    update_this_file_counts()

                after_number_of_traces = len(traces)
                # return
            # return
            ## MERGE OVERLAPPING TRIPLETS, video-guided trace deleting
            before_number_of_traces = len(traces)
            after_number_of_traces = -9
            while before_number_of_traces != after_number_of_traces and len(traces) >= 3:
                before_number_of_traces = len(traces)

                # merge_triplets_by_partition(traces, shift=get_max_shift(), silent=silent, debug=debug, do_count=False,
                #                             input_video=video_file, video_params=video_params)
                # with open(f"../auxiliary/triplets/partition/numbers_of_merged_in_a_call.txt", "a") as file:
                #     if before_number_of_traces - len(traces) > 0:
                #         file.write(f"{csv_file_path} {before_number_of_traces - len(traces)}\n")

                merge_overlapping_triplets_brutto(traces, shift=get_max_shift(), guided=guided, input_video=video_file,
                                                  silent=silent, debug=debug, show=show_all_plots, video_params=video_params)
                # with open(f"../auxiliary/triplets/brutto/numbers_of_merged_in_a_call.txt", "a") as file:
                #     if before_number_of_traces - len(traces) > 0:
                #         file.write(f"{csv_file_path} {before_number_of_traces - len(traces)}\n")

                # merge_overlapping_triplets_of_traces(traces, shift=get_max_shift(), guided=guided,
                #                                      input_video=video_file, silent=silent, debug=debug, show=show_plots,
                #                                      show_all_plots=show_all_plots, video_params=video_params)
                # with open(f"../auxiliary/triplets/build/numbers_of_merged_in_a_call.txt", "a") as file:
                #     if before_number_of_traces - len(traces) > 0:
                #         file.write(f"{csv_file_path} {before_number_of_traces - len(traces)}\n")

                after_number_of_traces = len(traces)
            before_number_of_traces = len(traces)
            if len(traces) > population_size:
                traces, ids_of_traces_to_be_deleted = trim_out_additional_agents_over_long_traces_by_partition_with_build_fallback(traces, population_size, silent=silent, debug=debug)

            # if before_number_of_traces != len(traces):
            # with open("../auxiliary/second_count_of_trimming.txt", "a") as file:
            #     file.write(f"{csv_file_path}: {before_number_of_traces}, {len(traces)} \n")

            ## RECOLLECT NUMBER OF TRACES
            after_after_number_of_traces = len(traces)

        if do_count:
            if is_first_call:
                with open(single_run_filename, "a") as file:
                    file.write(print_single_call() + f" {before_number_of_traces} -> {len(traces)}\n")

            update_cumulative_counts()
            with open(filename, "a") as file:
                file.write(print_this_file()+"\n")
            with open(cumulative_filename, "a") as file:
                file.write(print_cumulative() + f"; {number_of_traces_before_merging_overlapping_traces} -> {len(traces)}" + "\n")

        # QA of `merge_alone_overlapping_traces`
        if len(traces) >= 2:
            if not silent:
                print(colored(f"Pairs of overlapping traces after merging overlapping traces: {dictionary_of_m_overlaps_of_n_intervals(2, list(map(lambda x: x.frame_range, traces)), skip_whole_in=False)}", "yellow"))
        else:
            pass
            # show_plot_locations(traces)

        if not silent:
            print(colored(f"After merging overlapping traces together there are {len(traces)} left:", "yellow"))
            for index, trace in enumerate(traces):
                print(f"trace {trace.trace_id} of range {trace.frame_range} and length {trace.frame_range_len}")
            print()

        # set_show_plots(True)
        # scatter_detection(traces, subtitle="After merging overlapping traces.")

        # Storing the number of traces after MERGE OVERLAPPING TRACES and OVERLAPPING TRIPLETS
        counts.append(len(traces) + len(removed_full_traces))

        ############################
        ## REMOVE TRACES OF FULL LEN
        ############################
        if len(traces) > 1:
            traces, removed_full_traces, new_population_size = remove_full_traces(traces, removed_full_traces, population_size)
        else:
            new_population_size = population_size

        # if show_all_plots:
        #     scatter_detection(traces, subtitle="After merging overlapping traces.")

        if not fast_run:
            print("SECOND Gaping traces analysis")
            before_second_gaping_number_of_traces = len(traces)

            before_number_of_traces = len(traces)
            after_number_of_traces = 0
            while (not before_number_of_traces == after_number_of_traces) and (len(traces) > population_size):
                before_number_of_traces = len(traces)
                traces, ids_of_traces_to_be_deleted = trim_out_additional_agents_over_long_traces_by_partition_with_build_fallback(
                    traces, population_size, silent=silent, debug=debug)

                # if before_number_of_traces != len(traces):
                # with open("../auxiliary/first_count_of_trimming.txt", "a") as file:
                #     file.write(f"{csv_file_path}: {before_number_of_traces}, {len(traces)} \n")
                if show_all_plots:
                    scatter_detection(traces, subtitle="After trimming redundant overlapping traces.")
                traces = put_gaping_traces_together(traces, population_size, allow_force_merge=allow_force_merge,
                                                    guided=guided, silent=silent, debug=debug)
                if show_all_plots:
                    scatter_detection(traces, subtitle="After putting gaping traces together.")
                after_number_of_traces = len(traces)

            ## WRITE TRACES COUNT AFTER THIS SECOND LOOP
            # if before_second_gaping_number_of_traces > len(traces):
            #     # single_run_filename = f"../auxiliary/second_gaping_single_run_overlaps_count_{bees}.txt"
            #     single_run_filename = f"../auxiliary/second_gaping_single_run_only_gaps_count_{bees}.txt"
            #     with open(single_run_filename, "a") as file:
            #         file.write(f"{csv_file_path}; {before_second_gaping_number_of_traces} -> {len(traces)}\n")

            #
            # # Storing the number of traces after second TRIM REDUNDANT OVERLAPPING TRACES AND PUT GAPING TRACES TOGETHER
            # counts.append(len(traces) + len(removed_traces))

        ##############
        ## FULL GUIDED
        ##############
        if len(traces)+len(removed_full_traces) > original_population_size and guided:
            full_guided(traces, input_video=video_file, show=show_plots, silent=silent, debug=debug, video_params=video_params, has_tracked_video=has_tracked_video)

        ## VISUALISATIONS
        if show_all_plots:
            track_reappearance(traces, show=True)
            scatter_detection(traces, subtitle="Final.")
            show_overlaps(traces, subtitle="Final.", silent=silent, debug=debug)
            show_gaps(traces, subtitle="Final.", silent=silent, debug=debug)
            show_plot_locations(traces, subtitle="Final.")

        ## OBTAIN ALL FINAL TRACES
        all_final_traces = removed_full_traces
        all_final_traces.extend(traces)
        print(colored(f"ANALYSIS FINISHED. There are {len(all_final_traces)} traces left.", "green"))

        ## SAVE RESULTS (TABLE)
        is_new = save_current_result(counts, file_name=csv_file_path, population_size=original_population_size, is_first_run=is_first_run,
                                     is_guided=guided, is_force_merge_allowed=allow_force_merge, video_available=has_tracked_video, silent=silent, debug=debug)

        # TODO delete the following
        if is_first_run:
            pickle_traces(all_final_traces, csv_file_path, silent=silent, debug=debug, is_first_run=is_first_run)
        if not is_first_run:
            print(f"gonna pickle traces {csv_file_path}")
            pickle_traces(all_final_traces, csv_file_path, silent=silent, debug=debug, is_first_run=is_first_run)

        if is_new:
            convert_results_from_json_to_csv(silent=silent, debug=debug, is_first_run=is_first_run)
            if not is_first_run:
                save_traces_as_csv(all_final_traces, os.path.basename(csv_file_path), silent=silent, debug=debug, is_first_run=is_first_run)
            pickle_traces(all_final_traces, csv_file_path, silent=silent, debug=debug, is_first_run=is_first_run)
    else:
        # Just_annotate
        all_final_traces = load_result_traces(csv_file_path)
        traces = all_final_traces
        removed_full_traces = traces
        crop_offset, trim_offset = parse_video_info(video_file, traces, csv_file_path)

    # ANNOTATE THE VIDEO
    # Check we have found the video
    if has_video and (is_first_run is None or just_annotate):
        ## update the output video_file_name
        spam = output_video_file.split(".m")
        updated_output_video_file = f"{spam[0]}_{str(len(all_final_traces))}_traces.m{spam[1]}"
        # print(updated_output_video_file)
        if has_tracked_video is True:
            # annotate_video(input_video, output_video,              traces, frame_range, speed=1, trace_offset=0, trim_offset=0, crop_offset=(0, 0), show=False)
            annotate_video(video_file, updated_output_video_file, all_final_traces, False, 1, min(traces[0].frame_range[0], removed_full_traces[0].frame_range[0]), force_new_video=force_new_video)
        else:
            # annotate_video(input_video, output_video,               traces, frame_range, speed=1, trace_offset=0, trim_offset=0, crop_offset=(0, 0), show=False)
            annotate_video(video_file, updated_output_video_file, all_final_traces, False, 1, min(traces[0].frame_range[0], removed_full_traces[0].frame_range[0]), trim_offset, crop_offset, force_new_video=force_new_video)
