from urllib.parse import ParseResultBytes, non_hierarchical, parse_qs, urlparse, urljoin
from bs4 import BeautifulSoup
from Crawler import sessions

__all__ = [
    'OpenRedirect', 
    'ReflectedXSS', 
    'SQLInjection', 
    'CrossSiteRequestForgery', 
    'NOSQLInjection', 
    'OSCommandInjection', 
    'ServerSideTemplateInjection', 
    'LocalFileInclusion', 
    'RemoteFileInclusion'
]

class OpenRedirect:
    def __init__(self, URL, **info) -> None:
        pass

    def request_history_check(self) -> None:
        pass

class ReflectedXSS:
    def __init__(self, URL, **info) -> None:
        self.URL = URL
        self.info = info

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