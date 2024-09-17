import os

import analyse
import trace
from config import hash_config
from dave_io import load_traces

## TODO here insert your file and given trace id to be loaded
file = "20190822_141925574_1bee_generated_20210504_081658_nn"
trace_id = 24

if __name__ == "__main__":
    os.chdir("..")
    traces_file = f'../data/Video_tracking/190822/parsed/{file}.p'
    traces = load_traces(traces_file)

    for trace in traces:
        if trace.trace_id == trace_id:
            print(trace)

    traces_file = f'../data/Video_tracking/190822/after_first_run/{hash_config()}/{file}.p'
    traces = load_traces(traces_file)

    for trace in traces:
        if trace.trace_id == trace_id:
            print(trace)
