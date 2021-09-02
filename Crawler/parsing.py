from urllib.parse import urlencode, parse_qs, quote, unquote, urlparse
from selenium import Chrome, ChromeOptions
import requests

NT_PATH = './webdriver/wevdriver.exe'
POSIX_PATH = './webdriver/wevdriver'

class request():
    def __init__(self, url, **args) -> None:
        self.sess = requests.sessions()
        self.url = url
        args.setdefault('timeout', 3)
        self.args = args

    def get(self) -> dict:

        res = self.sess.get(self.url, *self.args)

        return {
            'status': res.status_code,
            'history':res.history,
            'body':res.text,
            'url':res.url,
            'conn':res.ok,
        }

    def post(self) -> dict:

        res = self.sess.post(self.url, *self.args)

        return {
            'status': res.status_code,
            'history':res.history,
            'body':res.text,
            'url':res.url,
            'conn':res.ok,
        }

    def webdriver(self) -> str:
        # selenium
        pass