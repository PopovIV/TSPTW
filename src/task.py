from pathlib import Path

class task:
    # constructor
    def __init__(self, filename: Path):
        C = list()# Costs matrix
        openTime = list()# Town opening time
        closeTime = list()# Town closing time
        self.isInit = False # variable to check that parse is successful
        with open(filename, "r") as file:
            lines = file.read().splitlines()
        if len(lines) < 2:# Small hardcode but okay
            return
        townNum = 0
        #fill closeTime
        times = lines.pop(-1).split()
        townNum = len(times)
        closeTime = [int(time) for time in times]
        #fill openTime
        times = lines.pop(-1).split()
        if townNum != len(times):
            return
        openTime = [int(time) for time in times]
        #fill C
        while len(lines) > 0:
            costs = lines.pop(0).split()
            if townNum != len(costs):
                return
            C.append([int(cost) for cost in costs])
        #check sizes
        if len(C) != townNum:
            return

        self.isInit = True
        self.C = C
        self.openTime = openTime
        self.closeTime = closeTime