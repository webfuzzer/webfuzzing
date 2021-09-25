from urllib.parse import parse_qs, quote, unquote, urlparse, urlunparse, urljoin, urlencode
from bs4 import BeautifulSoup
from request import sessions
from __globals__ import *

class URL:
    def __init__(self, URL, Page = False, **REQUEST_INFO) -> None:
        self.tags = tags

        REQUEST_INFO.setdefault('timeout', TIMEOUT)
        REQUEST_INFO.setdefault('headers', USER_AGENT)
        self.REQUEST_INFO = REQUEST_INFO
        self.URL = URL
        self.Redirect = URL
        self.Page = Page
        self.FirstURL = urlparse(URL)
        
        if Page:
            self.REQUESTS = sessions(URL, **REQUEST_INFO)
            self.TMP_REQUEST = self.REQUESTS.webdriver()
        else:
            self.REQUESTS = sessions(URL, **REQUEST_INFO)
            self.TMP_REQUEST = self.REQUESTS.get()

    def __call__(self) -> dict:
        pass

    def __del__(self) -> dict:
        del self.REQUESTS