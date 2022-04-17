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
            if(j not in res and C[lastIndex][j] < smallestCost):
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
