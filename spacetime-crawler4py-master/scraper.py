import re
from bs4 import BeautifulSoup
import urllib
from urllib.parse import urlparse, urldefrag


# SETTING GLOBAL VARIABLES
visited_urls = []
valid_netloc = ["ics.uci.edu","cs.uci.edu", "stat.uci.edu","informatics.uci.edu"]


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
    if is_valid(url):
        parsed_url = urlparse(url)
        d = "https://" + parsed_url.netloc
        if if_not_crawled(url, resp):
            try:
                soup = BeautifulSoup(resp.raw_response.content, "html.parser") #https://python.gotrained.com/beautifulsoup-extracting-urls/ implemented the algorithm to extract links using beautiful soup from this source
                a_tags = soup.find_all('a')
                for tag in a_tags:
                    list_links.append(urllib.parse.urljoin(d, tag.get('href')).split('#')[0]) #adding links to list after defragging the URL
            except:
                print("Error processing next URLs")
    return list_links #returns empty list if the URL is crawled or if the URL is not valid



def valid_response_status(respo):
    if 200<=respo.status<=299 and respo.status != 204:
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


        # if "calendar" in parsed.query or "calendar" in parsed.path:
        #     print("HERE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        #     return False

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
        
    if netloc == "today.uci.edu" and "/department/information_computer_sciences" in parsed_url.path:
        print("HERE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return True

    return False