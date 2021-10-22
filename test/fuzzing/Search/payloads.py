"""
기본적인 공격 벡터 : header, cookie, post data, get data
"""
from urllib.parse import parse_qs, urlparse, urljoin
from string import ascii_letters, digits
from bs4 import BeautifulSoup
from Storage.DB import Engine
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

class init:
    def __init__(self, crawling_contents, URL, **info):
        self.crawling_contents = crawling_contents
        self.info = info
        self.URL = URL

def init_session():
    return sessions()(Site=False)

def RandomString(strlen, digit=True):
    return ''.join([choice(ascii_letters + (digits if digit else '')) for _ in range(0,strlen)])

class OpenRedirect(init):
    pass

class ReflectedXSS(init):
    pass

class SQLInjection(init):
    pass

class CrossSiteRequestForgery(init):
    pass

class NOSQLInjection(init):
    pass

class OSCommandInjection(init):
    pass

class ServerSideTemplateInjection(init):
    pass

class LocalFileInclusion(init):
    pass

class RemoteFileInclusion(init):
    pass