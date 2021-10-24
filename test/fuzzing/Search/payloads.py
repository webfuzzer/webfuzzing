"""
기본적인 공격 벡터 : header, cookie, post data, get data
"""
from urllib.parse import parse_qs, urlencode, urlparse, urljoin
from string import ascii_letters, digits
from bs4 import BeautifulSoup
from Storage.DB import Engine
from base64 import b64decode
from Crawler import sessions
from random import choice

__all__ = [
    'ReflectedXSS',
    'OpenRedirect',
    'SQLInjection',
    'CrossSiteRequestForgery',
    'NOSQLInjection',
    'OSCommandInjection',
    'ServerSideTemplateInjection',
    'LocalFileInclusion',
    'RemoteFileInclusion'
]

attr = {
    'first_url':1,
    'current_url':2,
    'method':3,
    'history':4,
    'history_len':5,
    'response_url':6,
    'response_cookies':7,
    'response_headers':8,
    'response_status':9,
    'request_cookies':10,
    'request_headers':11,
    'body':12
}

def init_session():
    return sessions()(Site=False)

def RandomString(strlen, digit=True):
    return ''.join([choice(ascii_letters + (digits if digit else '')) for _ in range(0,strlen)])

class OpenRedirect:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL

class ReflectedXSS:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.sess = sessions().init_sess()
        self.info = info
        self.URL = URL
        self.exploit()

    def exploit(self):
        for content in self.crawling_contents:
            self.html = b64decode(content[attr['body']]).decode()
            self.current_url = content[attr['current_url']]
            self.search_text(content[attr['request_headers']], content[attr['request_cookies']])
 
    def search_text(self, headers, cookies):
        # query string
        urinfo = urlparse(self.current_url)
        if urinfo.query:
            qs = parse_qs(urinfo.query)
            for key, value in qs.items():
                if type(value) == list:
                    value = value[0]
                tmp = BeautifulSoup(self.html, 'html.parser')
                if tmp.find_all(text=value):
                    randstr = RandomString(5)
                    qs[key] = randstr
                    r = self.sess.get(urinfo._replace(query=urlencode(qs, doseq=True)).geturl())  
                    if randstr in r.text:
                        soup = BeautifulSoup(r.text, 'html.parser')
                        # inner text
                        if soup.find_all(text=randstr):
                            self.payloads_check('qs', key,qs)
                            break
        # cookies`
        if cookies:
            for key, value in cookies.items():
                tmp = BeautifulSoup(self.html, 'html.parser')
                if tmp.find_all(text=value):
                    randstr = RandomString(5)
                    cookies[key] = randstr
                    r = self.sess.get(self.current_url, cookies=cookies)  
                    if randstr in r.text:
                        soup = BeautifulSoup(r.text, 'html.parser')
                        # inner text
                        if soup.find_all(text=randstr):
                            self.payloads_check('cookie', key,cookies)
                            break
        # headers
        if headers:
            for key, value in headers.items():
                tmp = BeautifulSoup(self.html, 'html.parser')
                if tmp.find_all(text=value):
                    randstr = RandomString(5)
                    headers[key] = randstr
                    r = self.sess.get(self.current_url, headers=headers)
                    if randstr in r.text:
                        soup = BeautifulSoup(r.text, 'html.parser')
                        # inner text
                        if soup.find_all(text=randstr):
                            self.payloads_check('header', key,headers)
                            break

    def payloads_check(self, vector, key, _input = {''}):
        # vector : query string, cookies, headers
        print(self.current_url)
        print(f'{vector} : 취약점 찾은 것 같음')


class SQLInjection:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL

class CrossSiteRequestForgery:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL

class NOSQLInjection:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL

class OSCommandInjection:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL

class ServerSideTemplateInjection:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL

class LocalFileInclusion:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL

class RemoteFileInclusion:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL