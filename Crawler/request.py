from selenium.webdriver import Chrome, ChromeOptions
import requests

NT_PATH = './webdriver/wevdriver.exe'
POSIX_PATH = './webdriver/wevdriver'

class request():
    def __init__(self, url, conf, **args) -> None:

        self.sess = requests.sessions()
        self.url = url

        if conf:
            self.CONFIG = ['headless', 'window-size=1920x1080', 'disable-gpu', 'no-sandbox', 'disable-dev-shm-usage']
        else:
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
        
        self.options = ChromeOptions()
        for _ in self.options:
            self.options.add_argument(_)

        self.drive = Chrome(executable_path=)

        self.drive.implicitly_wait(3)
        self.drive.set_page_load_timeout(3)

        self.drive.get(self.url)

        return self.drive.page_source