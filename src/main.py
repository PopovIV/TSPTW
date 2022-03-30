from parse import read_task

if __name__ == "__main__":
    returnValue = read_task("example.txt")
    if returnValue is None:
        print("Error in parse")
    else:
        C, open, close = returnValue
        print(C)
        print(open)
        print(close)