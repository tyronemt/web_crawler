import re
from bs4 import BeautifulSoup
import urllib
from urllib.parse import urlparse, urlunparse


# GLOBAL VARIABLES
visited_urls = []
valid_netloc = ["ics.uci.edu","cs.uci.edu","stat.uci.edu","informatics.uci.edu"]
skip = ["archive.uci.edu", "intranet.ics.uci.edu", "grape.ics.uci.edu", "evoke.ics.uci.edu", "ganglia.ics.uci.edu", "cbcl.ics.uci.edu"]


# Honor the politeness delay for each site.
# Crawl all pages with high textual information content.
# Detect and avoid infinite traps.
# Detect and avoid sets of similar pages with no information.
# Detect and avoid dead URLs that return a 200 status but no data.
# Detect and avoid crawling very large files, especially if they have low information value.


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    list_links = []
    word_list = []

    if is_valid(url):
        # create urlparse object of url to later access specific parts we need of current URL
        parsed_url = urlparse(url, scheme="https")

        if if_not_crawled(url, resp):
            try:
                 # CITE: https://python.gotrained.com/beautifulsoup-extracting-urls/ 
                 # implemented the algorithm to extract links using beautiful soup from this source
                soup = BeautifulSoup(resp.raw_response.content, "html.parser")
                a_tags = soup.find_all('a')

                # extracting all text from webpage
                text_list = soup.text # returns string of all readable text 
                text_list = text_list.split('\n')

                # tokenize the text on the web page and store it in word_list
                for text in text_list:
                    text = re.sub(r"[^a-zA-Z0-9 :]", " ", text)
                    text_split = text.split()
                    word_list += text_split

                # DO NOT INCLUDE web pages with less than 10 tokens ("too low content")
                if (len(word_list) > 10):
                    update_tokens_file(word_list)
                    update_largest_URL(url, word_list)
                    update_URls_file(url)
                    # iterate through tags to obtain links present on web page
                    for tag in a_tags:
                        list_links.append(urllib.parse.urljoin(urlunparse(parsed_url), tag.get('href')).split('#')[0]) #adding links to list after defragging the URL

            except:
                print("Error processing next URLs")

    return list_links #returns empty list if the URL is crawled or if the URL is not valid


# The 2xx class of status codes indicates the action requested by the client
# was received, understood, and accepted, but 204 indicates no content.
def valid_response_status(respo):
    return 200<=respo.status<=299 and respo.status != 204


def is_valid(url):
    try:
        parsed = urlparse(url)

        if isValid_netloc(parsed) == False:
            return False

        if parsed.scheme not in set(["http", "https"]):
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico|calendar|events|event|img|apk|jpg|svg|txt|.py|rkt"
            + r"|png|tiff?|mid|mp2|mp3|mp4|json|jpeg"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1|odc"
            + r"|thmx|mso|arff|rtf|jar|csv|wp-content|gallery"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise


def if_not_crawled(url, respons):
    if valid_response_status(respons):
        # To ensure consistency in the formats of the URL
        # strings, avoid any extraneous forward slashes.
        if url.endwith("/"):
            url = url.rstrip("/")
        if url in visited_urls:
            return False
        else:
            visited_urls.append(url)
            return True
    else:
        return False


# Ignores the World Wide Web ('www') subdomain if it is part of network locality.
def process_sd(net_loc):
    sd = net_loc
    if "www." in net_loc:
        netloc = net_loc.replace("www.", "")
        return netloc
    return sd


def isValid_netloc(parsed_url):
    netloc = parsed_url.netloc
    sd = process_sd(netloc)

    counter = 0

    # Determines the number of parts that constitute the host name of the URL, which
    # includes domains (first and second levels) and subdomains (subsequent levels),
    # by counting the number of periods. Each part is separated by a period. The
    # number of parts of the host name is thus the number of periods plus one.
    for element in str(netloc):
        if element == ".":
            counter += 1

    # If the number of parts is greater than three, remove
    # the lowest-level domain (first part) of the URL.
    if counter >= 3:
        netloc_parts = netloc.split(".")
        netloc_parts.pop(0)
        sd = ".".join(netloc_parts)

    if "/department/information_computer_sciences" in parsed_url.path:
        return True
    # Avoids pages like https://www.ics.uci.edu/~smcaleer/publications.html,
    # as it contains traps in the form of PDF files.
    elif (netloc == "ics.uci.edu" and "publications" in parsed_url.path):
        return False
    if netloc in skip:
        return False
    elif sd in valid_netloc:
        return True
    else:
        return False


# helper function that writes into URLs_file to store unique urls we encounter
def update_URls_file(url):
    # open file to append data at end
    URLs_file = open("URLs.txt", 'a', encoding='utf-8')
    # update file
    URLs_file.write(url + '\n')
    # close existing file
    URLs_file.close()


# helper function that writes into largest_URL to store the current standing largest_url
def update_largest_URL(url, word_list):
    # open file to append data at end
    largest_URL = open("largest_URL.txt", 'a', encoding='utf-8')
    # update file
    largest_URL.write(url + '\n' + str(len(word_list)) + '\n')
    # close existing file
    largest_URL.close()


# helper function that writes into tokens_file to store all current tokens
def update_tokens_file(word_list):
    # open file to append data at end
    tokens_file = open("tokens.txt", 'a', encoding='utf-8')
    # update file
    tokens_file.write(str(word_list) + '\n')
    # close existing file
    tokens_file.close()
