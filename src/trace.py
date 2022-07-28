import copy
import math
import matplotlib.pyplot as plt
from numpy import iterable

from misc import has_overlap, is_before, merge_dictionary, take


class Trace:
    """ Single agent trace.

        Stores:
        frame_range (tuple): a pair frame numbers, first and last
        number_of_frames (int): number of frames
        frame_range_len (int): length of trace in frames
        trace_lenn (float): length of trace in x,y coordinates
        max_step_len (float): maximal length of a single step in x,y coordinates
        max_step_len_step_index (int): index of the longest step in x,y coordinates
        max_step_len_line (int): line of .csv file, where the longest step occurred
        max_step_len_frame_number (int): frame number, where the longest step occurred
        trace_lengths (dic): step length -> count of the steps of such length
        frames_tracked (list): list of frames tracked
        locations (list): list of pairs, locations in each frame
    """

    def __init__(self, trace, trace_id, debug=False):
        """ Parses a single agent trace obtained from the loopy csv file.

        :arg trace (dict): 'frame_number' -> [line_id, location [x,y]]
        :arg id (int): id of the trace
        :arg debug (bool): if True extensive output is shown
        """
        self.trace_id = trace_id

        frames = sorted(list(map(int, trace.keys())))
        # print("frames", frames)

        self.number_of_frames = len(trace.keys())
        self.frame_range = (frames[0], frames[-1])
        # print(frame_range)
        self.frame_range_len = float(frames[-1]) - float(frames[0])
        self.max_step_len = 0
        self.max_step_len_step_index = None
        self.max_step_len_line = None
        self.max_step_len_frame_number = None

        self.trace_lengths = dict()
        self.frames_tracked = []

        self.locations = []

        self.trace_lenn = 0

        for index, frame in enumerate(frames):
            self.frames_tracked.append(frame)
            if debug:
                print(trace[frame])
            self.locations.append(trace[frame][1])
            # print(trace[frames[index]])
            # print(trace[frames[index+1]])
            try:
                # print("index", index)
                # print("frames index ", frames[index])
                # print("traces frames index ", trace[str(frames[index])])
                # print("traces frames index, x,y part", trace[str(frames[index])][1])
                # print("map it to floats", list(map(float, (trace[str(frames[index])][1]))))
                step_len = math.dist(list(map(float, (trace[frames[index]][1]))),
                                           list(map(float, (trace[frames[index + 1]][1]))))
                approx_step_len = round(step_len, 6)
                if approx_step_len in self.trace_lengths.keys():  ## count the number of lenghts
                    self.trace_lengths[approx_step_len] = self.trace_lengths[approx_step_len] + 1
                else:
                    self.trace_lengths[approx_step_len] = 1
                if step_len > self.max_step_len:  ## Set max step len
                    self.max_step_len = step_len
                    self.max_step_len_step_index = index
                    self.max_step_len_line = int(trace[frames[index]][0])
                    self.max_step_len_frame_number = frame
                self.trace_lenn = self.trace_lenn + step_len
            except IndexError as err:
                if not index == len(frames) - 1:
                    # print(index)
                    # print(len(frames))
                    # print(trace)
                    # print("Error:", str(err))
                    raise err

    def show_step_lenghts_hist(self, bins=100):
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

    def show_trace_in_xy(self, where=False):
        """ Plots the trace in three plots, trace in x axis and y axis separately, time on horizontal axis in frame numbers.
            Last plot is the trace in x,y.
        """
        xs = []
        ys = []
        for locaion in self.locations:
            xs.append(locaion[0])
            ys.append(locaion[1])

        ## MAKE AND SHOW PLOTS
        if where:
            assert isinstance(where, list)
            fig1 = where[0][0]
            ax1 = where[0][1]
        else:
            fig_size = (10, 5)
            fig1, ax1 = plt.subplots()

        ax1.scatter(self.frames_tracked, xs, alpha=0.5)
        ax1.set_xlabel('Time')
        ax1.set_xlabel('x')
        ax1.set_title(f'Trace in x axis.')
        fig1.show()

        if where:
            assert isinstance(where, list)
            fig2 = where[1][0]
            ax2 = where[1][1]
        else:
            fig_size = (10, 5)
            fig2, ax2 = plt.subplots()

        ax2.scatter(self.frames_tracked, xs, alpha=0.5)
        ax2.set_xlabel('Time')
        ax2.set_xlabel('x')
        ax2.set_title(f'Trace in x axis.')
        fig2.show()

        if where:
            assert isinstance(where, list)
            fig3 = where[2][0]
            ax3 = where[2][1]
        else:
            fig_size = (10, 5)
            fig3, ax3 = plt.subplots()

        ax3.scatter(xs, ys, alpha=0.5)
        ax3.set_xlabel('x')
        ax3.set_xlabel('y')
        ax3.set_title(f'Trace "phase" space.')
        fig3.show()

        return [[fig1, ax1], [fig2, ax2], [fig3, ax3]]

    def check_trace_consistency(self):
        """ Verifies the consistency of the trace"""
        assert self.frame_range[0] <= self.frame_range[1]

    def __str__(self):
        return f"trace_id:{self.trace_id} frame_range:{self.frame_range} number_of_frames:{self.number_of_frames} " \
               f" frame_range_len:{self.frame_range_len} trace_lenn:{self.trace_lenn} " \
               f"max_step_len:{self.max_step_len} max_step_len_step_index:{self.max_step_len_step_index} " \
               f"max_step_len_line:{self.max_step_len_line} max_step_len_frame_number:{self.max_step_len_frame_number} " \
               f"trace_lengths:{take(5, self.trace_lengths.items())}[ frames_tracked:{self.frames_tracked[:5]} locations:{self.locations[:5]} "


