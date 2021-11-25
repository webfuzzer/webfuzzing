from urllib.parse import parse_qs, unquote, urlparse, urljoin, urlencode
from requests.exceptions import InvalidSchema
from Crawler.sessions import sessions
from Utils.utils import RandomString
from base64 import b64encode
from Storage.DB import Engine
from bs4 import BeautifulSoup
import tldextract
import pickle

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
            URL,
            Site
        )
        self.init_engine()
        self.engine.init_table(tldextract.extract(URL).domain)
        self.URLJOIN = (lambda TMPURL: urljoin(self.CurrentURL, TMPURL))
        self.rs = RandomString(15)

    def Crawler(self) -> bool:
        self.GETLinks(self.URL)
        return True

    def GETLinks(self, URL, method = 'GET', data={}):
        """GETLinks 함수를 이용하여 최상위 경로부터 다양한 모든 URL을 파싱할 수 있습니다.
        해당 함수의 경우 다양한 필터링을 거쳐 self.tags에 있는 attrs들을 가지고 파싱하며 파싱한 URL, method, history length 등 다양한 정보를 Storage.DB.Engine를 통하여 /db/url.db에 정보를 저장 합니다.
        """
        URINFO = urlparse(URL)
        URJOIN = self.URLJOIN(URL)
        try:
            if ((URL,method, str(data)) not in self.CurrentURLCheck) and urlparse(URJOIN).netloc == self.FirstURLParse.netloc:
                print(URL)
                """
                해당 URL이 Crawling 대상 URL이 맞는지 urlparse를 이용하여 domain 부분 체크
                urlparse("https://www.google.com/path/example/?test=test").netloc -> www.google.com
                """
                try:
                    # self.sess.request => requests.Session().request
                    # 해당 URL에 요청
                    if data:
                        if method == 'POST':
                            Response = self.sess.request(method, URJOIN, data=data, **self.info)
                        else:
                            Response = self.sess.request(method, URJOIN, params=data, **self.info)
                    else:
                        Response = self.sess.request(method, URJOIN, **self.info)
                except InvalidSchema:
                    # 만약 mail:me2nuk.com 같이 잘못된 schema으로 요청 할 경우 try except 으로 예외 처리하여 return None
                    return
                # URJOIN = Response.url if urlparse(URJOIN).netloc == urlparse(Response.url).netloc else URJOIN
                # 중복 체크를 위해 쿼리가 존재할 경우 값만 제거되는 URL 저장
                if (urlparse(Response.url).netloc == self.FirstURLParse.netloc) and len(Response.history) and ((Response.url,method, str(data)) not in self.CurrentURLCheck):
                    print("Crawling Redirection Check")
                    self.GETLinks(URL = Response.url, method = method)
                self.CurrentURLCheck.add((URJOIN, method, str(data),))
                html = Response.content.decode("utf-8", "replace")
                # print(self.CurrentURLCheck)
                # Storage.DB.Engine을 이용하여 sqlite db에 url 정보 저장
                self.engine.add(
                    first_url = self.URL,
                    current_url = self.URLJOIN(URJOIN),
                    method = method,
                    history = b64encode(pickle.dumps(Response.history)).decode(),
                    history_len = len(Response.history),
                    response_url = Response.url,
                    response_cookies = Response.cookies.get_dict(),
                    response_headers = dict(Response.headers),
                    response_status = Response.status_code,
                    request_cookies = Response.request._cookies.get_dict(),
                    request_headers = dict(Response.request.headers),
                    data = data,
                    body = b64encode(html.encode()).decode(),
                )
                """
                URL join을 위해 경로 체크
                urlparse("https://www.google.com/path/example/").path -> /path/example/
                """
                URLParseCurrentURL = urlparse(self.CurrentURL)
                if URINFO.path != URLParseCurrentURL.path:
                    self.CurrentURL = URLParseCurrentURL._replace(path=URINFO.path).geturl()
                htmlparser = BeautifulSoup(html, 'html.parser')
                form = htmlparser.find("form")
                if form:
                    form_action = form.get('action')
                    form_method = form.get('method')
                    form_method = (form_method if form_method in ['GET','PUT','POST','HEAD'] else 'GET')
                    action_url = self.URLJOIN(form_action)
                    form_in_elements_data = {}
                    form_submit_elements = form.find_all(name=['button', 'input', 'select', 'textarea'])
                    for SubmitElement in form_submit_elements:
                        value = SubmitElement.attrs.get('value')
                        form_in_elements_data.setdefault(SubmitElement.attrs.get('name'), (value if value else self.rs))
                    if form_method != 'POST':
                        action_url = urljoin(action_url, "?" + urlencode(form_in_elements_data, doseq=True))
                    if ((action_url,form_method, str(data)) not in self.CurrentURLCheck) and urlparse(action_url).netloc == self.FirstURLParse.netloc:
                        self.GETLinks(
                            URL = action_url,
                            method = (form_method),
                            data = form_in_elements_data,
                        )
                for attribute, tag in self.tags.items():
                    for element in htmlparser.find_all(tag):
                        if attribute in element.attrs:
                            attr_in_link = self.URLJOIN(element.get(attribute))
                            if ((attr_in_link,method, str(data)) not in self.CurrentURLCheck) and urlparse(attr_in_link).netloc == self.FirstURLParse.netloc:
                                self.GETLinks(URL = attr_in_link, method = method)
        except BaseException as e:
            print(e)
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, exc_tb.tb_lineno, e)

    def init_engine(self) -> None:
        # sqlite에 데이터 저장을 위해 Engine Class 생성
        self.engine = Engine()

    def closed(self) -> None:
        self.engine._sess.close_all()