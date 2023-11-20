import json
import os
import threading
import warnings
from multiprocessing import Process
from _socket import gethostname
from os.path import exists
from sys import platform
import cv2
from termcolor import colored

import analyse
import video_windows
from misc import convert_frame_number_back, is_in, get_leftmost_point, to_vect, get_colors, rgb_to_bgr, get_last_digit, \
    modulo, get_colour
from trace import Trace

global show_single
global show_number
# global video
global goto
goto = None


def make_named_window():
    if "lin" in platform:
        cv2.namedWindow("video", cv2.WINDOW_NORMAL)
    else:
        cv2.namedWindow("video", cv2.WINDOW_NORMAL)


def play_opencv(input_video, frame_range, speed, points, align_traces, align_arena_boundaries):
    """ Plays the given video in a new window.

    :arg input_video: (Path or str): path to the input video
    :arg frame_range: (list or tuple): if set shows only given frame range of the video
    :arg speed: ratio of rate, hence default speed is 1
    :arg points: (tuple of points): points to be shown over the video (TO ALIGN THE VIDEO)
    :arg align_traces: (bool or Path): flag whether to align traces (one time alignment of the traces to the video), use path to the file instead of True
    :arg align_arena_boundaries: (bool or Path): flag whether to align arena (one time alignment of the arena boundaries to the video), use path to the file instead of True
    :return: points: list of pairs - points obtained by alignment
    """
    # global video
    global goto
    video = cv2.VideoCapture(input_video)

    # Window name and size
    make_named_window()

    if frame_range:
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_range[0]-1)

    if points:
        print("Press WASD keys to move point(s) to respective direction, use +/- keys to enlarge/decrease the circle size and press q to save the alignment and close the window.")
    else:
        print("Press q (while video window) to stop the video and continue to question, press r to restart, a to rewind, d to forward, - to slow down, + to speed up")

    fps = video.get(5)

    first = True

    if frame_range:
        # print("frame_range", frame_range)
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_range[0])

    cv2.setWindowProperty("video", cv2.WND_PROP_TOPMOST, 1)

    # while video.isOpened():
    while True:
        frame_number = int(video.get(1))

        # Read video capture
        ret, frame = video.read()

        # Show the frame number
        cv2.putText(img=frame, text=str(frame_number), org=(15, 30), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.0,
                    color=(125, 246, 55), thickness=4)
        if points:
            colors = get_colors(len(points))
            colors = list(map(rgb_to_bgr, colors))

            for index, point in enumerate(points):
                point = list(map(round, point))
                # if point[0] != -1 and point[1] != -1:
                cv2.circle(frame, point, 4, color=colors[modulo(len(colors), index)], thickness=-1, lineType=cv2.LINE_AA)

        # Display each frame
        if str(gethostname()) == "Skadi":
            frame = cv2.resize(frame, [1736, 864], interpolation=cv2.INTER_AREA)

        if frame_range:
            if frame_range[0] <= frame_number <= frame_range[1]:
                cv2.imshow("video", frame)
        else:
            cv2.imshow("video", frame)

        key = cv2.waitKey(round(2*(100/fps)/speed))

        if first:
            # time.sleep(3)
            first = False

        if goto is not None:
            assert isinstance(goto, tuple)
            go_to_trace_start(*goto)
            goto = None

        if key == ord('q') or key == ord('Q'):
            break
        if key == ord('r') or key == ord('R'):
            if frame_range:
                video.set(cv2.CAP_PROP_POS_FRAMES, frame_range[0]-1)
            else:
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)

        if key == ord('a') or key == ord('A'):
            video.set(cv2.CAP_PROP_POS_FRAMES, max(frame_number - 100, frame_range[0]))

        if key == ord('d') or key == ord('D'):
            video.set(cv2.CAP_PROP_POS_FRAMES, min(frame_number + 100, frame_range[1]))

        if points:
            if key == ord("s") or key == ord('S'):
                for index, point in enumerate(points):
                    points[index] = [point[0], point[1]+10]

                # points = list(map(lambda x: x[1] = x[1] + 10, points))
            if key == ord("w") or key == ord('W'):
                for index, point in enumerate(points):
                    points[index] = [point[0], point[1]-10]

            if key == ord("a") or key == ord('A'):
                for index, point in enumerate(points):
                    points[index] = [point[0]-10, point[1]]

            if key == ord("d") or key == ord('D'):
                for index, point in enumerate(points):
                    points[index] = [point[0]+10, point[1]]

            if key == ord("s") or key == ord("w") or key == ord("a") or key == ord("d") or key == ord('W') or key == ord('A') or key == ord('S') or key == ord('D'):
                if frame_range:
                    video.set(cv2.CAP_PROP_POS_FRAMES, frame_range[0] - 1)
                else:
                    video.set(cv2.CAP_PROP_POS_FRAMES, 0)

            if key == ord("+"):
                left, right, up, down = points
                left = [left[0]-1, left[1]]
                right = [right[0]+1, right[1]]
                up = [up[0], up[1]+1]
                down = [down[0], down[1]-1]
                points = [left, right, up, down]

            if key == ord("-"):
                left, right, up, down = points
                left = [left[0]+1, left[1]]
                right = [right[0]-1, right[1]]
                up = [up[0], up[1]-1]
                down = [down[0], down[1]+1]
                points = [left, right, up, down]

    video.release()
    # Exit and destroy all windows
    cv2.destroyAllWindows()
    if points:
        if align_traces:
            with open(align_traces, "w") as file:
                file.write(f"video file: {input_video})\n")
                file.write(f"frame: {frame_range[0]}\n")
                file.write(f"points assigned: {points}\n")
        if align_arena_boundaries:
            print(f"Saving arena location in: {align_arena_boundaries}")
            with open(align_arena_boundaries, "w") as file:
                file.write(f"video file: {input_video})\n")
                file.write(f"frame: {frame_range[0]}\n")
                file.write(f"points assigned: {points}\n")
    return points


