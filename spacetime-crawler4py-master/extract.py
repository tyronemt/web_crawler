
def unique(url_text_file):
    s = ()
    file = open("answer.txt", "a", encoding = "utf-8")
    file2 = open(url_text_file,"a", encoding = "utf-8")

    for urls in file2:
        s.add(urls.rstrip("\n"))

    l = len(s)

    file.write("# of unique urls: " + str(l) + "\n")
    file.close()
    file2.close()

def longest(url_text_file):
    lst =[]
    file = open("answer.txt", "a", encoding = "utf-8")
    file2 = open(url_text_file,"a", encoding = "utf-8")
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
        i += 1

    file.write("Longest Page URL: " + str(longest) + "\n")
    file.write("Length of Longest Page: " + str(length) + "\n")
    file.close()




if __name__ == "__main__":
    unique("unique_URLs.txt")
    longest("longest_page.txt")