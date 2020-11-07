from collections import defaultdict
from urllib.parse import urlparse
 
stop_set = {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as",
             "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't",
             "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
             "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
             "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself",
             "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
             "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of",
             "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
             "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than",
             "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these",
             "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under",
             "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what",
             "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's",
             "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
             "yourself", "yourselves"}
 
 
# extract.py
# File that holds the helper functions that take in text files created/stored
# when scraping to answer analytic questions
 
# answers are subsequently written into "analytics.txt"
 
 
#######               QUESTION 1                #######
#######         how many unique urls?           #######
def unique(url_text_file):
    s = set()   # store URLS in set to avoid duplicates
    file = open("analytics.txt", "a", encoding = "utf-8")
    file2 = open(url_text_file,"r", encoding = "utf-8")
    file.write("Answering Question # 1:" + "\n")
 
    # iterate url_text_file for URL names to store unique URLS 
    for urls in file2:
        s.add(urls.rstrip("\n"))
 
    # write length/# of unique urls into analytics.txt
    file.write("# of unique urls: " + str(len(s)) + "\n\n")
    file.close()
    file2.close()
 
 
#######               QUESTION 2                #######
#######         what was longest page?          #######
def longest(url_text_file):
    file = open("analytics.txt", "a", encoding = "utf-8")
    file2 = open(url_text_file,"r", encoding = "utf-8")
    file.write("Answering Question # 2:" + "\n")
    i = 0           # indexer to check subsequent URLs while iterating
    longest = ""    # stores URL name for current longest page
    temp = ""
    length = 0      # stores length for current longest page
 
    # iterate through each URL for name/corresponding length
    for urls in file2:
        if i == 2:
            i = 0
        if i == 0:
            temp = urls.rstrip("\n")
        if i == 1:
            # if temp is of higher length than the current standing longest page
            # longest page will be temp
            if int(urls.strip("\n")) > length:
                longest = temp
                length = int(urls.strip("\n"))
        i += 1
 
    # write longest page and its length to analytics.txt
    file.write("Longest Page URL: " + str(longest) + "\n")
    file.write("Length of Longest Page: " + str(length) + "\n\n")
    file.close()
 
 
 
#######               QUESTION 3                #######
#######          50 most common words?          #######
def get_50_most(words_file):
    frequencies = defaultdict(int)
    output_file = open("analytics.txt", "a", encoding = "utf-8")
    output_file.write("Answering Question # 3:" + "\n\n")
    output_file.write("50 most common words in the entire set of pages crawled :" + "\n\n")
 
    with open(words_file, 'r', encoding='utf8') as words_file:
        # add a condition where the it will not add the word into the dictionary if it is a stop word.
        for line in words_file:
            line = line.rstrip("\n")
            temp = line.replace("[", "")
            temp2 = temp.replace("]","")
            temp3 = temp2.replace("'","")
            line_split = temp3.split(",")
            for word in line_split:
                if (word.lower()[1:] not in stop_set) and len(word[1:]) > 1 and word[1:].isalpha():
                    frequencies[word.lower()[1:]] += 1 # creates the dict of frequencies in the words file
    counter = 0
    # loops through the sorted dictionary where the largest frequencies are in the front
    for (word,frequency) in sorted(frequencies.items(), key = lambda x: -x[1]):
        if counter < 50: # counter to make sure it doesnt go over 50
            output_file.write(word + "-->" + str(frequency) + "\n")
            counter += 1
        else:
            break
 
 
    output_file.write("\n")
    output_file.close()
 
 
#######               QUESTION 4                #######
#######             # subdomains?               #######
def sort_URLS(url_text_file):
    lst = []
    d = defaultdict(int)
    file = open("analytics.txt", "a", encoding = "utf-8")
    file.write("Answering Question # 4:" + "\n\n")
    # sorts URLs then extracts the ICS subdomains and writes them into answer.txt
    with open(url_text_file, 'r', encoding='utf8') as url_file:
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
 
        file.write("# of subdomains found for 'ics.uci.edu': " + str(len(d.keys())) + "\n\n")
        for k,v in sorted(d.items(), key = lambda x: x[0].lower()):
            file.write(k + " URL #: " + str(v) + "\n")
 
    file.write("\n")
    file.close()
 
 
 
 
if __name__ == "__main__":
    unique("URLs.txt")
    longest("largest_URL.txt")
    get_50_most("tokens.txt")
    sort_URLS("URLs.txt")