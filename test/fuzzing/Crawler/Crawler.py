from urllib.parse import parse_qs, unquote, urlparse, urljoin, urlencode
from requests.exceptions import InvalidSchema
from Crawler.sessions import sessions
from base64 import b64encode
from Storage.DB import Engine
from bs4 import BeautifulSoup
import tldextract

class URL:
    def __init__(self, URL, Site = False, **info) -> None:
        self.tags = {
            'href':[
                    'a',
                    'link',
                    'area',
                    'base',
                ],
            'src':[
                    'img',
                    'script',
                    'iframe',
                    'embed',
                    'audio',
                    'input',
                    'script',
                    'source',
                    'track',
                    'video',
                ],
            'action':[
                    'form',
                ],
            'data':[
                    'object',
                ],
        }
        info.setdefault('timeout', 5)
        info.setdefault('headers', {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'})
        self.info = info
        self.CurrentURL = self.URL = URL
        self.FirstURLParse = urlparse(self.URL)
        self.CurrentURLCheck = set()
        self.sess = sessions()(
            urljoin(URL, '/') if Site else URL,
            Site
        )
        self.init_engine()
        self.engine.init_table(tldextract.extract(URL).domain)
        self.URLJOIN = (lambda TMPURL: urljoin(self.CurrentURL, TMPURL))

    def Crawler(self) -> bool:
        print(urljoin(self.URL, '/'))
        self.GETLinks(urljoin(self.URL, '/'))
        return True

    def GETLinks(self, URL, method = 'GET'):
        # https://www.google.com
        # URL이 fuzzing URL인지 체크
        # URL = self.empty_url(URL)
        # URL이 존재하는지 체크
        if URL:
            if urlparse(URL).netloc == self.FirstURLParse.netloc:
            # 해당 URL에 요청
                try:
                    Response = self.sess.request(method, URL, **self.info)
                except InvalidSchema:
                    return
                # 올바른 URL 형식으로 만들기 위해 현재 URL과 첫번째 URL 체크
                if urlparse(URL).path != self.FirstURLParse.path:
                    self.CurrentURL = Response.url

                htmlparser = BeautifulSoup(Response.text, 'html.parser')
                form= htmlparser.find("form")
                if form:
                    form_method = form.get('method')
                    form_action = form.get('action')
                    self.GETLinks(
                        URL = urljoin(self.CurrentURL,form_action),
                        method = (form_method if form_method in ['GET','PUT','POST','HEAD'] else 'GET'),
                    )
                for attribute, tag in self.tags.items():
                    for element in htmlparser.find_all(tag):
                        if attribute in element.attrs:
                            attr_in_link = element.get(attribute)
                            if self.qs_value_empty(attr_in_link) not in self.CurrentURLCheck and urlparse(self.URLJOIN(attr_in_link)).netloc == self.FirstURLParse.netloc:
                                self.CurrentURLCheck.add(self.qs_value_empty(attr_in_link)) # 파라미터가 비어 있는 URL을 넣어야 됨
                                self.engine.add(
                                    first_url = self.URL, # 퍼징 대상 URL 넣어야 됨
                                    current_url = self.URLJOIN(attr_in_link), # 현재 URL 넣어야 됨
                                    method = method, # 현재 method 넣어야 됨
                                    history_len = len(Response.history),
                                    body = b64encode(Response.text.encode()).decode(), # response body base64 encoding 해서 넣어야 됨
                                )
                                self.GETLinks(URL = attr_in_link, method = method)

    def qs_value_empty(self, URL) -> str:
        URL = self.URLJOIN(URL)
        urinfo = urlparse(URL)
        if urinfo.query:
            return urljoin(self.URL, unquote(urlencode(dict.fromkeys(sorted(parse_qs(urinfo.query)), ''), doseq=True)))
        return URL

    def empty_url(self, URL):
        if URL and self.FirstURLParse.netloc == urlparse(URL).netloc:
            return self.qs_value_empty(URL)
        return

    def init_engine(self) -> None:
        self.engine = Engine()