def merge_two_traces(trace1: Trace, trace2: Trace):
    """ Puts two traces together

    :arg trace1 (Trace) a Trace to be merged with the following trace
    :arg trace1 (Trace) a Trace to be merged with the following trace
    """
    ## CHECK
    assert isinstance(trace1, Trace)
    assert isinstance(trace2, Trace)
    if has_overlap(trace1.frame_range, trace2.frame_range):
        raise Exception("The two traces have an overlap. We cannot merge them.")

    ## MERGE
    trace1.trace_id = min(trace1.trace_id, trace2.trace_id)

    if is_before(trace1.frame_range, trace2.frame_range):
        merge_step = math.dist(trace1.locations[-1], trace2.locations[0])
        trace1.trace_lenn = trace1.trace_lenn + merge_step + trace2.trace_lenn

        trace1.frames_tracked.extend(trace2.frames_tracked)

        trace1.locations.extend(trace2.locations)

    else:
        merge_step = math.dist(trace2.locations[-1], trace1.locations[0])
        trace1.trace_lenn = trace2.trace_lenn + merge_step + trace1.trace_lenn

        spam = copy.copy(trace2.frames_tracked)
        spam.extend(trace1.frames_tracked)
        trace1.frames_tracked = spam

        spam = copy.copy(trace2.locations)
        spam.extend(trace1.locations)
        trace1.locations = spam

    trace1.frame_range = (min(trace1.frame_range[0], trace2.frame_range[0]), max(trace1.frame_range[1], trace2.frame_range[1]))
    trace1.number_of_frames = trace1.number_of_frames + trace2.number_of_frames
    if has_overlap(trace1.frame_range, trace2.frame_range):
        trace1.frame_range_len = trace1.frame_range[1] - trace1.frame_range[0]
    else:
        trace1.frame_range_len = trace1.frame_range_len + trace2.frame_range_len

    # print("trace1.max_step_len", trace1.max_step_len)
    # print("trace2.max_step_len", trace2.max_step_len)

    if trace1.max_step_len < trace2.max_step_len:
        trace1.max_step_len_step_index = trace2.max_step_len_step_index
        trace1.max_step_len_line = trace2.max_step_len_line
        trace1.max_step_len_frame_number = trace2.max_step_len_frame_number

    trace1.max_step_len = max(trace1.max_step_len, trace2.max_step_len)

    trace1.trace_lengths = merge_dictionary(trace1.trace_lengths, trace2.trace_lengths)

    # print(trace1.trace_lengths)
    if round(merge_step, 6) in trace1.trace_lengths.keys():
        trace1.trace_lengths[round(merge_step, 6)] = trace1.trace_lengths[round(merge_step, 6)] + 1
    else:
        trace1.trace_lengths[round(merge_step, 6)] = 1
    # print(trace1.trace_lengths)

    return trace1
