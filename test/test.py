from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
from tldextract.tldextract import extract

URLs = set()

tags = {
    'href':['a', 'link', 'area'],
    'src':['img', 'script', 'iframe'],
    'action':['form']
}

user_agent = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}

URL = 'http://localhost'

parsing = urlparse(URL)

def getLinks(url, scheme = 'http'):

    global tags
    global user_agent
    global URL
    global parsing

    tmpurl = urlparse(url)
    
    try:
        if tmpurl.netloc:
            if tmpurl.netloc != parsing.netloc:
                return

        if url[:2] == "//":
            ReqURLString = f"{scheme}:{url}"
        elif url[0] == "#":
            ReqURLString = f"{URL}{url}"
        elif tmpurl.scheme:
            ReqURLString = url
        else:
            if tmpurl.path[0] == "/" or tmpurl.path[:1] == "./":
                if tmpurl.path[0] == "/":
                    ReqURLString = f"{URL}{tmpurl.path}"
                else:
                    ReqURLString = f"{URL}{tmpurl.path[1:]}"
            else:
                ReqURLString = f"{url}/{tmpurl.path}"
        
        print(ReqURLString)

        req = requests.get(ReqURLString)
        soup = BeautifulSoup(req.text, 'html.parser')

        for attribute, tagname in tags.items():
            for element in soup.find_all(tagname):
                if attribute in element.attrs:
                    if element.attrs[attribute] not in URLs:
                        NewLink = element.get(attribute)
                        URLs.add(NewLink)
                        getLinks(NewLink)
    except:
        pass

getLinks(URL, parsing.scheme)