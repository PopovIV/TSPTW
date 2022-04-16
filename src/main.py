from task import task

if __name__ == "__main__":

    #get task 
    t = task("report.txt")
    if t.isInit is False:
        print("Error in parse")
    else:
        print(t.C)
        print(t.openTime)
        print(t.closeTime)