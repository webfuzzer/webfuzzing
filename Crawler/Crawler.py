from sys import float_repr_style
from urllib.parse import parse_qs, unquote, urlparse, urljoin, urlencode
from requests.exceptions import InvalidSchema
from Crawler.sessions import sessions
from Utils.utils import RandomString
from base64 import b64encode
from Storage.DB import Engine
from bs4 import BeautifulSoup
import tldextract
import pickle

URL_CHECK_REGEX = r'^(https|http|\/|^[\w,\s-]+\.[A-Za-z]{3}$).*$'

class URL:
    def __init__(self, URL, Site = False, subdomain = False,**info) -> None:
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
        self.subdomain_check = subdomain
        self.subdomain = tldextract.extract(URL).domain
        self.sess = sessions()(
            URL,
            Site
        )
        self.init_engine()
        self.engine.init_table(self.subdomain)
        self.URLJOIN = (lambda TMPURL: urljoin(self.CurrentURL, TMPURL))
        self.rs = RandomString(15)

    def Crawler(self) -> bool:
        self.GETLinks(self.URL)
        return True

    def GETLinks(self, URL, method = 'GET', data={}):
        URINFO = urlparse(URL)
        URJOIN = self.URLJOIN(URL)

        try:
            if self.DataURLCheck(URL, method, str(data)):
                try:
                    if data:
                        if method == 'POST':
                            Response = self.sess.request(method, URJOIN, data=data, **self.info)
                        else:
                            Response = self.sess.request(method, URJOIN, params=data, **self.info)
                    else:
                        Response = self.sess.request(method, URJOIN, **self.info)
                except InvalidSchema:
                    return

                self.CurrentURLCheck.add((URJOIN, method, str(data),))
                # if self.DataURLCheck(Response.url, method, str(data)):
                #         return
                html = Response.content.decode("utf-8", "replace")
                print(URJOIN)
                self.engine.add(
                    first_url = self.URL,
                    current_url = URJOIN,
                    method = method,
                    response_url = Response.url,
                    response_cookies = Response.cookies.get_dict(),
                    response_headers = dict(Response.headers),
                    response_status = Response.status_code,
                    request_cookies = Response.request._cookies.get_dict(),
                    request_headers = dict(Response.request.headers),
                    data = data,
                    body = b64encode(html.encode()).decode(),
                )

                if Response.history and (Response.url != URJOIN):
                    self.GETLinks(Response.url, method, data)

                URLParseCurrentURL = urlparse(self.CurrentURL)
                if URINFO.path != URLParseCurrentURL.path:
                    self.CurrentURL = URLParseCurrentURL._replace(path=URINFO.path).geturl()

                htmlparser = BeautifulSoup(html, 'html.parser')
                form = htmlparser.find("form")

                if form:
                    form_action = form.get('action')
                    form_method = form.get('method')
                    form_method = (form_method if form_method in ['GET','PUT','POST','HEAD'] else 'GET')
                    action_url = urljoin(Response.url,form_action)
                    form_in_elements_data = {}
                    form_submit_elements = form.find_all(name=['button', 'input', 'select', 'textarea'])

                    for SubmitElement in form_submit_elements:
                        value = SubmitElement.attrs.get('value')
                        form_in_elements_data.setdefault(SubmitElement.attrs.get('name'), (value if value else self.rs))

                    if form_method != 'POST':
                        action_url = urljoin(action_url, "?" + urlencode(form_in_elements_data, doseq=True))

                    if self.DataURLCheck(action_url, (form_method), str(form_in_elements_data)):
                        self.GETLinks(URL = action_url, method = form_method, data = form_in_elements_data)


                for attribute, tag in self.tags.items():
                    for element in htmlparser.find_all(tag):
                        if attribute in element.attrs:
                            attr_in_link = urljoin(Response.url, element.get(attribute))

                            if self.DataURLCheck(attr_in_link, method, str(data)):
                                self.GETLinks(URL = attr_in_link, method = method)

        except BaseException as e:
            return

    def DataURLCheck(self, url, method, data):
        if not (urlparse(url).netloc == self.FirstURLParse.netloc):
            return False
        if self.subdomain_check:
            if (tldextract.extract(url).subdomain == self.subdomain_check) and (url, method, str(data)) not in self.CurrentURLCheck:
                return True
        else:
            if (url, method, str(data)) not in self.CurrentURLCheck:
                return True
        return False

    def init_engine(self) -> None:
        self.engine = Engine()

    def closed(self) -> None:
        self.engine._sess.close_all()