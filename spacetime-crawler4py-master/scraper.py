import re
from bs4 import BeautifulSoup
import urllib
from urllib.parse import urlparse, urldefrag


# SETTING GLOBAL VARIABLES
visited_urls = []
valid_netloc = ["ics.uci.edu","cs.uci.edu", "stat.uci.edu","informatics.uci.edu"]
# invalid =["css","js","bmp","gif","jpeg","png","mp2",
#         "mp3","mp4","wav","avi","mov","mpeg","pdf","ps","ppt","pptx",
#         "doc","docx","xls","data","dat","exe","tar","msi","bin","psd",
#         "epub","jar","csv","zip","rar","txt","py","rkt", "json", "calendar"]


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    parsed_url = urlparse(url)
    output_list = list()
    d = "https://" + parsed_url.netloc
    if is_valid(url) and if_not_crawled(url, resp):
        soup = BeautifulSoup(resp.raw_response.content, "html.parser") #https://python.gotrained.com/beautifulsoup-extracting-urls/ implemented the algorithm to extract links using beautiful soup from this source
        a_tags = soup.find_all('a')
        for tag in a_tags:
            output_list.append(urllib.parse.urljoin(d, tag.get('href')).split('#')[0]) #adding links to list after defragging the URL
    return output_list



def valid_response_status(respo):
    if 200<=respo.status<=299:
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


        if "calendar" in parsed.query or "calendar" in parsed.path:
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
    netloc = netloc.strip("www.")

    sd = ".".join(netloc.split("."))


    for i in valid_netloc:
        if sd == i:
            return True

    if len(netloc.split(".")) >= 4:
        sd = ".".join(netloc.split(".")[1:])
        
    # if netloc == "wics.ics.uci.edu" and "/events" in parsed_url.path:
    #     return False

    # if netloc == "hack.ics.uci.edu" and "gallery" in parsed_url.path:
    #     return False

    # if (netloc == "grape.ics.uci.edu") or (netloc == "intranet.ics.uci.edu") or (netloc == "archive.ics.uci.edu"):
    #     return False

    if netloc == "today.uci.edu" and "/department/information_computer_sciences" in parsed_url.path:
        return True

    return False