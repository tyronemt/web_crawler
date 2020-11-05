import re
from bs4 import BeautifulSoup
import urllib
from urllib.parse import urlparse


# SETTING GLOBAL VARIABLES
visited_urls = []
valid_netloc = ["ics.uci.edu","cs.uci.edu","stat.uci.edu","informatics.uci.edu"]
skip = ["archive.uci.edu", "intranet.ics.uci.edu", "grape.ics.uci.edu", "evoke.ics.uci.edu", "ganglia.ics.uci.edu", "cbcl.ics.uci.edu"]

no_list =["calendar","events","img","apk", "jpg","css","js","bmp","pptx","doc","docx","xls","data","dat","gif","gz","svg","txt","py","rkt","json","pdf","jpeg","ico","png",
            "mp2","mp3","mp4","wav","avi","mov","pdf","ps","eps","tex","ppt","exe", "odc",
            "tar","msi","bin","psd","dmg","epub","jar","csv","zip","rar","wp-content"]


# Honor the politeness delay for each site
# Crawl all pages with high textual information content
# Detect and avoid infinite traps
# Detect and avoid sets of similar pages with no information
# Detect and avoid dead URLs that return a 200 status but no data (click here to see what the different HTTP status codes mean (Links to an external site.))
# Detect and avoid crawling very large files, especially if they have low information value

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    list_links = []
    word_list = []
    URLs_file = open("URLs.txt", 'a', encoding='utf-8')
    longest_page_file = open("longest_page.txt", 'a', encoding='utf-8')
    content_file = open("content.txt", 'a', encoding='utf-8')

    if is_valid(url):
        parsed_url = urlparse(url)
        d = "https://" + parsed_url.netloc
        if if_not_crawled(url, resp):
            try:
                 # CITE: https://python.gotrained.com/beautifulsoup-extracting-urls/ 
                 # implemented the algorithm to extract links using beautiful soup from this source
                soup = BeautifulSoup(resp.raw_response.content, "html.parser")
                a_tags = soup.find_all('a')

                # extracting all text from webpage
                text_list = soup.text # returns string of all readable text 
                text_list = text_list.split('\n')
                
                for text in text_list:
                    text = re.sub(r"[^a-zA-Z0-9 :]", " ", text)
                    text_split = text.split()
                    word_list += text_split

                # DO NOT INCLUDE web pages with less than 10 tokens ("too low content")
                if (len(word_list) > 10):
                    longest_page_file.write(url + '\n' + str(len(word_list)) +'\n')
                    content_file.write(str(word_list) + '\n')

                    URLs_file.write(url + '\n')
                    # iterate through tags to obtain links present on web page
                    for tag in a_tags:
                        list_links.append(urllib.parse.urljoin(d, tag.get('href')).split('#')[0]) #adding links to list after defragging the URL

            except:
                print("Error processing next URLs")

    # Close openend files           
    URLs_file.close()
    longest_page_file.close()
    content_file.close()

    return list_links #returns empty list if the URL is crawled or if the URL is not valid



def valid_response_status(respo):
    if 200<=respo.status<=299 and respo.status != 204: #status 204 means that theres no content
        return True
    else:
        return False
    
    
def is_valid(url):
    try:
        parsed = urlparse(url)

        if check_netloc(parsed) == False:
            return False
            
        if parsed.scheme not in set(["http", "https"]):
            return False

        for i in no_list:
            if i in parsed.query or i in parsed.path:
                return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

        

    except TypeError:
        print ("TypeError for ", parsed)
        raise



def if_not_crawled(url, respons):
    if valid_response_status(respons):
        if url[-1] == "/":
            if url not in visited_urls:
                visited_urls.append(url[:-1])
                return True
            else:
                return False
        else:
            if url not in visited_urls:
                visited_urls.append(url)
                return True
            else:
                return False
    else:
        return False



def check_netloc(parsed_url):

    netloc = parsed_url.netloc
    if "www." in netloc:
        netloc = netloc.replace("www.", "")

    sd = ".".join(netloc.split("."))

    if netloc.count(".") >= 4:
        sd = ".".join(netloc.split(".")[1:])
    
    if "/department/information_computer_sciences" in parsed_url.path:
        return True
    elif (netloc == "hack.ics.uci.edu" and "gallery" in parsed_url.path) or (netloc == "ics.uci.edu" and "publications" in parsed_url.path):
        return False
    
    for i in skip:
        if netloc == i:
            return False
    
    for i in valid_netloc:
        if sd == i:
            return True

    return False