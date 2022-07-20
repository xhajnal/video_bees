import math
import matplotlib.pyplot as plt


class Trace:
    """ Single agent trace

        Stores:
        frame_range (tuple): a pair frame numbers, first and last
        number_of_frames (int): number of frames
        frame_range_len (int): length of trace in frames
        trace_lenn (float): length of trace in x,y
        max_step_len (float): maximal length of a single step in x,y
        max_step_len_step_index (int): index of the longest step in x,y
        max_step_len_line (int): line of .csv file, where the longest step occurred
        max_step_len_frame_number (int): frame number, where the longest step occurred
    """

    def __init__(self, trace, id):
        """ Parses a single agent trace obtained from the loopy csv file.

            :param trace: a single trace of traces
            :param id (int): id of the trace
        """
        self.id = id

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

        self.trace_lenghts = dict()
        self.times_tracked = []

        self.trace_lenn = 0
        for index, frame in enumerate(frames):
            self.times_tracked.append(frame)
            # print(trace[frames[index]])
            # print(trace[frames[index+1]])
            try:
                # print("index", index)
                # print("frames index ", frames[index])
                # print("traces frames index ", trace[str(frames[index])])
                # print("traces frames index, x,y part", trace[str(frames[index])][1])
                # print("map it to floats", list(map(float, (trace[str(frames[index])][1]))))
                step_len = math.dist(list(map(float, (trace[str(frames[index])][1]))),
                                     list(map(float, (trace[str(frames[index + 1])][1]))))
                if step_len in self.trace_lenghts.keys():  ## count the number of lenghts
                    self.trace_lenghts[step_len] = self.trace_lenghts[step_len] + 1
                else:
                    self.trace_lenghts[step_len] = 1
                if step_len > self.max_step_len:  ## Set max step len
                    self.max_step_len = step_len
                    self.max_step_len_step_index = index
                    self.max_step_len_line = int(trace[str(frames[index])][0]) + 2
                    self.max_step_len_frame_number = frame
                self.trace_lenn = self.trace_lenn + step_len
            except IndexError as err:
                if not index == len(frames) - 1:
                    # print(index)
                    # print(len(frames))
                    # print(trace)
                    # print("Error:", str(err))
                    raise err

    def show_step_lenghts_hist(self):
        # print(self.trace_lenghts)
        plt.bar(list(self.trace_lenghts.keys()), self.trace_lenghts.values(), color='g', )
        plt.xlabel('Count of steps')
        plt.ylabel('Step size')
        plt.title(f'Histogram of step lengths. Trace {self.id}.')
        plt.show()