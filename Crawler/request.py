from selenium.webdriver import Chrome, ChromeOptions
from requests import get, post, head, put, sessions
import os

posix = './webdriver/chromedriver'
nt = './webdriver/chromedriver.exe'

class static:
    def __init__(self, url, **args) -> None:
        '''
        statis request
        module : requests 모듈 사용
        
        def get(self) -> dict: requests.get
        def put(self) -> dict: requests.put
        def post(self) -> dict: requests.post
        def head(self) -> dict: requests.head
        def sess(self) -> dict: requests.sessions
        '''

        self.url = url
        self._get = get
        self._put = put
        self._post = post
        self._head = head
        self._args = args
        self._sess = sessions

    def get(self) -> dict:

        r = self._get(self.url, **self._args)

        return {
            'text':r.text,
            'status':r.status_code,
            'history':r.history,
            'ok':r.ok,
        }

    def put(self) -> dict:

        r = self._put(self.url, **self._args)

        return {
            'text':r.text,
            'status':r.status_code,
            'history':r.history,
            'ok':r.ok,
        }

    def post(self) -> dict:

        r = self._post(self.url, **self._args)

        return {
            'text':r.text,
            'status':r.status_code,
            'history':r.history,
            'ok':r.ok,
        }

    def head(self) -> dict:

        r = self._head(self.url, **self._args)

        return {
            'text':r.text,
            'status':r.status_code,
            'history':r.history,
            'ok':r.ok,
        }

    def sess(self):
        return self._sess()

class dynamic:
    def __init__(self) -> None:
        '''
        dynamic request
        module : selenium 모듈 사용

        def WindowsNewTechnology(self) -> dict: Chrome() # windows
        def PortableOperationgSystemInterface(self) -> dict: Chrome() # linux
        '''
        
        pass

class request(static, dynamic):
    def __init__(self, url, **args) -> None:
        super().__init__(url, **args)

    def __str__(self) -> str:
        return '<[%s,%s]>'% (static.__name__, dynamic.__name__)

r = request('https://www.google.com')
print(r.get())