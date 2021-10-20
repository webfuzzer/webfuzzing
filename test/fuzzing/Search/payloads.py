"""
기본적인 공격 벡터 : header, cookie, post data, get data, s
"""
from urllib.parse import parse_qs, urlparse, urljoin
from bs4 import BeautifulSoup
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

    def try_html_element_events_check(self) -> None:
        pass

    def search_html_element(self) -> None:
        """
        - Header에 있는 값이 Response body에 출력 되는 경우
            - Cookie에 있는 값이 Response body에 출력 되는 경우
        - query에 있는 값이 Response body에 출력 되는 경우
        """

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