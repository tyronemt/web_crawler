
def unique(url_text_file):
    s = ()
    file = open("answer.txt", "a", encoding = "utf-8")
    file2 = open("url_text_file.txt","a", encoding = "utf-8")

    for urls in file2:
        s.add(urls.strip("\n"))

    l = len(s)

    file.write("# of unique urls: " + str(l) + "\n")
    file.close()
    file2.close()

def longest(url_text_file):
    file = open("answer.txt", "a", encoding = "utf-8")
    file2 = open("url_text_file","a", encoding = "utf-8")





if __name__ == "__main__":
