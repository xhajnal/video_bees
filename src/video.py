import json
import multiprocessing
import os
import time
from multiprocessing import Process
from threading import Thread
import cv2
import distinctipy
from termcolor import colored

from misc import convert_frame_number_back, dictionary_of_m_overlaps_of_n_intervals, is_in, get_leftmost_point, to_vect
from trace import Trace
import vlc
from tkinter import *


def play_opencv(input_video, frame_range, fps, speed, points):
    """ Plays the given video in a new window.

    :param input_video: (Path or str): path to the input video
    :param frame_range: (list or tuple): if set shows only given frame range of the video
    :param fps: (int): number of frames per second
    :param speed: ratio of rate, hence default speed is 1
    :arg points: (tuple of points): points to be shown over the video
    :return:
    """
    video = cv2.VideoCapture(input_video)
    # window name and size
    cv2.namedWindow("video", cv2.WINDOW_AUTOSIZE)
    if frame_range:
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_range[0]-1)
    print("Press q (while video window) to stop the video, press r to restart.")

    first = True

    while video.isOpened():
        # Read video capture
        ret, frame = video.read()
        frame_number = int(video.get(1))
        # print(frame_number)
        # Show the frame number
        cv2.putText(img=frame, text=str(frame_number), org=(15, 30), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.0,
                    color=(125, 246, 55), thickness=4)
        if points:
            colors = distinctipy.get_colors(len(points))
            colors = list(map(lambda x: [round(x[0] * 255), round(x[1] * 255), round(x[2] * 255)], colors))
            for index, point in enumerate(points):
                point = list(map(round, point))
                cv2.circle(frame, point, 4, colors[index], thickness=-1, lineType=cv2.LINE_AA)

        # Display each frame
        if frame_range:
            if frame_range[0] <= frame_number <= frame_range[1]:
                cv2.imshow("video", frame)
        else:
            cv2.imshow("video", frame)
        key = cv2.waitKey(round(2*(100/fps)/speed))

        if first:
            # time.sleep(3)
            first = False

        if key == ord('q'):
            break
        if key == ord('r'):
            if frame_range:
                video.set(cv2.CAP_PROP_POS_FRAMES, frame_range[0]-1)
            else:
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        if points:
            if key == ord("s"):
                for index, point in enumerate(points):
                    points[index] = [point[0], point[1]+10]

                # points = list(map(lambda x: x[1] = x[1] + 10, points))
            if key == ord("w"):
                for index, point in enumerate(points):
                    points[index] = [point[0], point[1]-10]

            if key == ord("a"):
                for index, point in enumerate(points):
                    points[index] = [point[0]-10, point[1]]

            if key == ord("d"):
                for index, point in enumerate(points):
                    points[index] = [point[0]+10, point[1]]

            if key == ord("s") or key == ord("w") or key == ord("a") or key == ord("d"):
                if frame_range:
                    video.set(cv2.CAP_PROP_POS_FRAMES, frame_range[0] - 1)
                else:
                    video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    video.release()
    # Exit and destroy all windows
    cv2.destroyAllWindows()
    if points:
        with open("../auxiliary/point.txt", "w") as file:
            file.write(f"video file: {input_video})\n")
            file.write(f"frame: {frame_range[0]}\n")
            file.write(f"points assigned: {points}\n")

    return points


def play_tk_opencv(input_video, frame_range, fps, speed):
    root = Tk()
    root.geometry("600x600")
    video = cv2.VideoCapture(input_video)
    # window name and size
    cv2.namedWindow("video", cv2.WINDOW_AUTOSIZE)
    while video.isOpened():
        # Read video capture
        ret, frame = video.read()
        # Display each frame
        cv2.imshow("video", frame)

    def on_closing():
        video.release()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

    try:
        # Release capture object
        video.release()
        # Exit and destroy all windows
        cv2.destroyAllWindows()
    except OSError:
        pass


