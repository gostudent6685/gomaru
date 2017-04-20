# gomaru-checkup v0.26
# [DONE] get informations of whole episode
# [TODO] save informations to local database
# [TODO] check whether new episode is
# [TODO] use command line arguments
from bs4 import BeautifulSoup as bsoup
from urllib.request import urlopen
from urllib.request import HTTPError
from urllib.request import Request
import re

def make_request_like_browser(url, user_agent=None ,referer=None):
    if user_agent == None:
        """
        More informations about user agent string:
          https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent/Firefox
        """
        user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; rv:10.0) Gecko/20100101 Firefox/10.0"
    chunk = {"User-Agent": user_agent}
    if referer != None:
        chunk["Referer"] = referer
    return Request(URL, headers=chunk)

def get_page(url):
    req = make_request_like_browser(url)
    try:
        html = urlopen(req)
    except HTTPError as e:
        print(e)
        return None
    return html

URL = "http://marumaru.in/b/manga/65484"

try_maximum = 5
for count in range(try_maximum):
    html = get_page(URL)
    if html == None:
        if count+1 < try_maximum:
            print("HTTP Error: trying again...")
            continue
        else:
            print("HTTP Error: exceeded number of attempts")
            exit()
    bsObj = bsoup(html.read(), "html.parser")
    content = bsObj.find("div", {"class":"content"})
    if content != None:
        break
    elif count+1 == try_maximum:
        print("Data Parsing Error: no contents found")
        exit()
        

link_re = "http\:\/\/[a-z]*(\.|)(wasabisyrup|shencomics|yuncomics)\.com\/archives\/[0-9a-zA-Z|\_\-\+]+"
manga_list = content.findAll("a", {"href":re.compile(link_re)})
if manga_list == None:
    print("Data Parsing Error: no contents found")
    exit()
for each_manga in manga_list:
    # " " -> ascii 32 'SP', chr(160) -> 'NBSP'
    text = each_manga.get_text().replace(" ","").replace(chr(160), "")
    if text == "":
        continue
    each_title = each_manga.get_text()
    each_link = each_manga["href"]
    print(each_title + ": " + each_link)
