from urllib.parse import parse_qs, quote, unquote, urlparse, urlunparse, urljoin
from tldextract import extract
from bs4 import BeautifulSoup
from request import *

class Crawler:
    def __init__(self, url, sub = False, scheme='http',**reqinfo) -> None:
        self.tags = {
            'href':['a', 'link', 'area'],
            'src':['img', 'script', 'iframe'],
            'action':['form']
        }
        UserAgent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}

        reqinfo.setdefault('timeout', 3)
        reqinfo.setdefault('headers', UserAgent)


        self.URLists = set()
        self.url = url
        self.redurl = url
        self.sub = sub
        self.reqinfo = reqinfo
        self.MainURLParsing = urlparse(url)

        self.getLinks(self.url)

    def __call__(self) -> dict:
        return self.URLists

    def getLinks(self, url = None) -> dict:

        requrl = self.LinkChecks(url)

        print(self.redurl)

        if requrl:
            try:
                req = requests.get(requrl, **self.reqinfo)
                if self.url != req.url:
                    
                    self.redurl = req.url
                soup = BeautifulSoup(req.text, 'html.parser')

                for attribute, tagname in self.tags.items():
                    for element in soup.find_all(tagname):
                        if attribute in element.attrs:
                            if element.attrs[attribute] not in self.URLists:
                                NewLink = element.get(attribute)
                                self.URLists.add(NewLink)
                                self.getLinks(NewLink)
            except:
                pass

    def LinkChecks(self, url, scheme='http') -> str:

        if url:
            RequestURLString = urljoin(self.redurl, url)
            return RequestURLString

            # tmpurl = urlparse(url)

            # if tmpurl.netloc:
            #     if tmpurl.netloc != self.MainURLParsing.netloc:
            #         return
            # if url[:2] == "//":
            #     RequestURLString = f"{scheme}:{url}"
            # elif url[0] == "#":
            #     RequestURLString = f"{self.redurl}{url}"
            # elif tmpurl.scheme:
            #     RequestURLString = url
            # else:
            #     if tmpurl.path[0] == "/":
            #         RequestURLString = f"{self.url}{tmpurl}"
            #     elif tmpurl.path[:2] == "./":

            #         RequestURLString = f"{self.redurl}{tmpurl[1:]}"
            #     else:
            #         RequestURLString = f"{self.redurl}/{tmpurl}"

            # return RequestURLString
    
C = Crawler('http://localhost')
print(C())