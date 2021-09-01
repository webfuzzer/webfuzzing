from urllib.parse import urlparse, parse_qs, urlencode
#from urllib import robotparser
from bs4 import BeautifulSoup
from api import *
import json

taglist = ['a','form','area']

class parse:
    def __init__(self, url, **args) -> None:
        self.url = url
        args.setdefault('timeout',2)
        self.args = args
        self.Response = get_req(self.url, **self.args)

        self.text = self.Response.text
        self.status = self.Response.status_code

        self.parameter = ResponseParameter(self.text)
    
        self.status = self.Response.status_code

    @property
    def tag(self) -> dict:

        return {
            'response':self.text,
            'status':self.status,
            'tag':self.parameter.GetTagLink()
        }


class ResponseParameter:
    def __init__(self, text) -> None:

        self.text = text

    def GetTagLink(self) -> list:
        global taglist

        self.tags = {}

        parser = BeautifulSoup(self.text, 'html.parser')

        for tagname in taglist:
            self.tags[tagname] = [i.get('href') for i in parser.find_all(tagname)]

        return self.tags

class JsonFile:
    def __init__(self, mode, **args) -> None:

        self.err = ''
        self.mode = 'None'
        self.load = json.load
        self.dump = json.dump
        self.encoding = 'UTF-8'

        if mode == 'r':
            try:
                self.JsonFileRead(**args)
            except BaseException as e:
                self.err = e
        elif mode == 'w':
            try:
                self.JsonFileWrite(**args)
            except BaseException as e:
                self.err = e
        else:
            self.err = '잘못된 mode'

    def __str__(self) -> str:
        if self.err:
            return '<JsonFile [ERR:(%s)]>'% (self.err)
        else:
            return '<JsonFile %s:[%s]>'% (self.mode, self.filename)


    def JsonFileRead(self, filename) -> (bool, str):    

        self.mode = 'r'

        try:
            with open(file=filename, mode=self.mode, encoding=self.encoding) as f:
                return (True, self.load(f))
        except:
            return (False, '')

    def JsonFileWrite(self, filename, data) -> (bool, str):

        self.mode = 'w+'
        self.data = data
        self.filename = filename

        try:
            with open(file=filename, mode=self.mode, encoding=self.encoding) as f:
                self.dump(data, f)
        except:
            return (False, '')

r = parse('https://www.google.com')

print(r.tag)