# Tyrone Tong - tyronet - 31413123

from collections import defaultdict
import re, os



def tokenize(path: str): #returns a list of tokens (O(N) runtime)
    lst =[]
    with open(path,encoding='utf8') as txt: 
        for lines in txt:
            lines = lines.rstrip("\n")
            lines = re.sub(r"[^a-zA-Z0-9 :]", " ", lines)
            lines_split = lines.split()
            lst += lines_split
    return lst
    
            
def computeWordFrequencies(lst: list): #takes tokenize list return and returns a map <token,count>, (O(N) runtime)
    dict = defaultdict(int)
    for words in lst:
        dict[words.lower()] += 1
    return dict   


def prnt(map: defaultdict): # prints out the word frequencies map    (O(n log(n)) runtime)
    lst = sorted(map.items(), key=lambda x: -x[1])      # O(n log n)
    for i in lst:                                       # O(N)
        print(i[0],"-", i[1])


if __name__ == "__main__":
    while True:
        path = input("Please input filepath : ")        #takes user inputs
        if path.endswith('.txt'):
            if os.path.exists(path):
                lst = tokenize(path)
                dict = computeWordFrequencies(lst)
                prnt(dict)
            else:
                print("Could not find file:", path)
        else:
            print("Cannot open", path)