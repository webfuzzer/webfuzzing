from urllib.parse import parse_qs, quote, unquote, urlparse, urlunparse, urljoin, urlencode
from bs4 import BeautifulSoup
from request import *

class Crawler:
    def __init__(self, url,**reqinfo) -> None:
        self.tags = {
            'href':['a', 'link', 'area', 'base'],
            'src':['img', 'script', 'iframe', 'embed', 'audio', 'input', 'script', 'source', 'track', 'video'],
            'action':['form'],
            'data':['object'],
        }
        UserAgent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}

        reqinfo.setdefault('timeout', 3)
        reqinfo.setdefault('headers', UserAgent)

        self.URLists = set()
        self.url = url
        self.redurl = url
        self.reqinfo = reqinfo
        self.MainURLParsing = urlparse(url)

    def __call__(self) -> dict:

        self.getLinks(self.url)

        return self.QueryEmpty()

    # def Crawler(self, url, **reqinfo) -> None:
    #     self.url = url

    #     if reqinfo: self.reqinfo = reqinfo

    #     return Crawler(self.url, **reqinfo)

    def getLinks(self, url = None) -> None:

        requrl = self.LinkChecks(url)
        if requrl:
            try:
                req = request(requrl, **self.reqinfo).get()
                
                if req['status'] == 200:

                    if self.url != req['url']:
                        self.redurl = req['url']

                    soup = BeautifulSoup(req['body'], 'html.parser')

                    for attribute, tagname in self.tags.items():
                        for element in soup.find_all(tagname):
                            if attribute in element.attrs:
                                if element.attrs[attribute] not in self.URLists:
                                    NewLink = element.get(attribute)

                                    self.URLists.add(NewLink)
                                    self.getLinks(NewLink)
            except:
                pass

    def LinkChecks(self, url) -> str:
        if url:
            RequestURLString = urljoin(self.redurl, url)
            return RequestURLString

    def QueryEmpty(self) -> set:

        URListTemp = set()

        for url in self.URLists:
            if url:
                URLParams = urlparse(url)

                if URLParams.query:
                    QueryString = parse_qs(URLParams.query)
                    for key in QueryString.keys():
                        QueryString[key] = ''
                    QueryString = unquote(urlencode(dict(sorted(QueryString.items())), doseq=True))
                    UNURL = urljoin(
                        self.url, urlunparse(URLParams._replace(query  = QueryString))
                    )

                    URListTemp.add(UNURL)

        return URListTemp
            
    
C = Crawler('http://localhost')
for i in C():
    print(i)

print("="*50)

for i in C():
    print(i)