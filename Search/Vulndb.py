"""
기본적인 공격 벡터 : header, cookie, post data, get data
"""
from urllib.parse import parse_qs, urlencode, urlparse, urljoin
from Search.payloads import fuzzer_payloads
from bs4 import BeautifulSoup, Comment
from Utils.utils import RandomString
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
        self.element_xss, self.attribute_xss, self.script_xss = fuzzer_payloads.xss()
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
            # print(self.current_url)
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
            if type(value) == list:
                value = value[0]
            if soup.find_all(text=value) or (True in [value in j for i in soup.find_all() for j in i.attrs.values()]) or (soup.text.find(value) != -1):
                # print(key, value, id(_input))
                self.RequestRandomString(method, _input, key, space)
                # self.RequestRandomString(method, _input, key, space)

    def RequestRandomString(self, method, _input, key, space):

        randstr = RandomString(5)
        temp = _input
        temp[key] = randstr
        # print(temp)
        if space == 'params':
            r = self.sess.request(method, self.urinfo._replace(query=urlencode(temp, doseq=True)).geturl(), **self.info)
            # print(r.url)
        else:
            r = self.sess.request(method, self.current_url, **{space:temp}, **self.info)
        if randstr in r.text:
            soup = BeautifulSoup(r.text, 'html.parser')
            # print(True in [randstr in j for i in soup.find_all() for j in i.attrs.values()], self.current_url)
            if soup.find_all(text=randstr) or(True in [randstr in j for i in soup.find_all() for j in i.attrs.values()]) or (soup.text.find(randstr) != -1):

                self.payloads_check(method,space, key,temp)

    def payloads_check(self, method, space, key, _input = {''}):
        for element in self.element_xss:
            temp = _input
            attrs_key_rand = RandomString(5)
            attrs_value_rand = RandomString(5)
            inner_text_rand = RandomString(5)
            temp[key] = element.format(f" {attrs_key_rand}={attrs_value_rand}", inner_text_rand)
            if space == 'params':
                r = self.sess.request(method, self.urinfo._replace(query=urlencode(temp, doseq=True)).geturl(), **self.info)
            else:
                r = self.sess.request(method, self.current_url, **{space:temp}, **self.info)
            soup = BeautifulSoup(r.text, 'html.parser')
            if soup.find(attrs={attrs_key_rand.lower():attrs_value_rand}, text=inner_text_rand) or (soup.find(attrs={attrs_key_rand.lower():attrs_value_rand}) and soup.string.find(inner_text_rand) if soup.string else False):
                print("\033[90m","="*50,"\033[0m")
                print(self.urinfo._replace(query=urlencode(temp, doseq=True)).geturl())
                print(f'\033[31m[{urlparse(self.current_url).path}] : {space} attack vector discover\033[0m')
                print(f'\033[32m{_input}\033[0m')
                break
        for attr in self.attribute_xss:
            pass
        for script in self.script_xss:
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
