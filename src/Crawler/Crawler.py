from urllib.parse import parse_qs, unquote, urlparse, urljoin, urlencode
from bs4 import BeautifulSoup
from .request import sessions
from . import __globals__ as var
from base64 import b64encode
from .db import DATABASE
import tldextract

class Crawler:
    def __init__(self, URL, Page = False, db = {}, **REQUEST_INFO) -> None:
        self.tags = var.tags
        self.Page = Page
        self.URLists = set()
        self.FirstURL = urlparse(URL)
        self.LatestURL = self.URL = URL
        REQUEST_INFO.setdefault('timeout', var.TIMEOUT)
        REQUEST_INFO.setdefault('headers', var.USER_AGENT)
    
        self.conn = DATABASE(host = db['HOST'], port = db['PORT'], user = db['USER'], passwd = db['PASSWORD'], db = db['DB'])

        self.table = tldextract.extract(URL).domain

        self.conn.DOMAIN_CREATE_TABLE(self.table)

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
        return

    def Crawler(self,  URL, Page = False, db = {}, **REQUEST_INFO) -> None:
        return Crawler(URL = URL , Page=Page, db=db, **REQUEST_INFO)

    def __del__(self) -> dict:
        del self.REQUESTS
    
    def GetLinks(self, url = None) -> None:
        REQUESTS_URL = self.URLJOIN(url)
        print(REQUESTS_URL)

        if REQUESTS_URL:
            if self.FirstURL.netloc == urlparse(REQUESTS_URL).netloc:
                if self.Page:
                    REQ = self.REQUESTS.driver_set(REQUESTS_URL)
                else:
                    REQ = self.REQUESTS.sess_set_get(REQUESTS_URL)
                if self.URL != REQ['url']:
                    self.LatestURL = REQ['url']

                soup = BeautifulSoup(REQ['body'], 'html.parser')
                for attribute, TagName in self.tags.items():
                    for element in soup.find_all(TagName):
                        if attribute in element.attrs:
                            if self.QueryStringValuEmpty(element.attrs[attribute]) not in self.URLists:
                                NEWLink = element.get(attribute)
                                tmp = self.QueryStringValuEmpty(NEWLink)
                                self.conn.URL_INSERT(f"INSERT INTO {self.table}(first_url, last_url, empty_url, body) SELECT '{self.URL}', '{self.URLJOIN(NEWLink)}', '{tmp}','{b64encode(REQ['body'].encode()).decode()}' FROM dual WHERE not exists(SELECT '' FROM {self.table} where empty_url='{tmp}');")
                                self.URLists.add(tmp)
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

# a = Crawler('http://localhost/wordpress', Page = True, db={
#     'HOST':'localhost',
#     'PORT':3306,
#     'USER':'root',
#     'PASSWORD':'autoset',
#     'DB':'fuzzing'
# })
# a()