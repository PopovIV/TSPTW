import numpy as np
import random
from task import task
from utils import closest_neighbor
from utils import calculate_path_cost
from utils import calculate_path_time
from utils import check_path
# global variables of algorithm
n = 10 # number of iterations
m = 10 # number of ants
# curvature factors
delta = 0.01
alpha = 0.01
# heuristic coefficients
beta = 0.5
gamma = 0.5
# pheromone renewal coefficients
z = 0.1
p = 0.1
# path selection factor
q0 = 0.9

# ant method solver class 
class antSolver:

    #constructor
    def __init__(self, t : task):
        self.t = t

    # main method to solve task
    # out : solution path + sum of path + total time
    def solve(self):
        if self.t.isInit == False:
            return
        # find first path by closest neighbor method
        openTime = self.t.openTime# Town opening time
        closeTime = self.t.closeTime# Town closing time
        C = self.t.C# matrix cost
        N = len(C)# number of cities
        path = closest_neighbor(C)
        # calculate pheromone matrix
        pheromone = N * calculate_path_cost(C, path)
        pheromoneMatrix = [[1 / pheromone] * N for i in range(N)]# matrix of pheromones on roads
        # main cycle begins
        globalSolution = list()
        for iteration in range(n):
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
                    maxCoef = 0
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
                        arrayOfCoef.append(p)
                        if(p > maxCoef):
                            maxCoef = p
                            bestChoice = townIndex
                    #calculate random choice
                    maxCoef = 0
                    randomChoice = 0
                    den = 0
                    for coef in arrayOfCoef:
                        den += coef
                    for i in range(len(arrayOfCoef)):
                        p = arrayOfCoef[i] / den
                        if(p > maxCoef):
                            maxCoef = p
                            randomChoice = townsToVisit[i]
                    # make a move with random generator
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
                if check_path(C, openTime, closeTime, localSolution) == False:
                    continue
                localSolutions.append(localSolution)
                if len(globalSolution) == 0 or calculate_path_cost(C, globalSolution) > calculate_path_cost(C, localSolution):
                    globalSolution = localSolution
            # when all ants finish their roots
            # local rule
            pheromoneMatrixChanges = [[0] * N for i in range(N)]
            for sol in localSolutions:
                solCost = 1 / calculate_path_cost(C, sol)
                for i in range(len(C)):
                    pheromoneMatrixChanges[sol[i]][sol[i + 1]] += solCost
            for i in range(len(pheromoneMatrix)):
                for j in range(len(pheromoneMatrix)):
                    pheromoneMatrix[i][j] = pheromoneMatrix[i][j] * (1 - z) + z * pheromoneMatrixChanges[i][j]

            #global rule
            pheromoneMatrixChanges = [[0] * N for i in range(N)]
            solCost = 1 / calculate_path_cost(C, globalSolution)
            for i in range(len(C)):
                pheromoneMatrixChanges[globalSolution[i]][globalSolution[i + 1]] += solCost
            for i in range(len(pheromoneMatrix)):
                for j in range(len(pheromoneMatrix)):
                    pheromoneMatrix[i][j] = pheromoneMatrix[i][j] * (1 - p) + p * pheromoneMatrixChanges[i][j]

        # end of all iterations
        return globalSolution, calculate_path_cost(C, globalSolution), calculate_path_time(C, openTime, globalSolution)