def show_video(input_video, traces=(), frame_range=(), video_speed=0.1, wait=False, points=(), video_params=True,
               fix_x_first_colors=False, align_traces=False, align_arena=False):
    """ Shows given video.

        :arg input_video: (Path or str): path to the input video
        :arg traces: (list): list of Traces to be shown
        :arg frame_range: (list or tuple): if set shows only given frame range of the video
        :arg video_speed: (float): ratio of rate, hence default speed is 1
        :arg wait: (bool): if True it will wait for the end of the video
        :arg points: (tuple of points): points to be shown over the video
        :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
        :arg fix_x_first_colors: (int): first given colors will be used only once in the video
        :arg align_traces: (bool): if True use points to align traces
        :arg align_arena: (bool): if True use points to align arena boundaries
    """
    if not input_video:
        return

    if not exists(input_video):
        print(colored(f"Could not find the video file: {input_video} \n", "red"))
        return

    vid_capture = cv2.VideoCapture(input_video)
    if vid_capture.isOpened() is False:
        print(colored(f"Error opening the video file: {input_video} \n", "red"))
        return
    # fps = vid_capture.get(5)
    vid_capture.release()

    print(f"Gonna show frame range: {frame_range}")

    if video_speed > 1:
        video_speed = 1

    if align_traces or align_arena:
        # to show points
        p = Process(target=play_opencv, args=(input_video, frame_range, video_speed, points, analyse.point_file if align_traces else False, analyse.arena_file if align_arena else False))
        p.start()
        # thread = threading.Thread(target=play_opencv, args=(input_video, frame_range, video_speed, points, align_traces, align_arena))
        # thread.start()
    else:
        try:
            assert isinstance(video_params, tuple) or isinstance(video_params, list)
        except AssertionError:
            video_params = (0, (0, 0))
        # show traces over

        # annotate_video(input_video, False, traces, frame_range, video_speed, 0, video_params[0], video_params[1], points, fix_x_first_colors, True)

        # print("gonna initialise app")
        video_windows.traces_to_show = traces
        video_windows.trim_offset = analyse.trim_offset
        app = video_windows.App()

        # print("gonna make a thread")
        p = threading.Thread(target=call_annotate_video_and_quit_gui_afterwards, args=(input_video, False, traces, frame_range, video_speed, 0, video_params[0], video_params[1], points, fix_x_first_colors, True, app,))
        p.start()

        # print("gonna run the app")
        app.mainloop()

        # p1 = Process(target=video_windows_tkinter.gui, args=(traces, analyse.trim_offset, ))
        # p1.start()
        # print("hello")
        #

        # thread.join()
        # thread1.join()
        # p = Process(target=annotate_video, args=(input_video, False, traces, frame_range, video_speed, 0, video_params[0], video_params[1], points, fix_x_first_colors, True,))
        # p.start()
    if wait:
        try:
            p.join()
            # del p

        except Exception as err:
            print("1", err)
            raise err


