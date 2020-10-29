# Tyrone Tong - tyronet - 31413123

import PartA, os, sys

def common(pathA, pathB):              # Prints out amount of common words and common words in two text files O(N) runtime   
    i = 0
    set_A = set(PartA.computeWordFrequencies(PartA.tokenize(pathA)))
    set_B = set(PartA.computeWordFrequencies(PartA.tokenize(pathB)))
    
    for common in set_A.intersection(set_B):    #O(N)
        print(common)   
        i += 1
    print("There are", i, "words in common.")


if __name__ == "__main__":
    pathA = sys.argv[1]
    if os.path.exists(pathA):
        if pathA.endswith('.txt'):
            pathB = sys.argv[2]
            if os.path.exists(pathB):
                if pathB.endswith('.txt'):
                    common(pathA,pathB)
                else:
                    print("Could not open file:", pathB)
            else:
                print("Could not find file:", pathB)
        else:
            print("Could not open file:", pathA)
    else:
            print("Could not find file:", pathA)