import cv2
import distinctipy

from trace import Trace
## TODO manage input and output


def annotate_video(input_video, output_video, traces, frame_offset):
    """ Annotates given video with the tracked position of individual bees.

    :arg input_video: (Path or str): path to the input video
    :arg output_video: (Path or str): path to the input video
    :arg traces: (list): a list of Traces
    :arg frame_offset: (int): number of the first frame cause opencv sees the first frame as 0th
    """
    for trace in traces:
        assert isinstance(trace, Trace)

    # PARAMS
    len_of_trace_shown_behind = 30

    # Create a video capture object, in this case we are reading the video from a file
    ## TODO manage input here
    vid_capture = cv2.VideoCapture('Resources/Cars.mp4')

    if (vid_capture.isOpened() == False):
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

    ## TODO manage output here
    output = cv2.VideoWriter('Resources/output_video_from_file.mp4', cv2.VideoWriter_fourcc(*'XVID'), fps, frame_size)

    ## INITIALISE ANNOTATION
    locations_of_traces = []
    colors = distinctipy.get_colors(len(traces))
    colors = list(map(lambda x: [round(x[0]*255), round(x[1]*255), round(x[2]*255)], colors))
    print(colors)
    for trace in traces:
        locations_of_traces.append([])

    while (vid_capture.isOpened()):
        # vid_capture.read() methods returns a tuple, first element is a bool
        # and the second is frame
        ret, frame = vid_capture.read()

        frame_number = int(vid_capture.get(1)) + frame_offset
        # print("frame_number", frame_number)

        if ret == True:
            cv2.imshow('Frame', frame)

            ## ANNOTATION
            # Round the position to whole pixels
            for trace_index, trace in enumerate(traces):
                try:
                    location_index = trace.frames_list.index(frame_number)
                except ValueError as err:
                    continue
                pointA = list(map(lambda x: round(x), trace.locations[location_index]))

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
            key = cv2.waitKey(1)

            if key == ord('q'):
                break
        else:
            break

    # Release the objects
    vid_capture.release()
    output.release()
    print("Finished annotation.")
