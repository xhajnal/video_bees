from _socket import gethostname
from time import time

from termcolor import colored

import dave

start_time = time()

dave.run(is_first_run=True)
print(colored(f"It took {gethostname()} {round(time() - start_time, 3)} seconds. \n", "green"))
