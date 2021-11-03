"""
기본적인 공격 벡터 : header, cookie, post data, get data
"""
from random import Random
from urllib.parse import parse_qs, quote_from_bytes, urlencode, urlparse, urljoin
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

def init_session():
    return sessions()(Site=False)

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

class ReflectedXSS:
    def __init__(self, datatable):
        """
        self.datatable:database content
        self.vuln_level:vulnerability level
        """
        self.element_eq_pay, self.element_empty_value, self.attribute_pay, self.script_pay = fuzzer_payloads.xss()
        self.datatable = datatable
        self.sess = sessions.init_sess()
        self.vuln_level = 0
        self.paths = set()

    def exploit(self):
        """
        """
        for content in self.datatable:
            self.body = b64decode(content[attr['body']]).decode()
            self.current_url = content[attr['current_url']]
            self.urinfo = urlparse(self.current_url)
            self.method = content[attr['method']]
            
            self.search_text(
                headers = content[attr['headers']],
                cookies = content[attr['cookies']],
            )

    def search_text(self, headers, cookies):
        """
        """

        rs = RandomString(5)

        if self.urinfo.query:
            qs = parse_qs(self.urinfo.query)
            for key, value in qs:
                if value in self.body and (rs in self.string_search_text(rs, 'qs', key = key, input = qs[:])):
                    pass

        if self.urinfo.fragment and self.urinfo.fragment in self.body and (rs in self.string_search_text(rs, 'fragment')):
            pass

        if cookies:
            for key, value in cookies:
                if value in self.body and (rs in self.string_search_text(rs, 'cookies', key = key, input = cookies[:])):
                    pass

        if headers:
            for key, value in headers:
                if value in self.body and (rs in self.string_search_text(rs, 'headers', key = key, input = headers[:])):
                    pass

    def string_search_text(self, rs, vector, key = '', input = {}):
        """
        search for a random string in response body
        """
        rs = rs

        if vector == 'fragment':
            r = self.sess.request(self.method, self.urinfo._replace(**{vector:rs}))
        elif vector == 'qs':
            input[key] = rs
            r = self.sess.request(self.method, self.urinfo._replace({vector:urlencode(input, doseq=True)}))
        else:
            input[key] = rs
            r = self.sess.request(self.method, **{vector:input})

        return r.text
    
    def html_injection_test(self):
        for element in self.element_eq_pay:
            attribute_key_rs = RandomString(5)
            attribute_value_rs = RandomString(5)
            inner_text_rs = RandomString(5)
            soup = BeautifulSoup(self.string_search_text(element.format(attribute_key_rs,attribute_value_rs, inner_text_rs)), 'html.parser')
            if soup.find(attrs={attribute_key_rs.lower():attribute_value_rs}, text=inner_text_rs):
                pass
            elif soup.find(attrs={attribute_value_rs.lower():attribute_value_rs}):
                pass
            elif soup.find(text=inner_text_rs):
                pass


        for element in self.element_empty_value:
            attribute_key_rs = RandomString(5)
            inner_text_rs = RandomString(5)
            self.string_search_text(element.format(attribute_key_rs, inner_text_rs))
            if soup.find(attrs={attribute_key_rs.lower():attribute_value_rs}, text=inner_text_rs):
                pass
            elif soup.find(attrs={attribute_value_rs.lower():attribute_value_rs}):
                pass
            elif soup.find(text=inner_text_rs):
                pass

    def cross_site_scripting_test(self):
        """
        """
        pass

class OpenRedirect:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL

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
