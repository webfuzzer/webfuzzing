from urllib.parse import urlencode, parse_qs, quote, unquote, urlparse
from bs4 import BeautifulSoup
from request import *

class Crawler:
    def __init__(self) -> None:
        self.tags = {
            'href':['a', 'link', 'area'],
            'src':['img', 'script', 'iframe'],
            'action':['form']
        }
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        }

    def tag(self) -> None:
        r = request('http://me2nuk.com', headers=self.headers)
        body = r.get()['body']
        soup = BeautifulSoup(body, 'html.parser')
        url = []

        for attribute, tagname in self.tags.items():
            for element in soup.find_all(tagname):
                print(element.get(attribute))

    def parsing(self) -> None:
        pass

C = Crawler()
C.ParsingTag()