def play_tk_vlc(input_video, frame_range, fps, speed):
    os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
    root = Tk()
    root.geometry("600x600")
    instance = vlc.Instance()
    player = instance.media_player_new()
    player.set_hwnd(root.winfo_id())
    player.set_media(instance.media_new(input_video))
    player.set_rate(speed)

    player.play()
    if frame_range:
        new_time = frame_range[0] * int(1000 // fps)
        player.set_time(new_time)

    def on_closing():
        player.stop()
        player.get_media().release()
        player.release()
        player.get_instance().release()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

    try:
        player.stop()
        player.get_media().release()
        player.release()
        player.get_instance().release()
    except OSError:
        pass


def play_vlc(input_video, frame_range):
    os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
    player = vlc.MediaPlayer(input_video)
    player.play()
    if frame_range:
        new_time = frame_range[0] * int(1000 // 100)
        player.set_time(new_time)
        time.sleep((frame_range[1] - frame_range[0]) / 100)
        player.pause()
        ## TODO slow down the video
        # player.stop()
        # player.get_media().release()
        # player.release()
        # player.get_instance().release()


def play_vlc2(input_video, frame_range):
    # creating an instance of vlc
    os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
    vlc_obj = vlc.Instance()

    # creating a media player
    vlcplayer = vlc_obj.media_player_new()

    # creating a media
    vlcmedia = vlc_obj.media_new(input_video)

    # setting media to the player
    vlcplayer.set_media(vlcmedia)

    # playing the video
    vlcplayer.play()


def show_video(input_video, frame_range=(), video_speed=0.1, wait=False, points=()):
    """ Shows given video

        :arg input_video: (Path or str): path to the input video
        :arg frame_range: (list or tuple): if set shows only given frame range of the video
        :arg video_speed: (float): ratio of rate, hence default speed is 1
        :arg wait: (bool): if True it will wait for the end of the video
        :arg points: (tuple of points): points to be shown over the video
    """
    vid_capture = cv2.VideoCapture(input_video)

    if vid_capture.isOpened() is False:
        print("Error opening the video file: ", input_video)
        return
    # Read fps and frame count
    else:
        # Get frame rate information
        # You can replace 5 with CAP_PROP_FPS as well, they are enumerations
        fps = vid_capture.get(5)
        # print("fps", fps)
    vid_capture.release()

    # vid_capture = cv2.VideoCapture(input_video)
    #
    # if (vid_capture.isOpened() == False):
    #     print("Error opening the video file")
    #
    # while (vid_capture.isOpened()):
    #     # vid_capture.read() methods returns a tuple, first element is a bool
    #     # and the second is frame
    #     ret, frame = vid_capture.read()
    #
    #     frame_number = int(vid_capture.get(1))
    #
    #     if ret is True:
    #         if frame_range:
    #             assert isinstance(frame_range, tuple) or isinstance(frame_range, list)
    #             if frame_range[0] <= frame_number <= frame_range[1]:
    #                 cv2.imshow('Frame', frame)
    #             else:
    #                 continue
    #         else:
    #             cv2.imshow('Frame', frame)
    #     else:
    #         break
    #
    # vid_capture.release()
    # # Closes all the frames
    # cv2.destroyAllWindows()

    ## B
    # os.add_dll_directory('D:\\VLC')
    # media_player = MediaPlayer()
    # media = Media("VID.mp4")
    # media_player.set_media(media)
    # media_player.play()

    ## C
    # play_vlc(input_video, frame_range)
    #
    ## make offset to capture right frame
    # if frame_range:
    #     if frame_range[0] > 50:
    #         frame_range = [frame_range[0] + 50, frame_range[1] + 56]

    p = Process(target=play_opencv, args=(input_video, frame_range, fps, video_speed, points,))
    p.start()
    if wait:
        p.join()
    # if frame_range:
    #     time.sleep((frame_range[1] - frame_range[0]) / (fps * video_speed))
    #     # time.sleep(max(5, (frame_range[1] - frame_range[0]) / (fps * video_speed)))
    #     p.terminate()

    ## D
    # play_vlc(input_video, frame_range)

    ## NOT WORKING
    # p = Process(target=play_vlc, args=(input_video, frame_range,))
    # p.start()
    # p.join()
    # print("hello")

    # E
    # play_vlc2(input_video, frame_range)

    ## NOT WORKING
    # p = Process(target=play_vlc2, args=(input_video, frame_range,))
    # p.start()
    # p.join()
    # print("hello")


def annotate_video(input_video, output_video, traces, frame_offset, video_frame_offset=0, crop_offset=(0, 0)):
    """ Annotates given video with the tracked position of individual bees.

    :arg input_video: (Path or str): path to the input video
    :arg output_video: (Path or str): path to the input video
    :arg traces: (list): a list of Traces
    :arg frame_offset: (int): number of the first frame cause opencv sees the first frame as 0th
    :arg video_frame_offset: (int): number of first frames to cut from original video
    :arg crop_offset: (tuple): a pair of pints, a vector to offset the location in order to match the input video
    """
    print(colored("ANNOTATES THE VIDEO WITH NEW TRACES", "blue"))

    ## TODO manage input and output
    # input_video = 'Resources/Cars.mp4'
    # output_video = '../output/video/output_video_from_file.mp4'

    for trace in traces:
        assert isinstance(trace, Trace)

    # PARAMS
    len_of_trace_shown_behind = 30  # number of frames the path is shown

    # Create a video capture object, in this case we are reading the video from a file
    vid_capture = cv2.VideoCapture(input_video)

    if vid_capture.isOpened() is False:
        print("Error opening the video file")
    # Read fps and frame count
    else:
        # Get frame rate information
        # You can replace 5 with CAP_PROP_FPS as well, they are enumerations
        fps = vid_capture.get(5)
        print('Frames per second : ', fps, 'FPS')

        # Get frame count
        # You can replace 7 with CAP_PROP_FRAME_COUNT as well, they are enumerations
        frame_count = vid_capture.get(7)
        print('Frame count : ', frame_count)

    # Obtain frame size information using get() method
    frame_width = int(vid_capture.get(3))
    frame_height = int(vid_capture.get(4))
    frame_size = (frame_width, frame_height)
    fps = int(vid_capture.get(5))
    # Initialize video writer object

    output = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'XVID'), fps, frame_size)

    ## INITIALISE ANNOTATION
    locations_of_traces = []
    colors = distinctipy.get_colors(len(traces))
    colors = list(map(lambda x: [round(x[0]*255), round(x[1]*255), round(x[2]*255)], colors))
    print("traces colours (R,G,B):", colors)
    for trace in traces:
        locations_of_traces.append([])

    while vid_capture.isOpened():
        # vid_capture.read() methods returns a tuple, first element is a bool
        # and the second is frame
        ret, frame = vid_capture.read()

        frame_number = int(vid_capture.get(1)) - video_frame_offset + frame_offset
        # print("frame_number", frame_number)

        # print("frame_number to look at in locations", frame_number)

        if int(vid_capture.get(1)) < video_frame_offset:
            vid_capture.set(cv2.CAP_PROP_POS_FRAMES, video_frame_offset)
            # print("pass")
            # continue

        ## TODO uncomment this to annotate only first 50 frames - for development purpose
        # if frame_number > 50 + frame_offset:
        #     # print("over")
        #     vid_capture.release()
        #     output.release()
        #     return

        if ret == True:
            ## TODO, uncomment to see the frame
            # cv2.imshow('Frame', frame)

            ## ANNOTATION
            # Round the position to whole pixels
            for trace_index, trace in enumerate(traces):
                try:
                    location_index = trace.frames_list.index(frame_number)
                except ValueError as err:
                    continue
                pointA = list(map(lambda x: round(x), to_vect(crop_offset, trace.locations[location_index])))

                # cv2.line(frame, pointA, pointB, (255, 255, 0), thickness=3, lineType=cv2.LINE_AA)
                try:
                    cv2.circle(frame, pointA, 4, colors[trace_index], thickness=-1, lineType=cv2.LINE_AA)
                except:
                    print(pointA)

                locations_of_traces[trace_index].append(pointA)
                for index, point in enumerate(locations_of_traces[trace_index]):
                    if index == 0:
                        continue
                    try:
                        cv2.line(frame, locations_of_traces[trace_index][index-1], point, colors[trace_index], thickness=1, lineType=cv2.LINE_AA)
                    except IndexError as err:
                        print("index", index)
                        print(len(locations_of_traces[trace_index]))
                        raise err

                if len(locations_of_traces[trace_index]) > len_of_trace_shown_behind:
                    del locations_of_traces[trace_index][0]

            # Write the frame to the output files
            output.write(frame)

            # 20 is in milliseconds, try to increase the value, say 50 and observe
            # make a queue of length 20
            ## TODO MAYBE UNCOMMENT THIS
            # key = cv2.waitKey(1)
            #
            # if key == ord('q'):
            #     break
        else:
            break

    # Release the objects
    vid_capture.release()
    output.release()
    print("Finished annotation.")


