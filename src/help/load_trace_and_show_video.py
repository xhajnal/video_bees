import os

import analyse
import trace
from dave_io import load_traces


if __name__ == "__main__":
    os.chdir("..")
    traces_file = '../data/Video_tracking/190822/parsed/20190822_141925574_1bee_generated_20210504_081658_nn.p'
    traces = load_traces(traces_file)

    for trace in traces:
        if trace.trace_id == 24:
            print(trace)

    traces_file = '../data/Video_tracking/190822/after_first_run/6619924870081120246/20190822_141925574_1bee_generated_20210504_081658_nn.p'
    traces = load_traces(traces_file)

    for trace in traces:
        if trace.trace_id == 24:
            print(trace)
