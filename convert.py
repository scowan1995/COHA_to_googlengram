import sys
import os


def get_paths(file):
    """
    Gets all the paths from a file contaning a list of paths
    params:
    file: a path to a file or None
    """
    if file is None:
        return []
    else:
        ls = []
        with open(file) as f:
            ls.append(f.readline())
        return ls

def createDirs():
    if not os.path.exists("../Converted_files"):
        os.makedirs("../Converted_files")

def main(nlength, desired_word, files=None):
    """
    params:
    files: A file containing a list of paths to the files to convert.
    nlength: the number of words you want to have around the word you are
             searching for. for example with nlenght 7 and desired_word
             mouse you would have n-grams like:
              "the little brown mouse jumped across the"
    desired_word: the word ou are looking for. "mouse" in the example above.
    returns: Nothing but number of converted files will be in the directory
             If you run this of files f1 and f1 you will see:
               convert_f1 and convert_f2 in the same directory
    """
    print("pararms in main:")
    print("nlength: " + str(nlength))
    print("desired_word: " + str(desired_word))
    print("files: " + files)
    createDirs()
    file_paths = get_paths(files)
    left_pad = nlength // 2
    right_pad = nlength - left_pad
    for i in file_paths:
        convert(i, desired_word, left_pad, right_pad)


def build_name(path):
    """
    builds the name of the new converted file from the old file's name
    """
    fname = path.split("/")[-1]  # get the file name from the path
    fname = fname.split("_")  # split the file name in subject, year, id
    fname[-1] = fname[-1][:len(fname[-1])-4]  # remove the .txt
    if len(fname) != 3:
        print("unusual name found: " + path)
        print("will use: " + "_".join(fname))
        return "_".join(fname)
    else:
        new_name = fname[0] + "_" + fname[2] + "_" + fname[1]
        return new_name


def constructGram(line: [str]):
    """ Constructs the ngram from the list of lines given."""
    l = ""
    for i in line:
        if i is not line[len(line)-1]:
            l += getLemma(i) + " "
        else:
            l += getLemma(i)
    return l


def store(ngrams: dict, gram: str):
    """ stores an ngram in a dictionary or updates the counter"""
    if gram in ngrams:
        ngrams[gram] += 1
    else:
        ngrams[gram] = 1


def convert(orig_f, word, left_pad, right_pad):
    """
    converts one particular file into a ngram format
    retruns whther or not the word was found
    """
    file = orig_f.strip("\n")
    new_name = build_name(file)
    ngrams = {}
    with open(file) as f:
        f.readline()
        lines = f.readlines()
        for i in range(len(lines)):
            lemma = getLemma(lines[i])
            if lemma == word:
                if i + right_pad < len(lines):
                    if i - left_pad < 0:
                        gram = constructGram(lines[: i + right_pad])
                    else:
                        gram = constructGram(lines[i - left_pad:
                                                   i + right_pad])
                else:
                    if i - left_pad < 0:
                        gram = constructGram(lines)
                    else:
                        gram = constructGram(lines[i - left_pad:])
                store(ngrams, gram)
    writeStore("../Converted_files/", ngrams, new_name)


def writeStore(path, store, name):
    year = name.split("_")[-1]
    with open(path + name, "w+") as f:
        for i in store:
            f.write(i + " " + str(year) + " " + str(store[i]) + " 1\n")


def getYear(f):
    """
    gets the year from the name of the file.
    Assumes the year follows the coha standard of <catagory>_year_id.tx
    """
    first = -1
    second = -1
    third = -1
    for i in range(len(f)):
        if f[i] == "_":
            if first == -1:
                first = i + 1
            elif second == -1:
                second = i + 1
            else:
                third = i
                break
    return f[second:third]


def getLemma(line):
    """
    retreves the second word in a line in the coha corpus, or nothing if
    given an empty line
    """
    if line == "":
        return ""
    s = line.split("\t")
    return s[1]


if __name__ == "__main__":
    """
    arg1: nlength -- the length of the desired ngram
    arg2: desired word -- the word you are looking for the senses of
    arg3: a list of the files you want
    """
    if sys.argv[1].lower() == "help":
        print("arg1: nlength -- the length of the desired ngram \
               arg2: desired word -- the word you want to search for \
               arg3: a list of the files you want")
    if len(sys.argv) >= 4:
        main(int(sys.argv[1]), sys.argv[2], sys.argv[3])
    else:
        print("\nError: not enough params\n")
