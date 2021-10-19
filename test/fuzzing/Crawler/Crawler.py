from urllib.parse import parse_qs, unquote, urlparse, urljoin, urlencode
from requests.exceptions import InvalidSchema
from Crawler.sessions import sessions
from base64 import b64encode
from Storage.DB import Engine
from bs4 import BeautifulSoup
import tldextract

class URL:
    def __init__(self, URL, Site = False, **info) -> None:
        # self.tags -> 파싱할 태그, 속성 리스트
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
        # Crawling 최적화를 위해 서버에서 계속 반환을 해주지 않는 경우 연결 끊기 위해 최대 5초 대기
        info.setdefault('timeout', 5)
        # headers를 필터링 하는 경우를 대비하여 User-Agent에 Chrome/93.0.4577.63 버전으로 추가
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
        self.engine.init_table(tldextract.extract(URL).domain) # tldextract.extract(URL)을 이용하여 domian만 가져온 후 테이블 생성
        self.URLJOIN = (lambda TMPURL: urljoin(self.CurrentURL, TMPURL))

    def Crawler(self) -> bool:
        self.GETLinks(urljoin(self.URL, '/'))
        return True

    def GETLinks(self, URL, method = 'GET'):
        """GETLinks 함수를 이용하여 최상위 경로부터 다양한 모든 URL을 파싱할 수 있습니다.
        해당 함수의 경우 다양한 필터링을 거쳐 self.tags에 있는 attrs들을 가지고 파싱하며 파싱한 URL, method, history length 등 다양한 정보를 Storage.DB.Engine를 통하여 /db/url.db에 정보를 저장 합니다.
        """
        # URL이 존재하는 경우 (False, None)인 경우 pass
        URINFO = urlparse(URL)
        URJOIN = self.URLJOIN(URL)

        print(URJOIN)

        if URL:
            """
            해당 URL이 Crawling 대상 URL이 맞는지 urlparse를 이용하여 domain 부분 체크
            urlparse("https://www.google.com/path/example/?test=test").netloc -> www.google.com
            """
            if urlparse(URJOIN).netloc == self.FirstURLParse.netloc:
                try:
                    # self.sess.request => requests.Session().request
                    # 해당 URL에 요청
                    Response = self.sess.request(method, URJOIN, **self.info)
                except InvalidSchema:
                    # 만약 mail:me2nuk.com 같이 잘못된 schema으로 요청 할 경우 try except 으로 예외 처리하여 return None
                    return
                self.CurrentURLCheck.add(self.qs_value_empty(URJOIN))
                self.engine.add(
                    first_url = self.URL,
                    current_url = self.URLJOIN(URJOIN),
                    method = method,
                    history_len = len(Response.history),
                    body = b64encode(Response.content.decode("utf-8", "replace").encode()).decode(),
                )
                """"
                URL join을 위해 경로 체크
                urlparse("https://www.google.com/path/example/").path -> /path/example/
                """
                URLParseCurrentURL = urlparse(self.CurrentURL)
                if URINFO.path != URLParseCurrentURL.path:
                    self.CurrentURL = URLParseCurrentURL._replace(path=URINFO.path).geturl()

                # elemtns 파싱을 위해 bs4 모듈 사용
                htmlparser = BeautifulSoup(Response.content.decode("utf-8", "replace").encode(), 'html.parser')
                # form 태그 찾기
                form = htmlparser.find("form")
                # 만약 form 태그가 존재하는 경우 / htmlparser.find 의 경우 없는 태그를 가져올려 하는 경우 None 반환
                if form:
                    # form 태그의 method attr 가져오기
                    form_method = form.get('method')
                    # form 태그의 action attr 가져오기
                    form_action = form.get('action')
                    # URL을 조합 한 뒤 method도 맞춰서 재귀 함수 작동
                    self.GETLinks(
                        URL = urljoin(self.CurrentURL,form_action),
                        # 잘못된 method가 들어 있는 경우를 대비하여 ['GET','PUT','POST','HEAD'] 메서드만 허용 ( 만약 다른 메서드도 넣어야 될 경우 추가 예정 )
                        method = (form_method if form_method in ['GET','PUT','POST','HEAD'] else 'GET'),
                    )
                # self.tags => 파싱하기 위한 태그들과 속성 dict
                for attribute, tag in self.tags.items():
                    # 파싱 할 모든 tag를 가져오기
                    for element in htmlparser.find_all(tag):
                        # 만약 해당 태그에 파싱 할 속성이 있는 경우
                        if attribute in element.attrs:
                            # 해당 속성 안에 있는 URL 가져오기
                            attr_in_link = element.get(attribute)
                            # attr_in_link 변수에 있는 URL에 쿼리가 있는 경우 값만 제거
                            qs_value_empty_attr_in_link = self.qs_value_empty(attr_in_link)
                            # 가져온 URL을 이미 가져왔는지 and 해당 URL이 Crawling URL과 같은 domain인지 체크
                            if qs_value_empty_attr_in_link not in self.CurrentURLCheck and urlparse(self.URLJOIN(attr_in_link)).netloc == self.FirstURLParse.netloc:
                                # 중복 체크를 위해 쿼리가 존재할 경우 값만 제거되는 URL 저장
                                # Storage.DB.Engine을 이용하여 sqlite db에 url 정보 저장
                                # 하위 url 파싱을 위해 재귀 함수로 반복적인 호출
                                self.GETLinks(URL = attr_in_link, method = method)

    def qs_value_empty(self, URL) -> str:
        URL = self.URLJOIN(URL)
        urinfo = urlparse(URL)
        # url에 쿼리가 존재하는지 체크
        if urinfo.query:
            """
            URL에 있는 쿼리를 정렬 한 뒤 값만 제거

            -> 쿼리를 딕셔너리로 분리 
                -> sorted 함수를 이용하여 키 값을 기준으로 정렬 
                    -> dict.formkeys 를 이용하여 빈값으로 변경
                        -> urlencode(doseq=True) 함수를 이용해 딕셔너리를 쿼리로 재조합
                            -> unqoute를 이용해 URL인코딩이 되어 있는 경우 디코딩
                                -> urljoin으로 올바른 URL로 조합
            """
            return urljoin(self.URL, unquote(urlencode(dict.fromkeys(sorted(parse_qs(urinfo.query)), ''), doseq=True)))
        # 쿼리가 존재하지 않는 경우 URL 반환
        return URL

    def empty_url(self, URL):
        # URL이 존재하는지 체크 and 해당 URL이 Crawling domain과 일치하는지 체크
        if URL and self.FirstURLParse.netloc == urlparse(URL).netloc:
            return self.qs_value_empty(URL)
        return

    def init_engine(self) -> None:
        # sqlite에 데이터 저장을 위해 Engine Class 생성
        self.engine = Engine()