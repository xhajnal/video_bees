import copy
import math
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from termcolor import colored

from config import *
from misc import has_overlap, is_before, merge_dictionary, take, get_overlap


class Trace:
    """ Single agent trace.

    Stores:
        frame_range (tuple): a pair frame numbers, first and last
        frames_list (list): list of all frames
        frame_range_len (int): length of trace in frames (computable)
        trace_length (float): length of trace in x,y coordinates (computable)
        max_step_len (float): maximal length of a single step in x,y coordinates (computable)
        max_step_len_step_index (int): index of the longest step in x,y coordinates
        max_step_len_line (int): line of .csv file, where the longest step occurred
        max_step_len_frame_number (int): frame number, where the longest step occurred
        trace_lengths (dic): step length -> count of the steps of such length (computable)
        locations (list): list of pairs, locations in each frame
        gap_frames (list): list of frame_numbers of gap frames
        overlap_frames (list): list of frame_numbers of overlapping frames
    Computable:
        number_of_frames_tracked (int): number of frames with tracked location
    """

    def __init__(self, parsed_trace, trace_id, debug=False):
        """ Parses a single agent trace obtained from the loopy csv file.

        :arg parsed_trace: (dict): 'frame_number' -> [line_id, location [x,y]]
        :arg trace_id: (int): id of the trace
        :arg debug: (bool): if True extensive output is shown
        """
        self.trace_id = trace_id

        frames = sorted(list(map(int, parsed_trace.keys())))
        # print("frames", frames)

        self.frame_range = [frames[0], frames[-1]]
        # print(frame_range)
        self.frame_range_len = int(float(frames[-1]) - float(frames[0]))
        self.max_step_len = 0
        self.max_step_len_step_index = None
        self.max_step_len_line = None
        self.max_step_len_frame_number = None

        self.trace_lengths = dict()
        self.frames_list = []

        self.locations = []

        self.trace_length = 0

        self.gap_frames = []
        self.overlap_frames = []

        # Compute trace_length(s)
        for index, frame in enumerate(frames):
            self.frames_list.append(frame)
            if debug:
                print(parsed_trace[frame])
            self.locations.append(parsed_trace[frame][1])
            # print(trace[frames[index]])
            # print(trace[frames[index+1]])
            try:
                # print("index", index)
                # print("frames index ", frames[index])
                # print("traces frames index ", trace[str(frames[index])])
                # print("traces frames index, x,y part", trace[str(frames[index])][1])
                # print("map it to floats", list(map(float, (trace[str(frames[index])][1]))))
                step_len = math.dist(list(map(float, (parsed_trace[frames[index]][1]))),
                                     list(map(float, (parsed_trace[frames[index + 1]][1]))))
                approx_step_len = round(step_len, 6)
                if approx_step_len in self.trace_lengths.keys():  # count the number of lengths
                    self.trace_lengths[approx_step_len] = self.trace_lengths[approx_step_len] + 1
                else:
                    self.trace_lengths[approx_step_len] = 1
                if step_len > self.max_step_len:  # Set max step len
                    self.max_step_len = step_len
                    self.max_step_len_step_index = index
                    self.max_step_len_line = int(parsed_trace[frames[index]][0])
                    self.max_step_len_frame_number = frame
                self.trace_length = self.trace_length + step_len
            except IndexError as err:
                if not index == len(frames) - 1:
                    # print(index)
                    # print(len(frames))
                    # print(trace)
                    # print("Error:", str(err))
                    raise err

    def get_gap_locations(self):
        """ Returns a list of locations of gaps. """
        gap_locations = []
        for frame in self.gap_frames:
            index = self.frames_list.index(frame)
            gap_locations.append(self.locations[index])

        return gap_locations

    def get_overlap_locations(self):
        """ Returns a list of locations of overlaps. """
        overlap_locations = []
        for frame in self.overlap_frames:
            index = self.frames_list.index(frame)
            overlap_locations.append(self.locations[index])

        return overlap_locations

    def get_locations_from_frame_range(self, interval):
        """ For a given frame range it results locations of the given range."""
        start_index = self.frames_list.index(interval[0])
        end_index = self.frames_list.index(interval[1])
        return self.locations[start_index:end_index + 1]

    def get_number_of_frames_tracked(self):
        """ Returns number of tracked frames. """
        return len(self.frames_list) - len(self.gap_frames)

    def check_trace_consistency(self):
        """ Verifies the consistency of the trace."""
        assert self.frame_range[0] <= self.frame_range[1]

    def recalculate_trace_lengths(self, recalculate_length=True, recalculate_lengths=True, recalculate_max_step_len=True):
        """ Recalculates trace length(s) based on locations. """
        # reset values
        if recalculate_length:
            self.trace_length = 0

        if recalculate_lengths:
            self.trace_lengths = {}

        # save old values - recalculate_max_step_len
        old_max_step = self.max_step_len
        max_step_len = 0
        max_step_index = 0

        # iterate through locations
        for index, location in enumerate(self.locations):
            # skip first index
            if index == 0:
                continue

            step_len = math.dist(location, self.locations[index-1])
            if step_len > max_step_len:
                max_step_len = step_len
                max_step_index = index
            if recalculate_lengths:
                approx_step_len = round(step_len, 6)
                if approx_step_len in self.trace_lengths.keys():  # count the number of lengths
                    self.trace_lengths[approx_step_len] = self.trace_lengths[approx_step_len] + 1
                else:
                    self.trace_lengths[approx_step_len] = 1
            if recalculate_length:
                self.trace_length = self.trace_length + step_len
        if recalculate_max_step_len:
            if not old_max_step == max_step_len:
                self.max_step_len = max_step_len
                self.max_step_len_step_index = max_step_index - 1  # because it was step to this index
                self.max_step_len_line = None
                self.max_step_len_frame_number = self.frames_list[max_step_index - 1]

    def show_step_lengths_hist(self, bins=100):
        """ Histogram of lengths of a single step. """
        # # print(self.trace_lengths)
        # plt.bar(list(self.trace_lengths.keys()), self.trace_lengths.values(), color='g')
        # plt.xlabel('Step size')
        # plt.ylabel('Count of steps')
        # plt.title(f'Histogram of step lengths. Trace {self.trace_id}.')
        # plt.show()

        spam = []
        for length in self.trace_lengths.keys():
            spam.extend([length]*self.trace_lengths[length])
            # if self.trace_lengths[length] > 1:
            #     print(self.trace_lengths[length])

        # print("hello")
        # print(len(list(self.trace_lengths.keys())))
        # print(len(spam))
        # print(self.trace_lengths.values())

        plt.hist(spam, color='g', bins=bins)
        plt.xlabel('Step size')
        plt.ylabel('Count of steps')
        plt.title(f'Histogram of step lengths. Trace {self.trace_id}.')
        plt.show()

    def show_trace_in_xy(self, whole_frame_range, from_to_frame=False, where=False, show=True, subtitle="", silent=False, debug=False):
        """ Plots the trace in three plots, trace in x-axis and y-axis separately, time on horizontal axis in frame numbers.
            Last plot is the trace in x,y.

        :arg whole_frame_range: [int, int]: frame range of the whole video
        :arg from_to_frame: (list): if set, showing only frames in given range
        :arg where: (list): is set, a list of three plots [[fig1, ax1], [fig2, ax2], [fig3, ax3]] in format fig1, ax1 = plt.subplots()
        :arg show: (bool): if True the plots are shown
        :arg subtitle: (string): a string to show under title
        :arg silent: (bool) if True no output is shown
        :arg debug: (bool) if True extensive output is shown
        :returns: list of pairs [figure, axis] for each of three plots
        """
        if subtitle is False:
            subtitle = ""

        # set boundaries for from_to_frame
        if from_to_frame is not False:
            assert isinstance(from_to_frame, list)
            assert len(from_to_frame) == 2
            if not has_overlap(from_to_frame, self.frame_range):
                return

            # from_to_frame right is before this trace
            if self.frame_range[0] < from_to_frame[0]:
                from_index = self.frames_list.index(from_to_frame[0])
            else:
                from_index = 0

            # from_to_frame left is after this trace
            if from_to_frame[1] < self.frame_range[1]:
                try:
                    to_index = self.frames_list.index(from_to_frame[1])
                except ValueError as err:
                    print(self.frames_list)
                    print(self.frame_range)
                    print(from_to_frame[1] < self.frame_range[1])
                    raise err
            else:
                to_index = -1

        else:
            from_index = 0
            to_index = -1

        # load locations for x and y-axis respectively
        xs = list(map(lambda x: x[0], self.locations))
        ys = list(map(lambda x: x[1], self.locations))

        gap_locations = self.get_gap_locations()
        overlap_locations = self.get_overlap_locations()

        if self.gap_frames and debug:
            print("gap_frames", self.gap_frames)
            print("gap_locations", gap_locations)
            print("list(map(lambda x: x[0], overlap_locations))", list(map(lambda x: x[0], gap_locations)))

        ## MAKE AND SHOW PLOTS
        if where:
            assert isinstance(where, list)
            fig1 = where[0][0]
            ax1 = where[0][1]
        else:
            fig1, ax1 = plt.subplots()

        # ax1.scatter(self.frames_tracked, xs, alpha=0.5)
        ax1.plot(list(range(self.frame_range[0], self.frame_range[1]+1)), xs, alpha=0.5, linewidth=0.4*rcParams['lines.linewidth'])
        ax1.scatter(self.overlap_frames, list(map(lambda x: x[0], overlap_locations)), c="black")
        ax1.scatter(self.gap_frames, list(map(lambda x: x[0], gap_locations)), c="white", edgecolors="black")
        ax1.set_xlabel('Time')
        ax1.set_ylabel('x')
        
        if from_to_frame is not False:
            ax1.set_xlim(from_to_frame)
        else:
            ax1.set_xlim(whole_frame_range)

        if where:
            ax1.set_title(f'Traces in x-axis.'+ ("\n"+subtitle if subtitle else ""))
        else:
            ax1.set_title(f'Trace {self.trace_id} in x-axis.'+ ("\n"+subtitle if subtitle else ""))
        if show:
            fig1.show()

        if where:
            assert isinstance(where, list)
            fig2 = where[1][0]
            ax2 = where[1][1]
        else:
            fig2, ax2 = plt.subplots()

        # ax2.scatter(self.frames_tracked, ys, alpha=0.5)
        ax2.plot(list(range(self.frame_range[0], self.frame_range[1]+1)), ys, alpha=0.5, linewidth=0.4*rcParams['lines.linewidth'])
        ax2.scatter(self.overlap_frames, list(map(lambda x: x[1], overlap_locations)), c="black")
        ax2.scatter(self.gap_frames, list(map(lambda x: x[1], gap_locations)), c="white", edgecolors="black")
        ax2.set_xlabel('Time')
        ax2.set_ylabel('y')
        if from_to_frame is not False:
            ax2.set_xlim(from_to_frame)
        else:
            ax2.set_xlim(whole_frame_range)

        if where:
            ax2.set_title(f'Traces in y-axis.'+ ("\n"+subtitle if subtitle else ""))
        else:
            ax2.set_title(f'Trace {self.trace_id} in y-axis.'+ ("\n"+subtitle if subtitle else ""))
        if show:
            fig2.show()

        if where:
            assert isinstance(where, list)
            fig3 = where[2][0]
            ax3 = where[2][1]
        else:
            fig3, ax3 = plt.subplots()

        xs = list(map(lambda x: x[0], self.locations[from_index:to_index]))
        ys = list(map(lambda x: x[1], self.locations[from_index:to_index]))
        # ax3.scatter(xs, ys, alpha=0.5)
        ax3.plot(xs, ys, 'x-', markersize=0.1, alpha=0.5, linewidth=0.4*rcParams['lines.linewidth'])
        ax3.scatter(list(map(lambda x: x[0], overlap_locations)), list(map(lambda x: x[1], overlap_locations)), c="black")
        ax3.scatter(list(map(lambda x: x[0], gap_locations)), list(map(lambda x: x[1], gap_locations)), c="white", edgecolors="black")
        ax3.set_xlabel('x')
        ax3.set_ylabel('y')
        max_position = max([max(xs), max(xs)])

        ## TODO implement from_to_frame

        # if max_position < 800:
        if max_position < max([get_screen_size()[0][1], get_screen_size()[1][1]]):
            plt.xlim(get_screen_size()[0])
            plt.ylim(get_screen_size()[1])
        else:
            plt.xlim(max_position)
            plt.ylim(max_position)

        if where:
            ax3.set_title(f'Traces "phase" space.'+ ("\n"+subtitle if subtitle else ""))
        else:
            ax3.set_title(f'Trace {self.trace_id} "phase" space.'+ ("\n"+subtitle if subtitle else ""))
        if show:
            fig3.show()

        if show:
            plt.show()
        return [[fig1, ax1], [fig2, ax2], [fig3, ax3]]

    def __str__(self):
        return f"trace_id:{self.trace_id} frame_range:{self.frame_range} " \
               f"number_of_frames_tracked:{self.get_number_of_frames_tracked()} " \
               f"trace_length:{round(self.trace_length,3)} " \
               f"max_step_len:{round(self.max_step_len,3)} max_step_len_step_index:{self.max_step_len_step_index} " \
               f"max_step_len_line:{self.max_step_len_line} max_step_len_frame_number:{self.max_step_len_frame_number} " \
               f"trace_lengths:{take(5, self.trace_lengths.items())}[ frames_list:{self.frames_list[:5]}... locations:{self.locations[:5]}... "


