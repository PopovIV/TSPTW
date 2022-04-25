import numpy as np
import random
from task import task
from utils import closest_neighbor
from utils import closest_neighbor_by_open_time
from utils import closest_neighbor_by_close_time
from utils import calculate_path_cost
from utils import calculate_path_time
from utils import check_path
import matplotlib.pyplot as plt

# global variables of algorithm
n = 2000 # number of iterations
m = 20 # number of ants
# curvature factors
delta = 0.01
alpha = 0.01
# heuristic coefficients
beta = 0.4
gamma = 0.6
# pheromone renewal coefficients
z = 0.1
p = 0.1
# path selection factor
q0 = 0.7

# ant method solver class 
class antSolver:

    #constructor
    def __init__(self, t : task):
        self.t = t

    # main method to solve task
    # out : solution path + sum of path + total time
    def solve(self):
        # find first path by closest neighbor method
        openTime = self.t.openTime# Town opening time
        closeTime = self.t.closeTime# Town closing time
        C = self.t.C# matrix cost
        N = len(C)# number of cities
        path = closest_neighbor_by_close_time(closeTime)
        # calculate pheromone matrix
        if check_path(C, openTime, closeTime, path) == False:
            print("bad first path")
            pheromone = N * n
        else:
            print("First path: " + str(path) + " with cost: " + str(calculate_path_cost(C, path)))
            pheromone = N * calculate_path_cost(C, path)
        pheromoneMatrix = [[1 / pheromone] * N for i in range(N)]# matrix of pheromones on roads
        delta_pheromone = pheromone
        # main cycle begins
        lastImprovement = 0
        iteration = 0
        globalSolution = path
        while True:
        #for iteration in range(n):
            localSolutions = list()
            for ant in range(m):
                localSolution = list()
                localSolution.append(0)
                curTime = openTime[0]# current time in path
                curTown = 0# index of town where we are
                townsToVisit = [i for i in range(1, N)]# indexies of towns to visit
                
                while(len(townsToVisit) != 0):
                    # calculate medians
                    d = s = 0
                    for townIndex in townsToVisit:
                        timeToTown = curTime + C[curTown][townIndex]
                        F = closeTime[townIndex] - timeToTown
                        if F >= 0:
                            d += F
                        W = openTime[townIndex] - timeToTown
                        if W > 0:
                            s += W
                    d /= len(townsToVisit)
                    s /= len(townsToVisit)
                    # calculate local heuristics (in fact find town with the most coef)
                    maxCoef = -1
                    bestChoice = 0
                    arrayOfCoef = list()
                    for townIndex in townsToVisit:
                        # local heuristics
                        f = w = 0
                        timeToTown = curTime + C[curTown][townIndex]
                        F = closeTime[townIndex] - timeToTown
                        if F >= 0:
                            f = 1 / (1 + np.exp(delta * (F - d)))
                        W = openTime[townIndex] - timeToTown
                        if W > 0:
                            w = 1 / (1 + np.exp(alpha * (W - s)))
                        else:
                            w = 1
                        # coef to select this town
                        p = pheromoneMatrix[curTown][townIndex] * (f ** beta) * (w ** gamma)
                        if(p > 0):
                            arrayOfCoef.append(p)
                        if(p > maxCoef):
                            maxCoef = p
                            bestChoice = townIndex
                    #check if no town was good to visit
                    if maxCoef == 0:
                        break
                    #calculate random choice
                    if len(arrayOfCoef) == 0:
                        randomChoice = bestChoice
                    else:
                        p = random.randint(0, len(arrayOfCoef) - 1)
                        randomChoice = townsToVisit[p]

                    q = random.uniform(0, 1)
                    if q > q0:
                        nextTown = randomChoice
                    else:
                        nextTown = bestChoice
                    localSolution.append(nextTown)
                    townsToVisit.remove(nextTown)
                    if curTime + C[curTown][nextTown] < openTime[nextTown]:
                        curTime = openTime[nextTown]
                    else:
                        curTime += C[curTown][nextTown]
                    curTown = nextTown
                # come back to 0-town
                localSolution.append(0)
                if len(localSolution) != N + 1:
                    continue
                if check_path(C, openTime, closeTime, localSolution) == False:
                    continue
                localSolutions.append(localSolution)
                if len(globalSolution) == 0 or calculate_path_cost(C, globalSolution) > calculate_path_cost(C, localSolution):
                    print(f"Next improv at {iteration}:" + str(localSolution) + " with cost: " + str(calculate_path_cost(C, localSolution)) \
                    + " with time: " + str(calculate_path_time(C, openTime, localSolution)))
                    lastImprovement = 0
                    globalSolution = localSolution
            # when all ants finish their roots
            # local rule
            lastImprovement += 1
            iteration += 1
            if lastImprovement == n:
                break
            pheromoneMatrixChanges = [[0] * N for i in range(N)]
            for sol in localSolutions:
                solCost = 1 / calculate_path_cost(C, sol)
                for i in range(len(C)):
                    pheromoneMatrixChanges[sol[i]][sol[i + 1]] += solCost
            for i in range(len(pheromoneMatrix)):
                for j in range(len(pheromoneMatrix)):
                    pheromoneMatrix[i][j] = pheromoneMatrix[i][j] * (1 - z) + z * pheromoneMatrixChanges[i][j]
            #global rule
            if len(globalSolution) == 0:
                continue
            pheromoneMatrixChanges = [[0] * N for i in range(N)]
            solCost = 1 / calculate_path_time(C, openTime, globalSolution)
            for i in range(len(C)):
                pheromoneMatrixChanges[globalSolution[i]][globalSolution[i + 1]] += solCost
            for i in range(len(pheromoneMatrix)):
                for j in range(len(pheromoneMatrix)):
                    pheromoneMatrix[i][j] = pheromoneMatrix[i][j] * (1 - p) + p * pheromoneMatrixChanges[i][j]
        # end of all iterations
        if len(globalSolution) == 0:
            return None
        return globalSolution, calculate_path_cost(C, globalSolution), calculate_path_time(C, openTime, globalSolution)

    def solveWithAnts(self, realSolution):
        cost = calculate_path_cost(self.t.C, realSolution)
        m = 10
        ants = list()
        error = list()
        times = list()
        while True:
            ants.append(m)
            sol = self.solve(m)[1]
            error.append((sol - cost) / cost)
            m += 10
            if(m > 130):
                break

        fig = plt.figure()
        plt.title("График зависимости ошибки от количества муравьев")
        plt.xlabel("Количество муравьев")
        plt.ylabel("Ошибка")
        plt.plot(ants, error)
        plt.grid(True)
        plt.show()
        return ants, error

    def solveWithIterations(self, realSolution):
        cost = calculate_path_cost(self.t.C, realSolution)
        n = 1000
        ants = list()
        error = list()
        times = list()
        while True:
            ants.append(n)
            sol = self.solve(n)[1]
            error.append((sol - cost) / cost)
            n += 50
            if(n > 6000):
                break

        fig = plt.figure()
        plt.title("График зависимости ошибки от количества итераций")
        plt.xlabel("Количество итераций")
        plt.ylabel("Ошибка")
        plt.plot(ants, error)
        plt.grid(True)
        plt.show()
        return ants, error
