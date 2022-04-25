# closest neighbor method for ant method
# in : C - Costs matrix
# out : list of indexies that represents path
from task import task


def closest_neighbor(C):
    res = list()  # list of indexies
    N = len(C)  # number of cities

    res.append(0)  # add first city manually
    for i in range(N):
        lastIndex = res[-1]
        newIndex = 0
        smallestCost = float('inf')
        for j in range(N):
            if (j not in res and C[lastIndex][j] < smallestCost):
                newIndex = j
                smallestCost = C[lastIndex][j]
        res.append(newIndex)

    return res

# closest neighbor method for ant method by open time
# in: openTime - array of open time of towns
# out : list of indexies that represents path 
def closest_neighbor_by_open_time(openTime):
    res = list()  # list of indexies
    N = len(openTime)  # number of cities

    res.append(0)  # add first city manually
    for i in range(N):
        newIndex = 0
        smallestCost = float('inf')
        for j in range(N):
            if (j not in res and openTime[j] < smallestCost):
                newIndex = j
                smallestCost = openTime[j]
        res.append(newIndex)

    return res

# closest neighbor method for ant method by close time
# in: openTime - array of closed time of towns
# out : list of indexies that represents path 
def closest_neighbor_by_close_time(closeTime):
    res = list()  # list of indexies
    N = len(closeTime)  # number of cities

    res.append(0)  # add first city manually
    for i in range(N):
        newIndex = 0
        smallestCost = float('inf')
        for j in range(N):
            if (j not in res and closeTime[j] < smallestCost):
                newIndex = j
                smallestCost = closeTime[j]
        res.append(newIndex)

    return res

# calculate path cost
# in : C - Costs matrix
#      indexies - path indexies
# out : cost of path
def calculate_path_cost(C, indexies):
    res = 0
    for i in range(len(C)):
        res += C[indexies[i]][indexies[i + 1]]
    return res

# calculate path cost
# in : C - Costs matrix
#      openTime - array of open time of towns
#      indexies - path indexies
# out : time of path
def calculate_path_time(C, openTime, indexies):
    res = 0
    for i in range(len(C)):
        res += C[indexies[i]][indexies[i + 1]]
        if res < openTime[indexies[i + 1]]:
            res = openTime[indexies[i + 1]]
    return res

# really dunno if this function has any point but let it be
# check if solution is corret (no time window errors)
# in : C - Costs matrix
#      openTime - array of opem time of towns
#      closeTime - array of close time of towns
#      indexies - path indexies
# out : true of false - flag that path is correct or not
def check_path(C, openTime, closeTime, indexies):
    curTime = 0
    for i in range(len(C)):
        curTime += C[indexies[i]][indexies[i + 1]]
        if curTime > closeTime[indexies[i + 1]]:
            return False
        if curTime < openTime[indexies[i + 1]]:
            curTime = openTime[indexies[i + 1]]
    return True

def data_converter(dir_path, *, suffix=""):
    """ converts test data from:
            <num of lines>
            <costs matrix with `num of lines` lines>
            <opening time> <closing time>  # for each city
        to:
            <costs matrix with `num of lines` lines>
            <opening times>
            <closing times>

    Changes the original file! To avoid pass a custom suffix

    :param dir_path: path to directory with test data (pass a String, or change the method's body
    :param suffix: additional string to the result file
    :return: void
    """
    import os
    for _, _, files in os.walk(dir_path):
        for file in files:
            if file.startswith("rgb"):
                lines = open(f"{dir_path}/{file}", "r").readlines()[:~1]
                open(f"{dir_path}/{file}", "w").writelines(lines)
            try:
                with open(f"{dir_path}/{file}", "r") as f:
                    c = int(f.readline())
                    mat = []
                    openT, closeT = [], []
                    for _ in range(c):
                        mat.append(f.readline())
                    for _ in range(c):
                        o, c = f.readline().split()
                        openT.append(o)
                        closeT.append(c)
                with open(f"{dir_path}/{file}{suffix}", "w") as f:
                    f.writelines((*mat, " ".join(openT), "\n", " ".join(closeT)))
            except Exception:
                continue

def check_triangularity_rule(t: task):
    """ check whether there is a triangularity rule:
        for two given nodes there is no other node,
        path through which will result in a shorter path

        Let a, b be the two nodes. There is no other node c:
        |a, b| > |a, c| + |c, b|

        c ____ a
         |    /
         |   /
         |  /
         | /
         b

    :param t: task with costs matrix
    :return: none, but prints
    """
    r = range(len(t.C))
    e = 10**(-3)  # tolerance
    for i in r:
        for j in r:
            for k in r:
                if t.C[i][j] > t.C[i][k] + t.C[k][j] + e:
                    print("Aha!", t.C[i][j], t.C[i][k], t.C[k][j], t.C[i][k] + t.C[k][j])
