from task import task
from antSolver import antSolver
from exhaustive import exhaustive
from backtrack import backtrack

if __name__ == "__main__":

    # get task 
    t = task("example.txt")

    if t.isInit is False:
        print("Error in parse")
    else:
        print(exhaustive(t))
        print(backtrack(t))
        # solve task with ant method
        solver = antSolver(t)
        print("Ant method solution:")
        solution = solver.solve()
        print(solution)