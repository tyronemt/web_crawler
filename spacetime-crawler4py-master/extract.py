
def unique(url_text_file):
    print("f")
    s = set()
    file = open("report.txt", "a", encoding = "utf-8")
    file2 = open(url_text_file,"r", encoding = "utf-8")

    for urls in file2:
        s.add(urls.rstrip("\n"))

    l = len(s)

    file.write("# of unique urls: " + str(l) + "\n")
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
    file.write("Length of Longest Page: " + str(length) + "\n")
    file.close()

def sort_URLS(url_text_file):
    counter = 0
    file = open("ics.txt", "a", encoding = "utf-8")
    with open(url_text_file, 'a', encoding='utf8') as url_file: #sorts URLs then extracts the ICS subdomains and writes them into answer.txt
        for url in sorted(url_file):
            if 'ics.uci.edu' in url:
                counter += 1
                file.write(url + " URL #: " + str(counter) +  "\n")
    file.close()



if __name__ == "__main__":
    unique("URLs.txt")
    longest("longest_page.txt")