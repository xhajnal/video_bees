from termcolor import colored
from config import get_bee_max_step_len
from misc import delete_indices


def single_trace_checker(traces, silent=False, debug=False):
    """ Checks a single trace.

    :arg traces: (list): a list of Traces
    :arg silent (bool) if True no output is shown
    :arg debug (bool) if True extensive output is shown
    :returns traces: (list): a list of Traces
    """
    print(colored("SINGLE TRACE CHECKER", "blue"))
    traces_with_zero_len_in_xy = []
    number_of_traces = len(traces)
    for index, trace in enumerate(traces):
        if not silent:
            print(colored(f"{trace}", "blue"))
        if trace.trace_length == 0:
            if not silent:
                print(colored("This trace has length of 0 in x,y. Gonna delete trace of this agent!", "red"))  ## this can be FP
            traces_with_zero_len_in_xy.append(index)
        if trace.max_step_len > get_bee_max_step_len():
            if not silent:
                print(colored(f"This agent has moved {trace.max_step_len} in a single step on frame {trace.max_step_len_frame_number}, you might consider fixing it!", "yellow"))
        if not silent:
            print()

    # DELETING TRACES WITH 0 LEN in XY
    traces = delete_indices(traces_with_zero_len_in_xy, traces)
    print(colored(f"Returning {len(traces)} traces, {number_of_traces - len(traces)} deleted.", "yellow"))
    return traces
