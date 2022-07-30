from termcolor import colored
from config import get_bee_max_step_len


def single_trace_checker(traces):
    """ Checks a single trace.

    :arg traces: (list): a list of Traces
    """
    print(colored("SINGLE TRACE CHECKER", "blue"))
    for index, trace in enumerate(traces):
        print(colored(f"{trace}", "blue"))
        if trace.trace_length == 0:
            print(colored("This trace has length of 0 in x,y. Consider deleting this agent!", "red"))  ## this can be FP
        if trace.max_step_len > get_bee_max_step_len():
            print(colored(f"This agent has moved {trace.max_step_len} in a single step on frame {trace.max_step_len_frame_number}, you might consider fixing it!", "yellow"))
        print()
