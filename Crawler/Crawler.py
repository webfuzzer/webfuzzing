from urllib.parse import parse_qs, quote, unquote, urlparse, urlunparse, urljoin, urlencode
from timeit import default_timer as dt
from bs4 import BeautifulSoup
from request import *
import sys
sys.setrecursionlimit(10000)

class Crawler:
    def __init__(self, url, req_check = False,**reqinfo) -> None:
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
        self.req_check = req_check
        self.MainURLParsing = urlparse(url)

        if req_check:
            self.reqs = request(url, conf=True)
            self.tmp_req = self.reqs.webdriver()
            self.check = True
            
        else:
            self.reqs = request(url, **self.reqinfo)
            self.tmp_req = self.reqs.get()
            self.check = True

    def __call__(self) -> dict:

        self.getLinks(self.redurl)
        return self.URLists

    def Crawler(self, url, **reqinfo) -> None:
        self.url = url

        if reqinfo: self.reqinfo = reqinfo

        return Crawler(self.url, **reqinfo)

    def getLinks(self, url = None) -> None:

        requrl = self.LinkChecks(url)

        if requrl:
            
            if self.MainURLParsing.netloc == urlparse(requrl).netloc:
                if self.check:
                    if self.req_check:
                        req = self.reqs.driver_set(requrl)
                    else:
                        req = self.reqs.get(requrl)
                else:
                    req = self.tmp_req
                if self.url != req['url']:
                    self.redurl = req['url']
 
                soup = BeautifulSoup(req['body'], 'html.parser')
                for attribute, tagname in self.tags.items():
                    for element in soup.find_all(tagname):
                        if attribute in element.attrs: # self.tags 리스트에 있는 속성이 존재하는지 체크
                            if self.QueryEmpty(element.attrs[attribute]) not in self.URLists: # 파싱한 엘리먼트의 속성(URL)이 self.URLists에 없으면 실행
                                NewLink = element.get(attribute) # URL 수집
                                self.URLists.add(self.QueryEmpty(NewLink)) # URL 추가
                                self.getLinks(NewLink) # 파싱한 URL으로 재귀 호출

    def LinkChecks(self, url) -> str or None:
        if url:
            RequestURLString = urljoin(self.redurl, url)
            return RequestURLString

    def QueryEmpty(self, url = None) -> set:
        if url:
            URLParams = urlparse(urljoin(self.redurl, url))
            if self.MainURLParsing.netloc == URLParams.netloc:
                if URLParams.query:
                    QueryString = parse_qs(URLParams.query)
                    for key in QueryString.keys():
                        QueryString[key] = ''
                    QueryString = unquote(urlencode(dict(sorted(QueryString.items())), doseq=True))
                    UNURL = urljoin(
                        self.url, urlunparse(URLParams._replace(query  = QueryString))
                    )
                    return UNURL
                else:
                    return url

startime = dt()

# C = Crawler('https://developer.mozilla.org/ko/docs/Web', req_check = True)
C = Crawler('https://itwiki.kr/', req_check = True)

print(C())


print(dt() - startime)