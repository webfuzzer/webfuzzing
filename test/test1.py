from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()
def getLinks(url):
    global pages
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.find_all("a"):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)
                
getLinks('https://sir.kr')