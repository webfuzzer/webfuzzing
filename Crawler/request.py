from selenium.webdriver import Chrome, ChromeOptions
import requests
import os

NT_PATH = './webdriver/chromedriver.exe'
POSIX_PATH = './webdriver/chromedriver'

class request:
    def __init__(self, url, conf = False, **args) -> None:

        self.sess = requests.Session()
        self.url = url
        ##############
        self.path = POSIX_PATH
        # 셀레니움 chromedriver path
        if os.name == "nt":
            # windows일 경우
            self.path = NT_PATH
        ##############
        if conf:
            self.CONFIG = ['window-size=1920x1080', 'disable-gpu', 'no-sandbox', 'disable-dev-shm-usage', 'headless']
        else:
            self.args = args
            # cookies, headers 등 다양한 요청 관련 정보

    def __getattr__(self, name: str) -> dict:
        return getattr(self,name)

    def get(self) -> dict:

        res = self.sess.get(self.url, **self.args)
        # GET 메서드 요청
        return {
            'status': res.status_code,
            'history':res.history,
            'headers':res.headers,
            'cookies':res.cookies,
            'body':res.text,
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
            'body':res.text,
            'url':res.url,
            'conn':res.ok,
            'request':res.request
        }

    def webdriver(self) -> str:
        try:
            self.options = ChromeOptions()
            for _ in self.CONFIG:
                self.options.add_argument(_)

            self.drive = Chrome(executable_path=self.path, options=self.options)

            self.drive.implicitly_wait(3)
            self.drive.set_page_load_timeout(3)

            self.drive.get(self.url)

            self.drive.quit()

            return {
                'status': 200,
                '':self.drive.page_source,
            }
        except Exception as e:
            return {
                'status': 500,
                'msg':e,
            }

#r = request('https://www.google.com', cookies = {'a':'a'})
#print(r.get()['body'])
#print(r.get()['cookies'])
#print(r.get()['body'])

# r = request('https://www.google.com', conf=True)
# print(r.webdriver())
