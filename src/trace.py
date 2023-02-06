import math
import matplotlib.pyplot as plt
from matplotlib import rcParams

from config import *
from fake import get_whole_frame_range
from misc import has_overlap, take


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
        is_done (bool): flag whether this trace has full length (computable using real_whole_range)
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
        self.is_done = False
        # print(frame_range)
        self.frame_range_len = int(float(frames[-1]) - float(frames[0])) + 1
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

    def get_gap_frame_range(self):
        ## TODO make more tests
        """ Returns the range of gaps."""
        if self.gap_frames:
            return (self.gap_frames[0], self.gap_frames[-1])
        else:
            return ()

    def get_gap_locations(self):
        ## TODO make more tests
        """ Returns a list of locations of gaps."""
        gap_locations = []
        for frame in self.gap_frames:
            index = self.frames_list.index(frame)
            gap_locations.append(self.locations[index])

        return gap_locations

    def get_overlap_frame_range(self):
        ## TODO make more tests
        """ Returns the range of overlaps."""
        if self.overlap_frames:
            return (self.overlap_frames[0], self.overlap_frames[-1])
        else:
            return ()

    def get_overlap_locations(self):
        ## TODO make more tests
        """ Returns a list of locations of overlaps."""
        overlap_locations = []
        for frame in self.overlap_frames:
            index = self.frames_list.index(frame)
            overlap_locations.append(self.locations[index])

        return overlap_locations

    def get_location_from_frame(self, frame_number):
        ## TODO make more tests
        """ For a given frame range it results locations of the given range."""
        start_index = self.frames_list.index(frame_number)
        return self.locations[start_index]

    def get_locations_from_frame_range(self, interval):
        ## TODO make more tests
        """ For a given frame range it results locations of the given range."""
        start_index = self.frames_list.index(interval[0])
        end_index = self.frames_list.index(interval[1])
        return self.locations[start_index:end_index + 1]

    def get_number_of_frames_tracked(self):
        ## TODO make more tests
        """ Returns number of tracked frames."""
        return len(self.frames_list) - len(self.gap_frames)

    def check_trace_consistency(self):
        ## TODO make more tests
        """ Verifies the consistency of the trace."""
        assert self.frame_range[0] <= self.frame_range[1]

    def check_whether_is_done(self, real_whole_frame_range):
        ## TODO make more tests
        """ Checks and stores whether this trace has its full length."""
        if self.frame_range == real_whole_frame_range:
            self.is_done = True
            return True
        else:
            self.is_done = False
            return False

    def recalculate_trace_lengths(self, recalculate_length=True, recalculate_lengths=True, recalculate_max_step_len=True):
        ## TODO make more tests
        """ Recalculates trace length(s) based on locations."""
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
        """ Histogram of lengths of a single step."""
        # # print(self.trace_lengths)
        # plt.bar(list(self.trace_lengths.keys()), self.trace_lengths.values(), color='g')
        # plt.xlabel('Step population_size')
        # plt.ylabel('Count of steps')
        # plt.title(f'Histogram of step lengths. Trace id {self.trace_id}.')
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
        plt.xlabel('Step population_size')
        plt.ylabel('Count of steps')
        plt.title(f'Histogram of step lengths. Trace id {self.trace_id}.')
        plt.show()

    def show_trace_in_xy(self, whole_frame_range=False, from_to_frame=False, where=False, show=True, subtitle="",
                         show_middle_point=False, silent=False, debug=False):
        """ Plots the trace in three plots, trace in x-axis and y-axis separately, time on horizontal axis in frame numbers.
            Last plot is the trace in x,y.

        :arg whole_frame_range: [int, int]: frame range of the whole video (with margins)
        :arg from_to_frame: (list): if set, showing only frames in given range
        :arg where: (list): is set, a list of three plots [[fig1, ax1], [fig2, ax2], [fig3, ax3]] in format fig1, ax1 = plt.subplots()
        :arg show: (bool): if True the plots are shown
        :arg subtitle: (string): a string to show under
        :arg show_middle_point: (bool): if True, a point in the middle of the trace is highlighted
        :arg silent: (bool) if True minimal output is shown
        :arg debug: (bool) if True extensive output is shown
        :returns: list of pairs [figure, axis] for each of three plots
        """
        # Obtained variables
        if whole_frame_range is False:
            whole_frame_range = get_whole_frame_range()

        if subtitle is False:
            subtitle = ""

        # print("self.gap_frames", self.gap_frames)
        # print("self.overlap_frames", self.overlap_frames)

        # set boundaries for from_to_frame
        if from_to_frame is not False:
            assert isinstance(from_to_frame, list) or isinstance(from_to_frame, tuple)
            assert len(from_to_frame) == 2
            if not has_overlap(from_to_frame, self.frame_range):
                return

            frame_range_len = from_to_frame[1] - from_to_frame[0]

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
                to_index = len(self.locations)

            ## GAPS
            # from_to_frame is either before or after gaps
            if self.gap_frames and has_overlap(from_to_frame, self.get_gap_frame_range()):
                if self.gap_frames[0] < from_to_frame[0]:
                    for index, gap_frame in enumerate(self.gap_frames):
                        if from_to_frame[0] > gap_frame:
                            from_gap_index = index
                            break
                else:
                    from_gap_index = 0

                if self.gap_frames and from_to_frame[1] < self.gap_frames[0]:
                    for index, gap_frame in enumerate(self.gap_frames):
                        to_gap_index = index
                        if gap_frame > from_to_frame[1]:
                            break
                else:
                    to_gap_index = len(self.gap_frames)
            else:
                from_gap_index = 0
                to_gap_index = 0

            ## OVERLAPS
            # from_to_frame is either before or after overlaps
            if self.overlap_frames and has_overlap(from_to_frame, self.get_overlap_frame_range()):
                if self.overlap_frames and self.overlap_frames[0] < from_to_frame[0]:
                    for index, overlap_frame in enumerate(self.overlap_frames):
                        if from_to_frame[0] > overlap_frame:
                            from_overlap_index = index
                            break
                else:
                    from_overlap_index = 0

                if self.overlap_frames and from_to_frame[1] < self.overlap_frames[0]:
                    for index, overlap_frame in enumerate(self.overlap_frames):
                        to_overlap_index = index
                        if overlap_frame > from_to_frame[1]:
                            break
                else:
                    to_overlap_index = len(self.overlap_frames)
            else:
                from_overlap_index = 0
                to_overlap_index = 0
        else:
            from_index = 0
            to_index = len(self.locations)

            from_gap_index = 0
            to_gap_index = len(self.gap_frames)

            from_overlap_index = 0
            to_overlap_index = len(self.overlap_frames)

        # print("self.gap_frames cut", self.gap_frames[from_gap_index:to_gap_index])
        # print("self.overlap_frames cut", self.overlap_frames[from_overlap_index:to_overlap_index])

        # load locations for x and y-axis respectively
        xs = list(map(lambda x: x[0], self.locations))
        ys = list(map(lambda x: x[1], self.locations))

        gap_locations = self.get_gap_locations()
        overlap_locations = self.get_overlap_locations()

        if self.gap_frames and debug:
            print("gap_frames", self.gap_frames)
            print("gap_locations", gap_locations)
            print("list(map(lambda x: x[0], overlap_locations))", list(map(lambda x: x[0], gap_locations)))

        if show_middle_point:
            if from_to_frame:
                middle_index = int(from_to_frame[0] + (from_to_frame[1] - from_to_frame[0])/2)
            else:
                middle_index = int(self.frame_range[0] + (self.frame_range[1] - self.frame_range[0])/2)
            x_middle_pos = self.locations[middle_index - self.frame_range[0]][0]
            y_middle_pos = self.locations[middle_index - self.frame_range[0]][1]

        ## MAKE AND SHOW PLOTS
        if where:
            assert isinstance(where, list)
            fig1 = where[0][0]
            ax1 = where[0][1]
        else:
            fig1, ax1 = plt.subplots()

        ## Set range
        if from_to_frame is not False:
            ax1.set_xlim(from_to_frame)
        else:
            ax1.set_xlim(whole_frame_range)

        # ax1.scatter(self.frames_tracked, xs, alpha=0.5)
        ax1.plot(list(range(self.frame_range[0], self.frame_range[1]+1)), xs, alpha=0.5, linewidth=0.4*rcParams['lines.linewidth'])
        if show_middle_point:
                ax1.scatter([middle_index], [x_middle_pos], c="magenta", s=3)
        ax1.scatter(self.overlap_frames[from_overlap_index: to_overlap_index], list(map(lambda x: x[0], overlap_locations))[from_overlap_index: to_overlap_index], c="black")
        ax1.scatter(self.gap_frames[from_gap_index: to_gap_index], list(map(lambda x: x[0], gap_locations))[from_gap_index: to_gap_index], c="white", edgecolors="black")
        ax1.set_xlabel('Time')
        ax1.set_ylabel('x')

        if where:
            ax1.set_title(f'Traces in x-axis.' + ("\n"+subtitle if subtitle else ""))
        else:
            ax1.set_title(f'Trace id {self.trace_id} in x-axis.' + ("\n"+subtitle if subtitle else ""))
        if show:
            fig1.show()

        if where:
            assert isinstance(where, list)
            fig2 = where[1][0]
            ax2 = where[1][1]
        else:
            fig2, ax2 = plt.subplots()

        ## Set range
        if from_to_frame is not False:
            ax2.set_xlim(from_to_frame)
        else:
            ax2.set_xlim(whole_frame_range)

        # ax2.scatter(self.frames_tracked, ys, alpha=0.5)
        ax2.set_ylabel('y')
        ax2.plot(list(range(self.frame_range[0], self.frame_range[1]+1)), ys, alpha=0.5, linewidth=0.4*rcParams['lines.linewidth'])
        if show_middle_point:
            ax2.scatter([middle_index], [y_middle_pos], c="magenta", s=3)
        ax2.scatter(self.overlap_frames[from_overlap_index: to_overlap_index], list(map(lambda x: x[1], overlap_locations))[from_overlap_index: to_overlap_index], c="black")
        ax2.scatter(self.gap_frames[from_gap_index: to_gap_index], list(map(lambda x: x[1], gap_locations))[from_gap_index: to_gap_index], c="white", edgecolors="black")
        ax2.set_xlabel('Time')

        ax2.invert_yaxis()

        if where:
            ax2.set_title(f'Traces in y-axis.' + ("\n"+subtitle if subtitle else ""))
        else:
            ax2.set_title(f'Trace id {self.trace_id} in y-axis.' + ("\n"+subtitle if subtitle else ""))
        if show:
            fig2.show()

        if where:
            assert isinstance(where, list)
            fig3 = where[2][0]
            ax3 = where[2][1]
        else:
            fig3, ax3 = plt.subplots()

        ax3.set_xlabel('x')
        ax3.set_ylabel('y')


        xs = list(map(lambda x: x[0], self.locations[from_index:to_index]))
        ys = list(map(lambda x: x[1], self.locations[from_index:to_index]))
        # ax3.scatter(xs, ys, alpha=0.5)
        plot3 = ax3.plot(xs, ys, 'x-', markersize=0.1, alpha=0.7, linewidth=0.4*rcParams['lines.linewidth'])
        if show_middle_point:
            ax3.scatter([x_middle_pos], [y_middle_pos], c="magenta", s=3)

        ax3.text(xs[0], ys[0], "A", fontsize=6, color=plot3[0].get_color())
        ax3.text(xs[-1], ys[-1], "B", fontsize=6, color=plot3[0].get_color())
        ax3.scatter(list(map(lambda x: x[0], overlap_locations))[from_overlap_index: to_overlap_index], list(map(lambda x: x[1], overlap_locations))[from_overlap_index: to_overlap_index], c="black")
        ax3.scatter(list(map(lambda x: x[0], gap_locations))[from_gap_index: to_gap_index], list(map(lambda x: x[1], gap_locations))[from_gap_index: to_gap_index], c="white", edgecolors="black")
        # ax3.plot(list(map(lambda x: x[0], self.locations)), list(map(lambda x: x[1], self.locations)), 'x-', markersize=0.1, alpha=0.3, linewidth=0.35*rcParams['lines.linewidth'])

        max_position = max([max(xs), max(xs)])

        ## TODO implement from_to_frame

        # if max_position < 800:
        if max_position < max([get_screen_size()[0][1], get_screen_size()[1][1]]):
            plt.xlim(get_screen_size()[0])
            plt.ylim(get_screen_size()[1])
        else:
            plt.xlim(max_position)
            plt.ylim(max_position)

        ax3.invert_yaxis()
        if where:
            ax3.set_title(f'Traces "phase" space.' + ("\n"+subtitle if subtitle else ""))
        else:
            ax3.set_title(f'Trace id {self.trace_id} "phase" space.' + ("\n"+subtitle if subtitle else ""))
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