def call_annotate_video_and_quit_gui_afterwards(a, b, c, d, e, f, g, h, i, j, k, app):
    """ Call annotate_video() and after it is closed it quits the gui interface. """
    # print("call_annotate_video_and_quit_gui_afterwards here")
    # print("gonna annotate the video")
    annotate_video(a, b, c, d, e, f, g, h, i, j, k)
    # print("gonna kill the gui")
    analyse.gonna_run = False
    # app.destroy()
    # print("gui destroyed")

    # app.quit()
    # app.destroy()
    # app.quitt()
    # print("gui quited")

    # del app


def show_all_traces():
    """ Shows all traces in the video. """
    global show_single
    show_single = False
    print("Showing all traces.")


def show_single_trace(index):
    """ Shows single trace in the video.

    :arg index: (int): showing only trace with the given index
    """
    global show_single
    global show_number
    show_single = True
    print("Showing single trace of index", index)
    show_number = index


def go_to_trace_start(index, traces_to_show, trim_offset):
    """ In the video, goes to the beginning of the given trace.

    :arg index: (int): index of the trace to be shown from traces_to_show
    :arg traces_to_show: (list): the list of traces to be shown in the video
    :arg trim_offset: (int): offset of the trimmed video
    """
    start = traces_to_show[index].frame_range[0]
    global video
    video.set(cv2.CAP_PROP_POS_FRAMES, trim_offset + start)


