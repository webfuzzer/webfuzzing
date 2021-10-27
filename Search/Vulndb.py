"""
기본적인 공격 벡터 : header, cookie, post data, get data
"""
from urllib.parse import parse_qs, urlencode, urlparse, urljoin
from Search.payloads import fuzzer_payloads
from Utils.utils import RandomString
from bs4 import BeautifulSoup
from base64 import b64decode
from Crawler import sessions

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
    'data':12,
    'body':13
}

def init_session():
    return sessions()(Site=False)

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
            self.search_text(
                headers = content[attr['request_headers']], 
                cookies = content[attr['request_cookies']], 
                data = content[attr['data']],
                method = content[attr['method']],
            )
 
    def search_text(self, *, headers, cookies, data, method):
        """
        if urlparse(self.current_url).query:
            쿼리가 있는 경우 체크
            self.InputValueCheck(parse_qs(urlparse(self.current_url).query), 'qs')
        if cookies:
            self.InputValueCheck(cookies, 'cookies')
        if haders:
            self.InputValueCheck(headers, 'headers')
        """
        self.urinfo = urlparse(self.current_url)
        if self.urinfo.query:
            self.InputValueCheck(method, parse_qs(self.urinfo.query), 'params')
        if data:
            self.InputValueCheck(method, data, 'data')
        if cookies:
            self.InputValueCheck(method, cookies, 'cookies')
        if headers:
            self.InputValueCheck(method, headers, 'headers')

    def InputValueCheck(self, method, _input, space):
        """
        먼저 해당 페이지에 출력이 되어 있는지 체크 한 다음 RandomString(5)를 이용하여 랜덤 값 체크
        """
        for key, value in _input.items():
            soup = BeautifulSoup(self.html, 'html.parser')
            if soup.find_all(text=value):
                self.RequestRandomString(method, _input, key, space)
            else:
                pass
                # self.RequestRandomString(method, _input, key, space)

    def RequestRandomString(self, method, _input, key, space):

        randstr = RandomString(5)
        _input[key] = randstr

        if space == 'params':
            r = self.sess.request(method, self.urinfo._replace(query=urlencode(_input, doseq=True)).geturl(), **self.info)
        else:
            r = self.sess.request(method, self.current_url, **{space:_input}, **self.info)

        if randstr in r.text:

            soup = BeautifulSoup(r.text, 'html.parser')
            if soup.find_all(text=randstr):

                self.payloads_check(method,space, key,_input)

    def payloads_check(self, method, space, key, _input = {''}):
        element_xss, attribute_xss, script_xss = fuzzer_payloads.xss()
        for element in element_xss:
            r = self.sess.request(method, self.current_url)
        for attr in attribute_xss:
            pass
        for script in script_xss:
            pass
        # print("\033[90m","="*50,"\033[0m")
        # print(f'\033[31m[{urlparse(self.current_url).path}] : {space} attack vector discover\033[0m')
        # print(f'\033[32m{_input}\033[0m')


        # vector : query string, cookies, headers
        # print("\033[90m","="*50,"\033[0m")
        # print(f'\033[31m[{urlparse(self.current_url).path}] : {vector} attack vector discover\033[0m')
        # print(f'\033[32m{_input}\033[0m')

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