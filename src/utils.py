# closest neighbor method for ant method
# in : C - Costs matrix
# out : list of indexies that represents path 
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


# calculate path cost
# in : C - Costs matrix
#      indexies - path indexies
# out : cost of path
def calculate_path_cost(C, indexies):
    res = 0
    for i in range(len(C)):
        res += C[indexies[i]][indexies[i + 1]]
    return res


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
