import os
import sys


def getYear(filepath):
    name = filepath.split("_")[-1]
    return name


def main(dir):
    """
    Take all the files from convert.py produce one file for each year
    """
    for i in range(1800, 2017):
        fs = getFiles(dir, i)
        if len(fs) > 0:
            stickTogether(fs, i)


def absoluteFilePaths(directory, year):
    """
    getsthe absolute path to all files in all sub directories in directory
    credit to: http://stackoverflow.com/a/9816863
    """
    return_val = []
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            if int(getYear(f)) == year:
                return_val.append(os.path.abspath(os.path.join(dirpath, f)))
    return return_val


def getFiles(dir, year):
    return absoluteFilePaths(dir, year)


def stickTogether(files, year):
    for i in files:
        store = {}
        getNgrams(i, store)
        writeStore(store, year)


def getNgrams(file, store):
    with open(file) as f:
        for i in f:
            x = i.split(" ")
            year = x[:-3]
            x = x[:-3]
            x = " ".join(x)
            if x in store:
                store[x] += 1
                print(year)
            else:
                store[x] = 1


def writeStore(store, year):
    createDirs("../Final")
    with open("../Final/" + str(year), "w+") as f:
        for i in store:
            f.write(i + " " + str(store[i]) + " 1\n")


def createDirs(saveHere):
    if not os.path.exists(saveHere):
        os.makedirs(saveHere)


if __name__ == "__main__":
    main(sys.argv[1])