def annotate_video(input_video, output_video, traces_to_show, frame_range, speed=1, trace_offset=0, trim_offset=0, crop_offset=(0, 0), points=(), fix_x_first_colors=False, show=False, force_new_video=False, debug=False):
    """ Annotates given video with the tracked position of individual bees.

    :arg input_video: (Path or str): path to the input video
    :arg output_video: (Path or str): path to the input video
    :arg traces_to_show: (list): a list of Traces to be shown
    :arg frame_range: (list or tuple): if set shows only given frame range of the video
    :arg speed: ratio of rate, hence default speed is 1
    :arg trace_offset: (int): number of the first frames where there is no trace
    :arg trim_offset: (int): number of the first frames to trim from original video
    :arg crop_offset: (tuple): a pair of pints, a vector to offset the location in order to match the input video
    :arg fix_x_first_colors: (int): first given colors will be used only once in the video
    :arg show: (bool): if True showing the frames, used with False only to annotate the video at the end of analysis
    :arg force_new_video: (bool): iff True, a new video will be created, even if video with the same amount of traces is there
    """

    lock = threading.Lock()
    lock.acquire()
    # print("lock acquired")

    from traces_logic import delete_trace_with_id, undelete_trace_with_id
    global show_single
    global show_number
    # global spamewqrt
    global goto
    show_single = False

    qt_working = None  ## Flag whether qt support is working

    if traces_to_show and not show:
        print(colored("ANNOTATES THE VIDEO WITH NEW TRACES", "blue"))

    if output_video:
        ## annotate only if the annotated video does not exist
        # print("output_video_file:", output_video)
        if force_new_video:
            if exists(output_video):
                number = 1
                spam = os.path.splitext(output_video)
                while exists(str(spam[0]+'_ver_'+str(number)+spam[1])):
                    number = number + 1
                output_video = str(spam[0]+'_ver_'+str(number)+spam[1])
        else:
            if exists(output_video):
                print(colored("Chosen video already exists, not overwriting it.", "yellow"))
                return
        print("output_video_file:", output_video)

    if frame_range:
        if frame_range[1] < trace_offset:
            print(colored(f"NOT SHOWING THE VIDEO AS frame_range[1] {frame_range[1]} < trace_offset {trace_offset}", "red"))
            return

    # Manage None input
    trace_offset = 0 if trace_offset is None else trace_offset
    trim_offset = 0 if trim_offset is None else trim_offset
    crop_offset = (0, 0) if crop_offset is None else crop_offset

    trace_ranges = []
    for trace in traces_to_show:
        assert isinstance(trace, Trace)
        trace_ranges.append(trace.frame_range)

    # PARAMS
    len_of_trace_shown_behind = 30  # number of frames the path is shown behind

    # Create a video capture object, in this case we are reading the video from a file
    # global video
    video = cv2.VideoCapture(input_video)

    make_named_window()

    try:
        cv2.createButton(f"Show All Traces", show_all_traces, None, cv2.QT_PUSH_BUTTON, 1)
        qt_working = True
    except cv2.error as err:
        qt_working = False

        # spamewqrt = traces_to_show

        ## Following line creates the gui but the rest of the program is paused wil gui is running
        # video_windows_tkinter.create_main_window(traces_to_show, trim_offset)
        # thread = threading.Thread(target=video_windows_tkinter.runn)
        # video_windows_tkinter.traces_to_show = traces_to_show
        # thread.run()
        # thread1 = video_windows_tkinter.Gui_video_thread(traces_to_show, trim_offset)
        # thread1.start()

    if qt_working is True:
        for indexx, trace in enumerate(traces_to_show):
            spam = indexx
            if trace.trace_id != traces_to_show[indexx].trace_id:
                raise Exception("indexing problem")
            cv2.createButton(f"Highlight Trace {trace.trace_id}", show_single_trace, [indexx], cv2.QT_PUSH_BUTTON | cv2.QT_NEW_BUTTONBAR, 1)
            cv2.createButton(f"Delete Trace {trace.trace_id}", delete_trace_with_id, [trace.trace_id], cv2.QT_PUSH_BUTTON, 1)
            cv2.createButton(f"UnDelete Trace {trace.trace_id}", undelete_trace_with_id, [trace.trace_id, indexx], cv2.QT_PUSH_BUTTON, 1)
            cv2.createButton(f"[{trace.frame_range[0]},{trace.frame_range[1]}]", go_to_trace_start, [video, spam, traces_to_show, trim_offset], cv2.QT_PUSH_BUTTON, 1, )
    else:
        pass  ## buttons created already elsewhere

    if str(gethostname()) == "Skadi":
        cv2.moveWindow("video", 0, 0)
        cv2.resizeWindow("video", 1900, 800)

    if video.isOpened() is False:
        print(colored("Error opening the video file", "red"))
    else:
        if show:
            print("Press q (while video window) to stop the video and continue to question. \nPress r to restart, a to rewind, d to forward, - to slow down, + to speed up.")
            # print("Press 0-9 to show only respective trace, Enter to start the video when the trace starts, or . to show all traces")
            if qt_working:
                print("Press Ctrl+P to show trace management - deleting, undeleting and showing the traces.")

        fps = video.get(5)
        if debug:
            print('Frames per second: ', fps, 'FPS')

        frame_count = video.get(7)
        if debug:
            print('Frame count: ', frame_count)

        if frame_range and debug:
            print('Show frames: ', frame_range)

        if debug:
            print('Ranges of Traces: ', trace_ranges)
            print('Traces to show: ', list(map(lambda x: x.trace_id, traces_to_show)))
        # print('All Traces: ', list(map(lambda x: x.trace_id, analyse.traces)))

    # Obtain frame population_size information using get() method
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))
    frame_size = (frame_width, frame_height)
    fps = int(video.get(5))

    # Initialize video writer object
    if output_video:
        output = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size)

    ## INITIALISE ANNOTATION
    locations_of_traces = []
    colors = get_colors(len(traces_to_show))
    if debug:
        print("traces colours (R,G,B):", colors)
    colors = list(map(rgb_to_bgr, colors))
    # print("traces colours (G,B,R):", colors)

    for trace in traces_to_show:
        ## TODO this can be optimised using queue instead of list
        locations_of_traces.append([])

    video.set(cv2.CAP_PROP_POS_FRAMES, trim_offset)
    cv2.setWindowProperty("video", cv2.WND_PROP_TOPMOST, 1)

    # while video.isOpened():
    while video.isOpened() or show:
        # vid_capture.read() methods returns a tuple, first element is a bool and the second is frame
        ret, frame = video.read()

        if frame_range:
            if int(video.get(1)) < trim_offset + max(trace_offset, frame_range[0]):
                video.set(cv2.CAP_PROP_POS_FRAMES, trim_offset + max(trace_offset, frame_range[0]))

        # convert current video frame into trace frame number
        frame_number = int(video.get(1)) - trim_offset
        # print("frame_number to look at in locations", frame_number)

        ## TODO uncomment this to annotate only first 50 frames - for development purpose only
        # if output_video and frame_number > 500 + trace_offset:
        #     # print("over")
        #     video.release()
        #     output.release()
        #     return

        if ret == True:
            for point in points:
                pointA = list(map(lambda x: round(x), to_vect(crop_offset, point)))
                cv2.circle(frame, pointA, 4, color=rgb_to_bgr((255, 255, 255)), thickness=-1, lineType=cv2.LINE_AA)

            ## ANNOTATION
            for trace_index, trace in enumerate(traces_to_show):
                if show_single:
                    if trace_index != show_number:
                        continue
                # if trace_index > 0:
                #     continue

                try:
                    location_index = trace.frames_list.index(frame_number)
                except ValueError as err:
                    continue

                # Recalculate the original's video position
                # Round the position to whole pixels
                spam = trace.locations[location_index]
                pointA = list(map(lambda x: round(x), to_vect(crop_offset, spam)))
                # TODO have a look here in case of hiding points [-1,-1]
                # if spam[0] > 0 and spam[1] > 0:
                #     pointA = list(map(lambda x: round(x), to_vect(crop_offset, spam)))
                # else:
                #     print()

                try:
                    # TODO have a look here in case of hiding points [-1,-1]
                    # if pointA[0] > 0 and pointA[1] > 0:

                    # cv2.line(frame, pointA, pointB, (255, 255, 0), thickness=3, lineType=cv2.LINE_AA)
                    cv2.circle(frame, pointA, 4, color=rgb_to_bgr(get_colour(trace_index, fix_x_first_colors)), thickness=-1, lineType=cv2.LINE_AA)
                    cv2.putText(frame, str(trace.trace_id), [pointA[0]+12, pointA[1]-12], fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.2,
                                color=rgb_to_bgr(get_colour(trace_index, fix_x_first_colors)),
                                thickness=2, lineType=cv2.LINE_AA)
                except Exception as err:
                    print(err)
                    print("Cannot show the point:", pointA)

                locations_of_traces[trace_index].append(pointA)
                for index, point in enumerate(locations_of_traces[trace_index]):
                    if index == 0:
                        continue
                    try:
                        cv2.line(frame, locations_of_traces[trace_index][index-1], point, color=rgb_to_bgr(get_colour(trace_index, fix_x_first_colors)), thickness=1, lineType=cv2.LINE_AA)
                    except IndexError as err:
                        print("index", index)
                        print(len(locations_of_traces[trace_index]))
                        raise err

                if len(locations_of_traces[trace_index]) > len_of_trace_shown_behind:
                    del locations_of_traces[trace_index][0]

            if show:
                if not frame_range or int(video.get(1)) <= trim_offset + frame_range[1]:
                    cv2.putText(img=frame, text=str(frame_number), org=(15, 30), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.0, color=(125, 246, 55), thickness=4)
                    cv2.imshow("video", frame)

                    # if str(gethostname()) == "Skadi":
                    #     cv2.moveWindow("video", 0, 0)
                    #     cv2.resizeWindow("video", 1900, 650)

                key = cv2.waitKey(round(2 * (100 / fps) / speed))

                if goto is not None:
                    assert isinstance(goto, tuple)
                    go_to_trace_start(*goto)
                    goto = None

                if key == ord('f') or key == ord('F'):
                    print(goto)

                if key == ord('q') or key == ord('Q'):
                    break
                if key == ord('r') or key == ord('R'):
                    if frame_range:
                        video.set(cv2.CAP_PROP_POS_FRAMES, trim_offset + frame_range[0])
                    else:
                        video.set(cv2.CAP_PROP_POS_FRAMES, trim_offset)
                    # locations_of_traces = [[]]*len(traces)
                    locations_of_traces = []
                    for trace in traces_to_show:
                        locations_of_traces.append([])

                if key == ord('a') or key == ord('A'):
                    if frame_range:
                        video.set(cv2.CAP_PROP_POS_FRAMES, max(trim_offset + frame_number - 100, trim_offset + frame_range[0]))
                    else:
                        video.set(cv2.CAP_PROP_POS_FRAMES, max(trim_offset + frame_number - 100, trim_offset + 0))
                    # locations_of_traces = [[]]*len(traces)
                    locations_of_traces = []
                    for trace in traces_to_show:
                        locations_of_traces.append([])

                if key == ord('d') or key == ord('D'):
                    if frame_range:
                        video.set(cv2.CAP_PROP_POS_FRAMES, min(trim_offset + frame_number + 100, trim_offset + frame_range[1]))
                    else:
                        video.set(cv2.CAP_PROP_POS_FRAMES, min(trim_offset + frame_number + 100, frame_count))

                    # locations_of_traces = [[]]*len(traces)
                    locations_of_traces = []
                    for trace in traces_to_show:
                        locations_of_traces.append([])

                if key == ord('+'):
                    speed = 1.1 * speed

                if key == ord('-'):
                    speed = 0.9 * speed

                for numeral in range(10):
                    if key == ord(f'{numeral}'):
                        show_single = True
                        show_number = numeral
                        # print(f"key {numeral} pressed")

                if key == ord('.'):
                    show_single = False

                if key == ord('\n') or key == ord('\r'):
                    print("Enter pressed ")
                    video.set(cv2.CAP_PROP_POS_FRAMES, trim_offset + traces_to_show[show_number].frame_range[0])
                    locations_of_traces = []
                    for trace in traces_to_show:
                        locations_of_traces.append([])

            # Write the frame to the output files
            if output_video:
                output.write(frame)

            # 20 is in milliseconds, try to increase the value, say 50 and observe
            # make a queue of length 20
            ## TODO MAYBE UNCOMMENT THIS
            # key = cv2.waitKey(1)
            #
            # if key == ord('q') or key == ord('Q'):
            #     break
        else:
            break

    # Release the objects
    cv2.destroyAllWindows()
    # print("all windows destroyed")

    video.release()
    # print("video released")
    # print(video.isOpened())
    # del video

    if output_video:
        output.release()
        # del output
        print(colored("Annotation done.", "yellow"))

    lock.release()
    # print("lock released")


