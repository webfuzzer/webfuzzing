from urllib.parse import urljoin
from selenium.webdriver import Chrome, ChromeOptions
import requests
import os

NT_PATH = r'C:\Users\MinUk\Documents\GitHub\Crawler\Crawler\webdriver\chromedriver.exe'
POSIX_PATH = 'webdriver/chromedriver'

class request:
    def __init__(self, url, conf = False, **args) -> None:

        self.sess = requests.Session()
        self.url = url
        self.driver = False
        ##############
        self.path = POSIX_PATH
        # 셀레니움 chromedriver path
        if os.name == "nt":
            # windows일 경우
            self.path = NT_PATH
        ##############
        if conf:
            self.CONFIG = ['window-size=1920x1080', 'disable-gpu', 'no-sandbox', 'disable-dev-shm-usage', '--log-level=3']
        else:
            self.args = args
            # cookies, headers 등 다양한 요청 관련 정보
    def __getattr__(self, name: str) -> dict:
        return getattr(self,name)

    def set(self, url, **args) -> dict:
        self.url = url
        self.args = args

        return self.get()

    def get(self) -> dict:

        res = self.sess.get(self.url, **self.args)

        res.close()
        # GET 메서드 요청
        return {
            'status': res.status_code,
            'history':res.history,
            'headers':res.headers,
            'cookies':res.cookies,
            'body':res.content.decode("utf-8", "replace"),
            'url':res.url,
            'conn':res.ok,
            'request':res.request
        }


    def post(self) -> dict:

        res = self.sess.post(self.url, **self.args)

        return {
            'status': res.status_code,
            'history':res.history,
            'headers':res.headers,
            'cookies':res.cookies,
            'body':res.content.decode("utf-8", "replace"),
            'url':res.url,
            'conn':res.ok,
            'request':res.request
        }

    def driver_set(self, url, conf = False) -> str:
        self.url = url
        self.conf = conf
        return self.driver_get()

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
            {
                'status': 200,
                'url':self.drive.current_url,
                'body':'',
            }

    def drive_quit(self) -> bool:
        try:
            self.drive.quit()
            return True
        except:
            return False

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

#r = request('https://www.google.com', cookies = {'a':'a'})
#print(r.get()['body'])
#print(r.get()['cookies'])
#print(r.get()['body'])

# r = request('https://www.google.com', conf=True)
# print(r.webdriver())
