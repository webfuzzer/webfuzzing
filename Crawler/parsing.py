from urllib.parse import urlparse, parse_qs, urlencode
from bs4 import BeautifulSoup
from api import *
import json

class parse:
    def __init__(self, url, **args) -> None:
        self.url = url
        self.args = args.setdefault('timeout',2)
    def request(self) -> str:
        print(self.args)
        return get_req(self.url, self.args)

class ResponseParameter:
    def __init__(self) -> None:
        self.loads = json.loads
        self.dumps = json.dumps

    def JsonFileWrite(self, Filename, data) -> bool:
        return True

print(parse('https://www.google.com').request())