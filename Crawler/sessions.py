from selenium.webdriver import Chrome, ChromeOptions
from requests import Session
import os

class sessions:
    def __init__(self) -> None:
        pass

    def __call__(self, TOPURL = None, Site = False) -> None:
        if Site:
            return self.init_drive(TOPURL)
        else:
            return self.init_sess()

    def init_sess(self):
        self.sess = Session()
        self.sess.max_redirects = 10
        return self.sess

    def init_drive(self, url):

        self.CHROMEOPTION = ['window-size=1920x1080', 'disable-gpu', 'no-sandbox', 'disable-dev-shm-usage', '--log-level=3']
        self.PATH = {
            'nt':'\\src\\Crawler\\webdriver\\chromedriver.exe',
            'posix':'/src/Crawler/webdriver/chromedriver',
        }

        self.options = ChromeOptions()
        for _ in self.CHROMEOPTION:
            self.options.add_argument(_)

        self.driver = Chrome(
                os.getcwd() + (self.PATH['nt'] if os.name == "nt" else self.PATH['posix']),
                options=self.options
        )
        self.driver.implicitly_wait(5)
        self.driver.set_page_load_timeout(5)
        self.driver.get(url)

        return self.driver