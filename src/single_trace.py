from termcolor import colored
from config import get_bee_max_step_len
from misc import delete_indices


def single_trace_checker(traces):
    """ Checks a single trace.

    :arg traces: (list): a list of Traces
    """
    print(colored("SINGLE TRACE CHECKER", "blue"))
    traces_with_zero_len_in_xy = []
    for index, trace in enumerate(traces):
        print(colored(f"{trace}", "blue"))
        if trace.trace_length == 0:
            print(colored("This trace has length of 0 in x,y. Gonna delete trace of this agent!", "red"))  ## this can be FP
            traces_with_zero_len_in_xy.append(index)
        if trace.max_step_len > get_bee_max_step_len():
            print(colored(f"This agent has moved {trace.max_step_len} in a single step on frame {trace.max_step_len_frame_number}, you might consider fixing it!", "yellow"))
        print()

    # DELETING TRACES WITH 0 LEN in XY
    traces = delete_indices(traces_with_zero_len_in_xy, traces)
    return traces
