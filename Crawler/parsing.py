from urllib.parse import urlparse, parse_qs, urlencode
from bs4 import BeautifulSoup
from api import *
import json

class parse:
    def __init__(self, url, **args) -> None:
        self.url = url
        args.setdefault('timeout',2)
        self.args = args
        self.Response = get_req(self.url, **self.args)
        self.parameter = ResponseParameter(Response)
    
        self.status = self.Response.status_code

    @property
    def tag(self) -> dict:

        self.parameter

        return {
            'response': self.Response.text, # Response text
        }


class ResponseParameter:
    def __init__(self, text) -> None:

        self.text = text
        self.load = json.load
        self.dump = json.dump
        self.mode = 'None'

    def GetTagLink(self) -> dict:
          
        parser = BeautifulSoup(self.text, 'html.parser')
        tags = ['a', 'form', '']
        for elements in parser.find_all('a')

    def JsonFileRead(self, Filename) -> (bool, str):    

        self.mode = 'r'

        try:
            with open(file=filename, mode=self.mode, encoding='UTF-8') as f:
                return (True, self.load(f))
        except:
            return (False, '')

    def JsonFileWrite(self, Filename, data) -> (bool, str):

        self.mode = 'w+'
        self.data = data
        self.Filename

        try:
            with open(file=filename, mode=self.mode, encoding='UTF-8') as f:
                self.dump(data, f)
        except:
            return (False, '')        

r = parse('https://www.google.com')
print(r.tag)