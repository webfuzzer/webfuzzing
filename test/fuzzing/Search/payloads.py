"""
기본적인 공격 벡터 : header, cookie, post data, get data, s
"""
from urllib.parse import parse_qs, urlparse, urljoin
from string import ascii_letters, digits
from bs4 import BeautifulSoup
from Crawler import sessions
from Storage import Engine
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

def init_session():
    return sessions()(Site=False)

def init_engine():
    return Engine()

def RandomString(strlen, digit=True):
    return ''.join([choice(ascii_letters + (digits if digit else '')) for _ in range(0,strlen)])

class OpenRedirect:
    def __init__(self, URL, **info) -> None:
        pass

    def request_history_check(self) -> None:
        pass

class ReflectedXSS:
    def __init__(self, URL, **info) -> None:
        self.URL = URL
        self.info = info
        self.sess = init_session()
        self.engine = init_engine()

    def try_html_element_events_check(self) -> None:
        pass

    def search_html_element(self) -> None:
        pass

    def input_value_check(self) -> None:
        pass

class SQLInjection:
    pass

class CrossSiteRequestForgery:
    pass

class NOSQLInjection:
    pass

class OSCommandInjection:
    pass

class ServerSideTemplateInjection:
    pass

class LocalFileInclusion:
    pass

class RemoteFileInclusion:
    pass