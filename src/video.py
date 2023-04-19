import json
import os
from _socket import gethostname
from multiprocessing import Process
from os.path import exists
from sys import platform

import cv2
from termcolor import colored

from misc import convert_frame_number_back, is_in, get_leftmost_point, to_vect, get_colors, rgb_to_bgr, get_last_digit
from trace import Trace


def play_opencv(input_video, frame_range, speed, points):
    """ Plays the given video in a new window.

    :arg input_video: (Path or str): path to the input video
    :arg frame_range: (list or tuple): if set shows only given frame range of the video
    :arg speed: ratio of rate, hence default speed is 1
    :arg points: (tuple of points): points to be shown over the video (TO ALIGN THE VIDEO)
    :return:
    """
    video = cv2.VideoCapture(input_video)
    # window name and size
    if "lin" in platform:
        cv2.namedWindow("video", cv2.WINDOW_NORMAL)
    else:
        cv2.namedWindow("video", cv2.WINDOW_AUTOSIZE)
    if frame_range:
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_range[0]-1)

    if points:
        print("Press WASD keys to move point(s) to respective direction, press q to save the alignment and close the window.")
    else:
        print("Press q (while video window) to stop the video, press r to restart, a to rewind, d to forward, - to slow down, + to speed up")

    fps = video.get(5)

    first = True

    if frame_range:
        # print("frame_range", frame_range)
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_range[0])

    # while video.isOpened():
    while True:
        frame_number = int(video.get(1))
        # print(frame_number)
        # ## TODO delete this
        # if frame_range:
        #     if frame_number < frame_range[0]:
        #         # print("setting the frame", frame_range[0])
        #         video.set(1, frame_range[0])
        #         # print("frame set to", int(video.get(1)))

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
                cv2.circle(frame, point, 4, color=colors[get_last_digit(index)], thickness=-1, lineType=cv2.LINE_AA)

        # Display each frame
        if frame_range:
            if frame_range[0] <= frame_number <= frame_range[1]:
                cv2.imshow("video", frame)
        else:
            cv2.imshow("video", frame)
        if str(gethostname()) == "Skadi":
            cv2.resizeWindow("video", 1900, 800)

        key = cv2.waitKey(round(2*(100/fps)/speed))

        if first:
            # time.sleep(3)
            first = False

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

    video.release()
    # Exit and destroy all windows
    cv2.destroyAllWindows()
    if points:
        with open("../auxiliary/point.txt", "w") as file:
            file.write(f"video file: {input_video})\n")
            file.write(f"frame: {frame_range[0]}\n")
            file.write(f"points assigned: {points}\n")

    return points


