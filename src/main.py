from collections import Counter, defaultdict
from pathlib import Path
from pprint import pprint
from timeit import timeit
import signal

import utils, b_cl, b_op
from task import task
from antSolver import antSolver
from backtrack import backtrack
import time


class TimeoutException(Exception):  # Custom exception class
    pass


def timeout_handler(signum, frame):  # Custom signal handler
    raise TimeoutException


def antsResearch():
    _dir = "../test_data"
    files = ["rc_206.1.txt", "rc_207.4.txt", "rbg010a.tw", "rc_202.2.txt", "rc_205.1.txt", "rc_203.4.txt", "rbg017.2.tw",
             "rbg017.tw", "rbg016a.tw", "rbg016b.tw", "rbg017a.tw", "rc_203.1.txt", "rbg019a.tw", "rbg019b.tw", "rbg019c.tw",
             "rbg019d.tw", "rbg021.2.tw", "rbg021.3.tw", "rbg021.4.tw", "rbg021.5.tw", "rbg021.6.tw", "rbg021.7.tw", "rbg021.8.tw",
             "rbg021.9.tw", "rbg021.tw", "rc_201.1.txt", "n20w100.003.txt", "n20w20.001.txt", "n20w20.002.txt", "n20w20.003.txt",
             "n20w20.004.txt", "n20w20.005.txt", "n20w40.002.txt", "n20w60.004.txt", "n20w60.005.txt", "n20w80.001.txt", "n20w80.002.txt",
             "rbg020a.tw", "rc_204.3.txt", "rbg027a.tw", "rbg031a.tw", "rbg033a.tw", "rbg034a.tw", "rbg035a.2.tw", "rbg035a.tw", "rbg038a.tw",
             "n40w20.003.txt", "rbg040a.tw", "rbg041a.tw", "rbg042a.tw", "rbg048a.tw", "rbg049a.tw", "rbg050a.tw", "rbg050b.tw", "rbg050c.tw", 
             "rbg055a.tw", "rbg067a.tw", "rbg092a.tw", "rbg125a.tw", "rbg132.2.tw", "rbg132.tw", "rbg152.3.tw", "rbg152.tw", "rbg172a.tw",
             "rbg193.2.tw", "rbg193.tw", "rbg201a.tw", "rbg233.2.tw", "rbg233.tw"]
    #algs = [ants]
    for file in files:
        t = task(Path(f"{_dir}/{file}"))
        # fine-tuning the tests
        c_num = len(t.openTime)  # number of clients in the current test file
        ants = antSolver(t)
        time_start = time.time()
        res = ants.solve()
        time_res = time.time() - time_start
        if res == None:
            continue
        print(f"{file} & {c_num} & {time_res}")

# Change the behavior of SIGALRM
#signal.signal(signal.SIGALRM, timeout_handler)

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