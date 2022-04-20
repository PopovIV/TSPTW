from pathlib import Path
from pprint import pprint

from task import task
from antSolver import antSolver
from exhaustive import exhaustive
from backtrack import backtrack

if __name__ == "__main__":

    import os
    _dir = "../test_data"

    for _, _, files in os.walk(_dir):
        for file in files:
            # very bad nodes distribution
            if file in {"rc_203.4.txt"}:
                continue
            t = task(Path(f"{_dir}/{file}"))
            # fine-tuning the tests
            s, e = 8, 21  # <- set the desired number of clients (cities)
            c_num = len(t.openTime)  # number of clients in the current test file
            if s <= c_num < e:
                print(f"{file}, # of clients: {c_num}")
                # pprint(exhaustive(t))
                pprint(backtrack(t))
                # print(antSolver(t).solve())
                print()
