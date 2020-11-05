from collections import defaultdict
from urllib.parse import urlparse

def unique(url_text_file):
    s = set()
    file = open("report.txt", "a", encoding = "utf-8")
    file2 = open(url_text_file,"r", encoding = "utf-8")

    for urls in file2:
        s.add(urls.rstrip("\n"))

    l = len(s)

    file.write("# of unique urls: " + str(l) + "\n\n")
    file.close()
    file2.close()

def longest(url_text_file):
    file = open("report.txt", "a", encoding = "utf-8")
    file2 = open(url_text_file,"r", encoding = "utf-8")
    i = 0
    longest = ""
    temp = ""
    length = 0
    for urls in file2:
        if i == 2:
            i = 0
        if i == 0:
            temp = urls.rstrip("\n")
        if i == 1:
            if int(urls.strip("\n")) > length:
                longest = temp
                length = int(urls.strip("\n"))
        i += 1

    file.write("Longest Page URL: " + str(longest) + "\n")
    file.write("Length of Longest Page: " + str(length) + "\n\n")
    file.close()

def sort_URLS(url_text_file):
    lst = []
    d = defaultdict(int)
    file = open("report.txt", "a", encoding = "utf-8")
    with open(url_text_file, 'r', encoding='utf8') as url_file: #sorts URLs then extracts the ICS subdomains and writes them into answer.txt
        for i in url_file:
            lst.append(i.rstrip("\n"))
        
        for url in lst:
            parsed = urlparse(url)
            netloc = parsed.netloc 
            if ("www") in netloc:
                netloc = netloc.strip("www.")
            sd = ".".join(netloc.split("."))

            if len(netloc.split(".")) >= 4:
                sd = ".".join(netloc.split(".")[1:])
            if 'ics.uci.edu' == sd:
                d[netloc] += 1

        for k,v in sorted(d.items(), key = lambda x: x[0].lower()):
            file.write(k + " URL #: " + str(v) + "\n")
                  
    file.write("\n")
    file.close()

def get_50_most(words_file):
    frequencies = defaultdict(int)
    output_file = open("report.txt", "a", encoding = "utf-8")
    stop_words = open("stop_words.txt", "r", encoding = "utf-8")
    stop_list = []
    for line in stop_words: 
        line = line.rstrip("\n")
        stop_list.append(str(line))

    with open(words_file, 'r', encoding='utf8') as words_file:
        for line in words_file: #add a condition where the it will not add the word into the dictionary if it is a stop word.
            line = line.rstrip("\n")
            temp = line.replace("[", "")
            temp2 = temp.replace("]","")
            temp3 = temp2.replace("'","")
            line_split = temp3.split(",")
            for word in line_split:
                if word.lower() not in stop_list and len(word) > 1:
                    frequencies[word.lower()] += 1 #creates the dict of frequencies in the words file
    counter = 0
    for (word,frequency) in sorted(frequencies.items(), key = lambda x: -x[1]): #loops through the sorted dictionary where the largest frequencies are in the front
        if counter < 50: #counter to make sure it doesnt go over 50
            output_file.write(word + "-->" + str(frequency) + "\n")
            counter += 1
        else:
            break
    output_file.write("\n")
    output_file.close()
    stop_words.close()
        


if __name__ == "__main__":
    unique("URLs.txt")
    longest("longest_page.txt")
    get_50_most("content.txt")
    sort_URLS("URLs.txt")