def make_help_video(debug=False):
    """ Annotates given video with the tracked position of individual bees.

    :arg debug: (bool): if True extensive output is shown
    """
    print(colored("MAKE HELP VIDEO", "blue"))

    # Create a video capture object, in this case we are reading the video from a file
    vid_capture = cv2.VideoCapture(r"../test/help_input.mp4")

    if vid_capture.isOpened() is False:
        print("Error opening the video file")
    # Read fps and frame count
    else:
        # Get frame rate information
        # You can replace 5 with CAP_PROP_FPS as well, they are enumerations
        fps = vid_capture.get(5)
        if debug:
            print('Frames per second : ', fps, 'FPS')

        # Get frame count
        # You can replace 7 with CAP_PROP_FRAME_COUNT as well, they are enumerations
        frame_count = vid_capture.get(7)
        if debug:
            print('Frame count : ', frame_count)

    # Obtain frame population_size information using get() method
    frame_width = int(vid_capture.get(3))
    frame_height = int(vid_capture.get(4))
    frame_size = (frame_width, frame_height)
    fps = int(vid_capture.get(5))
    # Initialize video writer object

    output = cv2.VideoWriter("../test/help_video.mp4", cv2.VideoWriter_fourcc(*'XVID'), fps, frame_size)

    ## INITIALISE ANNOTATION
    locations_of_traces = []

    while vid_capture.isOpened():
        # vid_capture.read() methods returns a tuple, first element is a bool
        # and the second is frame
        ret, frame = vid_capture.read()

        frame_number = int(vid_capture.get(1))
        # print("frame_number", frame_number)

        if ret is True:
            # cv2.line(frame, [0,0], [700,700], [255,0,0], thickness=8, lineType=cv2.LINE_AA)
            # cv2.line(frame, [300, 300], [300, -900], [0, 255, 0], thickness=8, lineType=cv2.LINE_AA)
            # cv2.circle(frame, [200,200], 4, color, thickness=-1, lineType=cv2.LINE_AA)

            cv2.putText(img=frame, text=str(frame_number), org=(15, 30), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.0,
                        color=(125, 246, 55), thickness=4)

            # Write the frame to the output files
            output.write(frame)

            # Show the frame
            cv2.imshow('Frame', frame)

            # wait for the frame to be shown
            key = cv2.waitKey(1)

            # press 'q' key to stop the annotation
            if key == ord('q') or key == ord('Q'):
                break
        else:
            break

    # Release the objects
    vid_capture.release()
    output.release()
    print("Finished annotation.")


