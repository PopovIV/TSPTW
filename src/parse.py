from pathlib import Path

# Function to read tsptw from file
def read_task(filename : Path):
    C = list()# Costs matrix
    openTime = list()# Town opening time
    closeTime = list()# Town closing time

    with open(filename, "r") as file:
        lines = file.read().splitlines()
    if len(lines) == 0:
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

    return C, openTime, closeTime
