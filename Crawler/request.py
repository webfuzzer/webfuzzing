from selenium.webdriver import Chrome, ChromeOptions
from requests import get, post, head, put, sessions
import os

posix = './webdriver/'
nt = './webdriver/'

class static:
    def __init__(self) -> None:
        '''
        statis request
        module : requests 모듈 사용
        
        def get(self) -> dict: requests.get
        def put(self) -> dict: requests.put
        def post(self) -> dict: requests.post
        def head(self) -> dict: requests.head
        def sess(self) -> dict: requests.sessions
        '''

        pass

class dynamic:
    def __init__(self) -> None:
        '''
        dynamic request
        module : selenium 모듈 사용

        def WindowsNewTechnology(self) -> dict: Chrome() # windows
        def PortableOperationgSystemInterface(self) -> dict: Chrome() # linux
        '''
        
        pass