## BEE SPECIFIC
def parse_video_info(video_file, traces, csv_file_path):
    """ Obtains video parameters either loading from the json or via user-guided video and csv file parser.
    Use file with "movie" in its name to skip this (returning (None, None))

    vect - to move the locations according the cropping the video
    trace_offset - number of first frames of the video to skip

    :arg traces (list) list of traces
    :arg video_file: (Path or str): path to the input video
    :arg csv_file_path: (str or Path): path to the csv_file
    :return: tuple:
            vector of shift to assign to the locations so that align with the not cropped video,
            number of first frames of the video to be skipped
    """
    # There is no video file
    if not video_file:
        warnings.warn("No video file given.")
        return None, None

    # There is video file given but the files does not exist
    if os.path.isfile(video_file) is not True:
        warnings.warn("Video file does not exist.")
        return None, None

    # If a trimmed and cropped video is used
    if "movie" not in video_file:
        try:
            try:
                # if transpositions empty
                if os.stat("../auxiliary/transpositions.txt").st_size == 0:
                    raise KeyError
                # load transpositions
                with open("../auxiliary/transpositions.txt") as file:
                    transpositions = json.load(file)
            except FileNotFoundError as err:
                # transpositions.txt not found
                raise KeyError
            # load video record
            crop_vect, frame_offset = transpositions[video_file]

        except KeyError:
            # transposition or the file not found, align the video
            crop_vect, frame_offset = align_the_video(traces, video_file, csv_file_path)

        return frame_offset, crop_vect

    else:
        return 0, [0, 0]


