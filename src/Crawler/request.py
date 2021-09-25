from selenium.webdriver import Chrome, ChromeOptions
from __globals__ import *
from db import DATABASE
import requests
import os

SELENIUM_CONFIG =['window-size=1920x1080', 'disable-gpu', 'no-sandbox', 'disable-dev-shm-usage', '--log-level=3', 'headless']

class sessions:
    def __init__(self, url, **args) -> None:
        self.url = url
        self.arguments = args
        self.sess_check = False
        self.CONFIG = SELENIUM_CONFIG
        self.path = NT_PATH if os.name == "nt" else POSIX_PATH

        self.sess = requests.Session()
        
    def __call__(self, url, **args : dict) -> dict:
        self.url = url
        self.arguments = args

    def driver_set(self, url) -> str:
        self.url = url

        return self.driver_get()

    def sess_rtn(self, response) -> dict:
        return {
            'status': response.status_code,
            'history':response.history,
            'headers':response.headers,
            'cookies':response.cookies,
            'body':response.content.decode("utf-8", "replace"),
            'url':response.url,
            'conn':response.ok,
            'request':response.request
        }

    def sess_get(self) -> dict:

        res = self.sess.get(self.url, **self.arguments)

        return self.returns(res)


    def sess_post(self) -> dict:

        res = self.sess.post(self.url, **self.arguments)

        return self.returns(res)

    def driver_get(self) -> str:
        try:

            if self.driver:
                self.drive.get(self.url)

                return {
                    'status': 200,
                    'url':self.drive.current_url,
                    'body':self.drive.page_source,
                }

            else:
                return self.webdriver()

        except:

            return {
                'status': 200,
                'url':self.drive.current_url,
                'body':'',
            }

    def webdriver(self) -> str:
        self.options = ChromeOptions()

        for _ in self.CONFIG:
            self.options.add_argument(_)

        self.drive = Chrome(self.path, options=self.options)
        self.drive.implicitly_wait(5)
        self.drive.set_page_load_timeout(5)
        self.drive.get(self.url)
        self.driver = True
        
        return {
            'status': 200,
            'url':self.drive.current_url,
            'body':self.drive.page_source,
        }

    def __del__(self) -> None:
        self.sess.close()
        self.drive.quit()