import os
import warnings

import analyse
import trace
from config import hash_config
from dave_io import load_traces, get_video_path
from make_video import parse_video_info, show_video
from traces_logic import compute_whole_frame_range, get_video_whole_frame_range


global real_whole_frame_range
global whole_frame_range

## TODO here insert your file, given trace id to be loaded, and given frame range of the video to be seen
file = "20190822_141925574_1bee_generated_20210504_081658_nn"
trace_id = 24
frame_range = (500, 10114)

if __name__ == "__main__":
    os.chdir("..")

    ## LOAD VIDEO
    csv_file_path = f'../data/Video_tracking/190822/{file}.csv'
    video_file, output_video_file, is_video_original = get_video_path(csv_file_path)

    ## LOAD TRACES
    traces_file = f'../data/Video_tracking/190822/parsed/{file}.p'
    traces = load_traces(traces_file)

    for trace in traces:
        if trace.trace_id == trace_id:
            print(trace)

    ## VIDEO COMPUTATION
    real_whole_frame_range = compute_whole_frame_range(traces)
    # Compute frame range margins for visualisation
    whole_frame_range = get_video_whole_frame_range(traces)

    ## OBTAIN VIDEO PARAMETERS
    # VECT - to move the locations according the cropping the video
    # trace_offset - number of first frames of the video to skip

    analyse.trim_offset, analyse.crop_offset = parse_video_info(video_file, traces, csv_file_path)
    video_params = [analyse.trim_offset, analyse.crop_offset] if analyse.crop_offset is not None else None
    if video_params is None:
        warnings.warn(
            f"Video file {video_file} not loaded properly. Check whether the file is located and named properly.")

    ## SHOW THE VIDEO
    show_video(input_video=video_file, traces=traces, frame_range=frame_range, wait=True, points=(),
               video_params=video_params, fix_x_first_colors=2)


    ## LOAD TRACES
    traces_file = f'../data/Video_tracking/190822/after_first_run/{hash_config()}/{file}.p'
    traces = load_traces(traces_file)

    for trace in traces:
        if trace.trace_id == trace_id:
            print(trace)

    ## VIDEO COMPUTATION
    real_whole_frame_range = compute_whole_frame_range(traces)
    # Compute frame range margins for visualisation
    whole_frame_range = get_video_whole_frame_range(traces)

    ## OBTAIN VIDEO PARAMETERS
    # VECT - to move the locations according the cropping the video
    # trace_offset - number of first frames of the video to skip

    analyse.trim_offset, analyse.crop_offset = parse_video_info(video_file, traces, csv_file_path)
    video_params = [analyse.trim_offset, analyse.crop_offset] if analyse.crop_offset is not None else None
    if video_params is None:
        warnings.warn(
            f"Video file {video_file} not loaded properly. Check whether the file is located and named properly.")

    ## SHOW THE VIDEO
    show_video(input_video=video_file, traces=traces, frame_range=frame_range, wait=True, points=(),
               video_params=video_params, fix_x_first_colors=2)