def align_the_video(traces, video_file, csv_file_path):
    """ User-guided alignment of the video onto its not cropped version.

    :arg traces (list) list of traces
    :arg video_file: (Path or str): path to the input video
    :arg csv_file_path: (str or Path): path to the csv_file
    :return: vector of shift to assign to the locations so that align with the not cropped video,
            number of first frames of the video to be skipped
    """
    # Find a frame with at least half of population
    # if population_size == 1:
    #     da_frame = traces[0].frame_range[0]
    #     da_traces_indices = [0]
    # else:
    #     da_frame = -1
    #     for number in reversed(range(population_size)):
    #         dictionary = dictionary_of_m_overlaps_of_n_intervals(population_size, list(map(lambda x: x.frame_range, traces)), skip_whole_in=False)
    #         if not dictionary:
    #             continue
    #         else:
    #             da_frame = list(dictionary.values())[0][0]
    #             da_traces = list(dictionary.keys())[0]
    #             break

    da_frame = 5000
    points = []
    for trace in traces:
        assert isinstance(trace, Trace)
        if is_in([da_frame, da_frame], trace.frame_range):
            points.append(trace.get_location_from_frame(da_frame))

    offset_frame = convert_frame_number_back(0, csv_file_path)

    da_converted_frame = convert_frame_number_back(da_frame, csv_file_path)

    # show_video(input_video, traces=(), frame_range=(), video_speed=0.1, wait=False, points=(), video_params=True)
    show_video(input_video=video_file, traces=(), frame_range=[da_converted_frame, da_converted_frame], wait=True,
               points=points, video_params=True, align_traces=True)

    # READ THE OUTPUT FILE
    with open(analyse.point_file, "r") as file:
        lines = file.readlines()

    for line in lines:
        if "points assigned:" in line:
            assigned_points = line.split(":")[1]
        # if "frame:" in line:
        #     offset_frame = int(line.split(":")[1])

    try:
        assigned_points = json.loads(assigned_points)
    except NameError:
        raise Exception("Loading the point from the auxiliary/point.txt failed, please check the file.")

    leftmost_point, a = get_leftmost_point(points)
    leftmost_assigned_point, b = get_leftmost_point(assigned_points)
    leftmost_assigned_point = list(map(float, leftmost_assigned_point))
    ## TODO - maybe check that all the other points share the vector of transposition
    vector = to_vect(leftmost_point, leftmost_assigned_point)
    vector = list(map(lambda x: -x, vector))

    ## STORE THE ALIGNMENT
    try:
        os.mkdir("../auxiliary")
    except OSError:
        pass

    try:
        if os.stat("../auxiliary/transpositions.txt").st_size == 0:
            transpositions = {}
        else:
            with open("../auxiliary/transpositions.txt") as file:
                transpositions = json.load(file)
    except FileNotFoundError as err:
        file = open("../auxiliary/transpositions.txt", "a")
        file.close()
        transpositions = {}

    if video_file in transpositions.keys():
        raise Exception("This transposition already in the file.")

    transpositions[video_file] = [vector, offset_frame]

    with open("../auxiliary/transpositions.txt", 'w') as file:
        file.write(json.dumps(transpositions))

    return vector, offset_frame


