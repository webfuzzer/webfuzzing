from urllib.parse import parse_qs, urlparse, urljoin
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
    pass

class ReflectedXSS:
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