def show_video(input_video, traces=(), frame_range=(), video_speed=0.1, wait=False, points=(), video_params=True):
    """ Shows given video.

        :arg input_video: (Path or str): path to the input video
        :arg traces: (list): list of Traces
        :arg frame_range: (list or tuple): if set shows only given frame range of the video
        :arg video_speed: (float): ratio of rate, hence default speed is 1
        :arg wait: (bool): if True it will wait for the end of the video
        :arg points: (tuple of points): points to be shown over the video
        :arg video_params: (bool or tuple): if False a video with old tracking is used, otherwise (trim_offset, crop_offset)
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

    if video_speed > 1:
        video_speed = 1

    if points:
        # to show points
        p = Process(target=play_opencv, args=(input_video, frame_range, video_speed, points,))
    else:
        try:
            assert isinstance(video_params, tuple) or isinstance(video_params, list)
        except AssertionError:
            video_params = (0, (0, 0))
        # show traces over
        p = Process(target=annotate_video, args=(input_video, False, traces, frame_range, video_speed, 0, video_params[0], video_params[1], True,))
    p.start()
    if wait:
        p.join()


def annotate_video(input_video, output_video, traces, frame_range, speed=1, trace_offset=0, trim_offset=0, crop_offset=(0, 0), show=False, force_new_video=False, debug=False):
    """ Annotates given video with the tracked position of individual bees.

    :arg input_video: (Path or str): path to the input video
    :arg output_video: (Path or str): path to the input video
    :arg traces: (list): a list of Traces
    :arg frame_range: (list or tuple): if set shows only given frame range of the video
    :arg speed: ratio of rate, hence default speed is 1
    :arg trace_offset: (int): number of the first frames where there is no trace
    :arg trim_offset: (int): number of the first frames to trim from original video
    :arg crop_offset: (tuple): a pair of pints, a vector to offset the location in order to match the input video
    :arg show: (bool): if True showing the frames
    :arg force_new_video: (bool): iff True, a new video will be created, even a video with the same amount of traces is there
    """
    if traces and not show:
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
    for trace in traces:
        assert isinstance(trace, Trace)
        trace_ranges.append(trace.frame_range)

    # PARAMS
    len_of_trace_shown_behind = 30  # number of frames the path is shown behind

    # Create a video capture object, in this case we are reading the video from a file
    video = cv2.VideoCapture(input_video)
    if "lin" in platform:
        cv2.namedWindow("video", cv2.WINDOW_NORMAL)
    else:
        cv2.namedWindow("video", cv2.WINDOW_AUTOSIZE)

    if str(gethostname()) == "Skadi":
        cv2.moveWindow("video", 0, 0)
        cv2.resizeWindow("video", 1900, 800)

    if video.isOpened() is False:
        print(colored("Error opening the video file", "red"))
    else:
        if show:
            print("Press q (while video window) to stop the video, press r to restart, a to rewind, d to forward, - to slow down, + to speed up")

        fps = video.get(5)
        if debug:
            print('Frames per second: ', fps, 'FPS')

        frame_count = video.get(7)
        if debug:
            print('Frame count: ', frame_count)

        if frame_range and debug:
            print('Show frames: ', frame_range)

        # if debug:
        print('Ranges of Traces: ', trace_ranges)

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
    ## TODO fix this as it is SUPER slow for big number of traces
    colors = get_colors(len(traces))
    if debug:
        print("traces colours (R,G,B):", colors)
    colors = list(map(rgb_to_bgr, colors))
    # print("traces colours (G,B,R):", colors)

    for trace in traces:
        ## TODO this can be optimised using queue instead of list
        locations_of_traces.append([])

    video.set(cv2.CAP_PROP_POS_FRAMES, trim_offset)

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

        ## TODO uncomment this to annotate only first 50 frames - for development purpose
        # if output_video and frame_number > 500 + trace_offset:
        #     # print("over")
        #     video.release()
        #     output.release()
        #     return

        if ret == True:
            ## ANNOTATION
            for trace_index, trace in enumerate(traces):
                # if trace_index > 0:
                #     continue

                try:
                    location_index = trace.frames_list.index(frame_number)
                except ValueError as err:
                    continue

                # Round the position to whole pixels
                pointA = list(map(lambda x: round(x), to_vect(crop_offset, trace.locations[location_index])))

                # print(trace_index, trace.trace_id, colors[get_last_digit(trace_index)], pointA)

                # cv2.line(frame, pointA, pointB, (255, 255, 0), thickness=3, lineType=cv2.LINE_AA)
                try:
                    cv2.circle(frame, pointA, 4, color=colors[get_last_digit(trace_index)], thickness=-1, lineType=cv2.LINE_AA)
                except:
                    print(pointA)

                locations_of_traces[trace_index].append(pointA)
                for index, point in enumerate(locations_of_traces[trace_index]):
                    if index == 0:
                        continue
                    try:
                        cv2.line(frame, locations_of_traces[trace_index][index-1], point, color=colors[get_last_digit(trace_index)], thickness=1, lineType=cv2.LINE_AA)
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

                if key == ord('q') or key == ord('Q'):
                    break
                if key == ord('r') or key == ord('R'):
                    if frame_range:
                        video.set(cv2.CAP_PROP_POS_FRAMES, trim_offset + frame_range[0])
                    else:
                        video.set(cv2.CAP_PROP_POS_FRAMES, trim_offset)
                    # locations_of_traces = [[]]*len(traces)
                    locations_of_traces = []
                    for trace in traces:
                        locations_of_traces.append([])

                if key == ord('a') or key == ord('A'):
                    if frame_range:
                        video.set(cv2.CAP_PROP_POS_FRAMES, max(trim_offset + frame_number - 100, trim_offset + frame_range[0]))
                    else:
                        video.set(cv2.CAP_PROP_POS_FRAMES, max(trim_offset + frame_number - 100, trim_offset + 0))
                    # locations_of_traces = [[]]*len(traces)
                    locations_of_traces = []
                    for trace in traces:
                        locations_of_traces.append([])

                if key == ord('d') or key == ord('D'):
                    if frame_range:
                        video.set(cv2.CAP_PROP_POS_FRAMES, min(trim_offset + frame_number + 100, trim_offset + frame_range[1]))
                    else:
                        video.set(cv2.CAP_PROP_POS_FRAMES, min(trim_offset + frame_number + 100, frame_count))

                    # locations_of_traces = [[]]*len(traces)
                    locations_of_traces = []
                    for trace in traces:
                        locations_of_traces.append([])

                if key == ord('+'):
                    speed = 1.1 * speed

                if key == ord('-'):
                    speed = 0.9 * speed

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
    video.release()
    if output_video:
        output.release()
        print(colored("Annotation done.", "yellow"))


def make_help_video(debug=False):
    """ Annotates given video with the tracked position of individual bees.
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
    # there is no video file
    if not video_file:
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
            vect, frame_offset = transpositions[video_file]

        except KeyError:
            # transposition or the file not found, align the video
            vect, frame_offset = align_the_video(traces, video_file, csv_file_path)

        return vect, frame_offset

    else:
        return None, None


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
    show_video(input_video=video_file, traces=(), frame_range=[da_converted_frame, da_converted_frame], wait=True, points=points, video_params=True)

    # READ THE OUTPUT FILE
    with open("../auxiliary/point.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        if "points assigned:" in line:
            assigned_points = line.split(":")[1]
        # if "frame:" in line:
        #     offset_frame = int(line.split(":")[1])

    assigned_points = json.loads(assigned_points)
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


if __name__ == "__main__":
    # make_help_video()
    # show_video(input_video, traces=(), frame_range=(), video_speed=0.1, wait=False, points=(), video_params=True)

    # show_video("../test/help_video.mp4")
    # show_video("../test/help_video.mp4", frame_range=(300, 500), wait=False, video_speed=5)
    # show_video("../test/help_video.mp4", frame_range=(300, 500), video_params=[0, (0, 0)], video_speed=5)
    annotate_video("../test/help_video.mp4", False, (), frame_range=(), speed=1, trace_offset=0, trim_offset=50, crop_offset=(0, 0), show=True)
    # show_video("../test/help_video.mp4", frame_range=(300, 500), video_params=[0, 0, (0, 0)], video_speed=0.5)
