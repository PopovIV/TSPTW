from task import task
from antSolver import antSolver

if __name__ == "__main__":

    # get task 
    t = task("report.txt")

    if t.isInit is False:
        print("Error in parse")
    else:
        # solve task with ant method
        solver = antSolver(t)
        print("Ant method solution:")
        solution, cost, time = solver.solve()
        print("Towns to visit in order:")
        print(solution)
        print("Total cost of path:")
        print(cost)
        print("Total time of path:")
        print(time)