def make_help_video():
    """ Annotates given video with the tracked position of individual bees.
    """
    print(colored("ANNOTATES THE VIDEO WITH NEW TRACES", "blue"))

    # Create a video capture object, in this case we are reading the video from a file
    vid_capture = cv2.VideoCapture(r"../test/help_input.mp4")

    if vid_capture.isOpened() is False:
        print("Error opening the video file")
    # Read fps and frame count
    else:
        # Get frame rate information
        # You can replace 5 with CAP_PROP_FPS as well, they are enumerations
        fps = vid_capture.get(5)
        print('Frames per second : ', fps, 'FPS')

        # Get frame count
        # You can replace 7 with CAP_PROP_FRAME_COUNT as well, they are enumerations
        frame_count = vid_capture.get(7)
        print('Frame count : ', frame_count)

    # Obtain frame size information using get() method
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
            if key == ord('q'):
                break
        else:
            break

    # Release the objects
    vid_capture.release()
    output.release()
    print("Finished annotation.")


def align_the_video(traces, video_file, population_size, real_whole_frame_range, csv_file):
    """ User guided alignment of the video onto its not cropped version

    :arg traces (list) list of traces
    :arg video_file: (Path or str): path to the input video
    :arg population_size: (int): population size of original traces
    :arg real_whole_frame_range: (tuple of int): frame range of the video
    :arg csv_file: (str or Path): path to the csv_file
    :return: vector of shift to assign to the locations so that align with the not cropped video
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

    da_frame = 0
    points = []
    for trace in traces:
        assert isinstance(trace, Trace)
        if is_in([da_frame, da_frame], trace.frame_range):
            points.append(trace.get_location_from_frame(da_frame))

    da_converted_frame = convert_frame_number_back(da_frame, csv_file)

    show_video(input_video=video_file, frame_range=[da_converted_frame, da_converted_frame], wait=True, points=points)

    with open("../auxiliary/point.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        if "points assigned:" in line:
            assigned_points = line.split(":")[1]
        if "frame:" in line:
            offset_frame = int(line.split(":")[1])

    assigned_points = json.loads(assigned_points)
    leftmost_point, a = get_leftmost_point(points)
    leftmost_assigned_point, b = get_leftmost_point(assigned_points)
    leftmost_assigned_point = list(map(float, leftmost_assigned_point))
    ## TODO - maybe check that all the other points share the vector of transposition
    vector = to_vect(leftmost_point, leftmost_assigned_point)
    vector = list(map(lambda x: -x, vector))

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


if __name__ == "__main__":
    # make_help_video()
    # show_video("../test/help_video.mp4")
    show_video("../test/help_video.mp4", frame_range=(300, 500))
