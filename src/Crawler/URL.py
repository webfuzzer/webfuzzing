from urllib.parse import parse_qs, quote, unquote, urlparse, urlunparse, urljoin, urlencode
from timeit import default_timer as dt
from bs4 import BeautifulSoup
from request import sessions
from __globals__ import *

startime = dt()

__all__ = ['parse_qs', 'quote', 'unquote', 'urlparse', 'urlunparse', 'urljoin', 'urlencode', 'BeautifulSoup']

class URL:
    def __init__(self, URL, Page = False, **REQUEST_INFO) -> None:
        self.tags = tags
        self.Page = Page
        self.URLists = set()
        self.FirstURL = urlparse(URL)
        self.LatestURL = self.URL = URL
        REQUEST_INFO.setdefault('timeout', TIMEOUT)
        REQUEST_INFO.setdefault('headers', USER_AGENT)
        self.REQUEST_INFO = REQUEST_INFO
        self.URLJOIN = (lambda TMPURL: urljoin(self.URL, TMPURL) if TMPURL else None)
        
        if Page:
            self.REQUESTS = sessions(URL, **REQUEST_INFO)
            self.TMP_REQUEST = self.REQUESTS.webdriver()
        else:
            self.REQUESTS = sessions(URL, **REQUEST_INFO)
            self.TMP_REQUEST = self.REQUESTS.sess_get()

    def __call__(self) -> dict:
        self.GetLinks(self.URL)
        return self.URLists

    def Crawler(self, url, **REQUEST_INFO) -> None:
        self.url = url
        if REQUEST_INFO: self.REQUEST_INFO = REQUEST_INFO

        return URL(self.URL, **self.REQUEST_INFO)

    def __del__(self) -> dict:
        del self.REQUESTS
    
    def GetLinks(self, url = None) -> None:
        REQUESTS_URL = self.URLJOIN(url)

        if REQUESTS_URL:
            if self.FirstURL.netloc == urlparse(REQUESTS_URL).netloc:
                if self.Page:
                    REQ = self.REQUESTS.driver_set(REQUESTS_URL)
                else:
                    REQ = self.REQUESTS.sess_get()
                if self.URL != REQ['url']:
                    self.LatestURL = REQ['url']

                soup = BeautifulSoup(REQ['body'], 'html.parser')
                for attribute, TagName in self.tags.items():
                    for element in soup.find_all(TagName):
                        if attribute in element.attrs:
                            if self.QueryStringValuEmpty(element.attrs[attribute]) not in self.URLists:
                                NEWLink = element.get(attribute)
                                self.URLists.add(self.QueryStringValuEmpty(NEWLink))
                                self.GetLinks(NEWLink)

    def QueryStringValuEmpty(self, url) -> str:
        url = self.URLJOIN(url)
        if url:
            URLparse = urlparse(url)
            if self.FirstURL.netloc == URLparse.netloc:
                return url \
                    if not URLparse.query \
                    else \
                        urljoin(
                            self.URL,
                            unquote(
                                urlencode(
                                    dict.fromkeys(
                                        sorted(
                                            parse_qs(URLparse.query)), ''
                                        )
                                    ,doseq=True
                                )
                            )
                        )
        return

C = URL('http://localhost/wordpress/', Page=True)

print(C())

print(dt() - startime)