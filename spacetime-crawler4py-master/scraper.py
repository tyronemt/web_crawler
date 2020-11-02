import re
from urllib.parse import urlparse, urldefrag
from bs4 import BeautifulSoup

visited = []
valid_netloc = ["ics.uci.edu","cs.uci.edu", "stat.uci.edu","informatics.uci.edu"]

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]




# def extract_next_links(url, resp):
#     output_list = list()
#     try:
#         parsed_url = urlparse(url)
        
#         d = "https://" + parsed_url.netloc
#         if is_valid(url) and if_not_crawled(url) and valid_response_status(resp):
#             print("in if statement")
#             html_content = resp.raw_response.content
#             soup = BeautifulSoup(html_content, "html.parser") #https://python.gotrained.com/beautifulsoup-extracting-urls/ implemented the algorithm to extract links using beautiful soup from this source
#             a_tags = soup.find_all('a')
#             for tag in a_tags:
#                 print(tag)
#                 link  = tag.get('href') #extracts the links
#                 link2 = urllib.parse.urljoin(d, link)
#                 output_list.append(urldefrag(link2)[0]) #adding links to list
#                 print("here")
#     except:
#         print("error extracting next link")
#     return output_list

def extract_next_links(url, resp):
    try:
        if is_valid(url) and if_not_crawled(url) and valid_response_status(resp):
            output_list = list()
            html_content = resp.raw_response.content
            soup = BeautifulSoup(html_content, "lxml") #https://python.gotrained.com/beautifulsoup-extracting-urls/ implemented the algorithm to extract links using beautiful soup from this source
            a_tags = soup.find_all('a')
            for tag in a_tags:
                link  = tag.get('href') #extracts the links
                output_list.append(link) #adding links to list
            return output_list
    except:
        print("error extracting next link")


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



def if_not_crawled(url):
    if url[-1] == "/":
        if url not in visited:
            visited.append(url[:-1])
            return True
        else:
            return False
    else:
        if url not in visited:
            visited.append(url)
            return True
        else:
            return False



def check_netloc(parsed_url):

    netloc = parsed_url.netloc 
    netloc = netloc.strip("www.")

    sd = ".".join(netloc.split("."))

    if len(netloc.split(".")) >= 4:
        sd = ".".join(netloc.split(".")[1:])
        

    if netloc == "today.uci.edu" and "/department/information_computer_sciences" in parsed_url.path:
        return True
    
    if netloc == "wics.ics.uci.edu" and "/events" in parsed_url.path:
        return False

    if netloc == "hack.ics.uci.edu" and "gallery" in parsed_url.path:
        return False

    if (netloc == "grape.ics.uci.edu") or (netloc == "intranet.ics.uci.edu") or (netloc == "archive.ics.uci.edu"):
        return False
    
    for i in valid_netloc:
        if sd == i:
            return True