def merge_two_traces_with_gap(trace1: Trace, trace2: Trace, silent=False, debug=False):
    """ Puts two traces together.

    :arg trace1: (Trace): a Trace to be merged with the following trace
    :arg trace2: (Trace): a Trace to be merged with the following trace
    :arg silent (bool) if True no output is shown
    :arg debug (bool) if True extensive output is shown

    :returns: trace1: (Trace): merged trace of two given traces
    """
    ## CHECK
    assert isinstance(trace1, Trace)
    assert isinstance(trace2, Trace)

    if debug:
        print("trace1.trace_id", trace1.trace_id)
        print("trace2.trace_id", trace2.trace_id)

    if has_overlap(trace1.frame_range, trace2.frame_range):
        raise Exception("The two traces have an overlap. We cannot merge them. Try other merge function.")

    ## MERGE
    # set trace id
    trace1.trace_id = min(trace1.trace_id, trace2.trace_id)

    # swapping traces if trace2 is before trace1
    if is_before(trace2.frame_range, trace1.frame_range):
        spam = trace2
        trace2 = trace1
        trace1 = spam
        del spam

    ## Calculate the gap
    # gap range is the range of the gap not including the border points of traces
    gap_range = [trace1.frame_range[-1]+1, trace2.frame_range[0]-1]

    # gap size in frames
    frame_gap_size = trace2.frames_list[0] - trace1.frames_list[-1] - 1
    # gap size in xy (last and first point)
    merge_step = math.dist(trace1.locations[-1], trace2.locations[0])

    # trace len is sum of both plus the gap
    trace1.trace_length = trace1.trace_length + merge_step + trace2.trace_length

    # list of frame, not to be confused with number_of_frames_tracked is list of all frames including the gap
    for frame in range(gap_range[0], gap_range[1]+1):
        trace1.frames_list.append(frame)
        # add the gap to the gap frames
        trace1.gap_frames.append(frame)
    trace1.frames_list.extend(trace2.frames_list)

    # Based on the gap size
    if frame_gap_size <= get_max_trace_gap_to_interpolate_distance():
        # set a point of location of the gap as linear interpolation of two bordering points
        if debug:
            print("frame_gap_size", frame_gap_size)
            print(trace1.locations[-1], trace2.locations[0])
        in_middle_points = np.linspace(trace1.locations[-1], trace2.locations[0], num=frame_gap_size+1, endpoint=False)
        # in_middle_points = list(map(lambda x: [int(x[0]), int(x[1])], in_middle_points))
        # cutting the first point and changing to float
        in_middle_points = list(map(lambda x: [float(x[0]), float(x[1])], in_middle_points))[1:]
        trace1.locations.extend(in_middle_points)

    else:
        in_middle_point = [-sys.maxsize, -sys.maxsize]

        # fill the gap location as the chosen point
        for frame in range(frame_gap_size):
            trace1.locations.append(in_middle_point)

    ## DEPRICATED
    # set a point of location of the gap as a point in the middle between the border points
    # in_middle_point = [abs(trace2.locations[0][0] + trace1.locations[-1][0])/2, abs(trace2.locations[0][1] + trace1.locations[-1][1])/2]
    # # fill the gap location as the chosen point
    # for frame in range(frame_gap_size - 1):
    #     trace1.locations.append(in_middle_point)

    # extend the locations with locations of trace2
    trace1.locations.extend(trace2.locations)

    # frame range is simply leftmost and rightmost frame of the two traces, remember they are sorted
    trace1.frame_range = [trace1.frame_range[0], trace2.frame_range[1]]

    # frame_range_len is the len from new boundary to another
    trace1.frame_range_len = int(float(trace1.frame_range[-1]) - float(trace1.frame_range[0]))

    # print("trace1.max_step_len", trace1.max_step_len)
    # print("trace2.max_step_len", trace2.max_step_len)

    if trace1.max_step_len < trace2.max_step_len:
        trace1.max_step_len_step_index = trace2.max_step_len_step_index
        trace1.max_step_len_line = trace2.max_step_len_line
        trace1.max_step_len_frame_number = trace2.max_step_len_frame_number

    trace1.max_step_len = max(trace1.max_step_len, trace2.max_step_len)

    # TODO fix this by adding the the steps of the gap
    trace1.trace_lengths = merge_dictionary(trace1.trace_lengths, trace2.trace_lengths)

    # print(trace1.trace_lengths)
    if round(merge_step, 6) in trace1.trace_lengths.keys():
        trace1.trace_lengths[round(merge_step, 6)] = trace1.trace_lengths[round(merge_step, 6)] + 1
    else:
        trace1.trace_lengths[round(merge_step, 6)] = 1
    # print(trace1.trace_lengths)

    return trace1


