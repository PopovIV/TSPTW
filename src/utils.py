# closest neighbor method for ant method
# in : C - Costs matrix
# out : list of indexies that represents path 
def closest_neighbor(C):
    res = list()# list of indexies
    N = len(C)# number of cities

    res.append(0)# add first city manually
    for i in range(N):
        lastIndex = res[-1]
        newIndex = 0
        smallestCost = float('inf')
        for j in range(N):
            if j not in res and C[lastIndex][j] < smallestCost :
                newIndex = j
                smallestCost = C[lastIndex][j]
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
#      openTime - array of opem time of towns
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
