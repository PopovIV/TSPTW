from collections import Counter, defaultdict
from pathlib import Path
from pprint import pprint
from timeit import timeit
import signal

from src import utils, b_cl, b_op
from task import task
from antSolver import antSolver
from backtrack import backtrack


class TimeoutException(Exception):  # Custom exception class
    pass


def timeout_handler(signum, frame):  # Custom signal handler
    raise TimeoutException


# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)

if __name__ == "__main__":

    import os

    _dir = "../test_data"
    d = defaultdict(list)
    algs = [backtrack, b_op.backtrack, b_cl.backtrack]
    for _, _, files in os.walk(_dir):
        for file in files:
            t = task(Path(f"{_dir}/{file}"))
            # fine-tuning the tests
            c_num = len(t.openTime)  # number of clients in the current test file
            time = 0
            max_t = 5
            for alg in algs:
                signal.alarm(max_t)
                try:
                    time = timeit("alg(t)", number=1, globals=globals())
                except TimeoutException:
                    time = max_t
                    continue
                else:
                    signal.alarm(0)
                finally:
                    d[(c_num, file)].append(time)
    # pprint(d)
    cumm = [[], [], []]
    c_umm = [[], [], []]
    for key in sorted(d):
        if not [max_t] * len(d[key]) == d[key]:
            print(f"{key[1].replace('_',f'{chr(92)}_')} & {key[0]} & {' & '.join(map(lambda t: f'>{t}'if t == max_t else f'{t:.6f}', d[key]))} \\\\")
            for r, c in enumerate(d[key]):
                c_umm[r].append(c)
                if c != max_t:
                    cumm[r].append(c)
    # exceeding
    print(" & ".join(map(lambda t: f"{sum(t) / len(t):.6f}", c_umm)))
    # non exceeding
    print(" & ".join(map(lambda t: f"{sum(t) / len(t):.6f}", cumm)))