# BEES SPECIFIC
def obtain_arena_boundaries(video_file, csv_file_path, center, diameter):
    """ User-guided alignment of the arena boundaries.

    :arg video_file: (Path or str): path to the input video
    :arg csv_file_path: (str or Path): path to the csv_file
    :arg center: (point): location of the center of the arena
    :arg diameter: (int): diameter of the arena (in pixels)
    :return: new_center, new_diameter
    """

    da_frame = 5000

    x, y = center

    # LEFT RIGHT UP DOWN
    points = [[x-diameter/2, y], [x+diameter/2, y], [x, y+diameter/2], [x, y-diameter/2]]

    da_converted_frame = convert_frame_number_back(da_frame, csv_file_path)

    show_video(input_video=video_file, traces=(), frame_range=[da_converted_frame, da_converted_frame], wait=True,
               points=points, video_params=True, align_arena=True)

    # READ THE OUTPUT FILE
    with open(analyse.arena_file, "r") as file:
        lines = file.readlines()

    for line in lines:
        if "points assigned:" in line:
            assigned_points = line.split(":")[1]
        # if "frame:" in line:
        #     offset_frame = int(line.split(":")[1])

    assigned_points = json.loads(assigned_points)

    left, right, up, down = assigned_points

    new_center = [round((right[0] + left[0])/2), round((up[1] + down[1])/2)]

    ## RECALCULATE FROM THE VIDEO
    trim, crop = analyse.video_params
    new_center = [new_center[0] + crop[0], new_center[1] + crop[1]]

    new_diameter = right[0] - left[0]

    ## STORE THE ALIGNMENT
    try:
        if os.stat(analyse.arena_boundaries_file).st_size == 0:
            transpositions = {}
        else:
            with open(analyse.arena_boundaries_file) as file:
                transpositions = json.load(file)
    except FileNotFoundError as err:
        file = open(analyse.arena_boundaries_file, "a")
        file.close()
        transpositions = {}

    # if video_file in transpositions.keys():
    #     raise Exception("Arena boundaries for this video already in the file.")

    transpositions[video_file] = [new_center, new_diameter]

    with open(analyse.arena_boundaries_file, 'w') as file:
        file.write(json.dumps(transpositions))

    return new_center, new_diameter


if __name__ == "__main__":
    # make_help_video()
    # show_video(input_video, traces=(), frame_range=(), video_speed=0.1, wait=False, points=(), video_params=True)

    # show_video("../test/help_video.mp4")
    # show_video("../test/help_video.mp4", frame_range=(300, 500), wait=False, video_speed=5)
    # show_video("../test/help_video.mp4", frame_range=(300, 500), video_params=[0, (0, 0)], video_speed=5)
    annotate_video("../test/help_video.mp4", False, (), frame_range=(), speed=1, trace_offset=0, trim_offset=50, crop_offset=(0, 0), show=True)
    # show_video("../test/help_video.mp4", frame_range=(300, 500), video_params=[0, 0, (0, 0)], video_speed=0.5)