def merge_two_overlapping_traces(trace1: Trace, trace2: Trace, silent=False, debug=False):
    """ Puts two overlapping traces together.

    :arg trace1: (Trace): a Trace to be merged with the following trace
    :arg trace2: (Trace): a Trace to be merged with the following trace
    :arg silent (bool) if True no output is shown
    :arg debug (bool) if True extensive output is shown

    :returns: trace1: (Trace): merged trace of two given traces
    """
    # CHECK validity
    assert isinstance(trace1, Trace)
    assert isinstance(trace2, Trace)
    if not has_overlap(trace1.frame_range, trace2.frame_range):
        raise Exception("The two traces have no overlap. Try using function 'merge_two_traces' instead.")
    else:
        overlap = get_overlap(trace1.frame_range, trace2.frame_range)

    # Decide whether to keep overlap of trace1 or trace2
    index1_overlap_start = trace1.frames_list.index(overlap[0])
    index2_overlap_end = trace2.frames_list.index(overlap[1])

    if debug:
        print("index1_overlap_start", index1_overlap_start)
        print("index2_overlap_end", index2_overlap_end)

    dist1 = math.dist(trace1.locations[index1_overlap_start - 1], trace2.locations[0])
    dist2 = math.dist(trace1.locations[-1], trace2.locations[index2_overlap_end + 1])

    if debug:
        print("dist1", dist1)
        print("dist2", dist2)

    trace1.frame_range = [trace1.frame_range[0], trace2.frame_range[1]]

    if dist1 < dist2:
        ## Cutting trace1
        if not silent:
            print(colored(f"Cutting first trace of the pair of id {trace1.trace_id}.", "yellow"))
        # trim
        trace1.frames_list = trace1.frames_list[:index1_overlap_start]
        trace1.locations = trace1.locations[:index1_overlap_start]
    else:
        ## Cutting trace2
        # trim
        if not silent:
            print(colored(f"Cutting second trace of the pair of id {trace2.trace_id}.", "yellow"))
        trace2.frames_list = trace2.frames_list[index2_overlap_end + 1:]
        trace2.locations = trace2.locations[index2_overlap_end + 1:]

    # Append frame list and locations
    trace1.frames_list.extend(trace2.frames_list)
    trace1.locations.extend(trace2.locations)

    # recalculate attributes
    trace1.frame_range_len = len(trace1.frames_list)

    if debug:
        print("trace1.frame_range", trace1.frame_range)
        # print("trace1.frames_tracked", trace1.frames_tracked)
        print("length trace1.frames_tracked", len(trace1.frames_list))
        # print("trace1.locations", trace1.locations)
        print("length trace1.locations", len(trace1.locations))

    # Add overlapping frames to the trace
    for frame in range(overlap[0], overlap[1]+1):
        trace1.overlap_frames.append(frame)
    trace1.overlap_frames = list(sorted(trace1.overlap_frames))

    # compute max step attributes
    trace1.recalculate_trace_lengths(recalculate_length=True, recalculate_lengths=True, recalculate_max_step_len=True)

    return trace1
