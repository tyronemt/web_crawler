import re
from urllib.parse import urlparse

visited = []
valid_netloc = ["ics.uci.edu","cs.uci.edu", "stat.uci.edu","informatics.uci.edu"]

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    parsed_url = urlparse(url)
    output_list = list()
    raw_data = resp.raw_response.content
    soup = beautifulSoup(raw_data, "lxml") #https://python.gotrained.com/beautifulsoup-extracting-urls/ implemented the algorithm to extract links using beautiful soup from this source
    a_tags = soup.find_all('a')
    for tag in a_tags:
        link  = tag.find_all('a') #extracts the links
        output_list.append(link)
    return output_list
    


    
    # Implementation requred. #use the URL parameter and use beautiful soup to crawl each link that is embedded in the HTML file for the URL, then return the list of those links 
    return list()

def is_valid(url):
    try:
        parsed = urlparse(url)
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

def if_crawled(url):
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

