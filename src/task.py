from pathlib import Path

class task:

    # constructor
    def __init__(self, filename: Path):
        *c, open_times, close_times = [[*map(float, line.split())] for line in open(filename, "r").readlines()]
        assert len(c) == len(open_times) and len(c) == len(close_times), "Invalid data: different dimensions"
        self.C = c
        self.openTime = open_times
        self.closeTime = close_times
