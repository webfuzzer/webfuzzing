from urllib.parse import urlencode, parse_qs, quote, unquote, urlparse
from tldextract import extract
from bs4 import BeautifulSoup
from request import *

class Crawler:
    def __init__(self, url, **args) -> None:
        self.url = url

        self._urlparams = urlparse(url)
        self.tmp_tld = extract(self.url)

        self.tags = {
            'href':['a', 'link', 'area'],
            'src':['img', 'script', 'iframe'],
            'action':['form']
        }

        user_agent = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        }

        args.setdefault('timeout', 3)
        args.setdefault('headers', user_agent)
        
        self.args = args


    def tag(self, subdomain = False) -> None:

        r = request(self.url, **self.args)

        body = r.get()['body']
        soup = BeautifulSoup(body, 'html.parser')
        self.url = []

        for attribute, tagname in self.tags.items():
            for element in soup.find_all(tagname):
                self.url.append(element.get(attribute))

        self.urlparser(subdomain)

        for i in self.url:
            print(i)

    def urlparser(self, subdomain = False) -> None:

        index = 0
        temp = self.url
        # for 으로 for i in self.url을 한다고 하여도 list.pop 으로 인해 요소가 삭제되면서 리스트 index를 잘못 잡게 되면서 몇개씩 건너뛰게 됨
        '''
        >>> 'bug'
        'bug'
        >>> index = 0
        >>> a = [1,2,3,2,2,3,4,6,5,6]
        >>> for i in a:
        ...     if i%2 == 0:
        ...             a.pop(index)
        ...     index += 1
        ...
        2
        2
        4
        6
        >>> a
        [1, 3, 2, 3, 6, 5]
        >>> 'while'
        'while'
        >>> a = [1,2,3,2,2,3,4,6,5,6]
        >>> index = 0
        >>> while index < len(a):
        ...     if a[index] % 2 == 0:
        ...             a.pop(index)
        ...     else:
        ...             index += 1
        ...
        2
        2
        2
        4
        6
        6
        >>> a
        [1, 3, 3, 5]
        '''
        # while을 이용하여 모든 요소 체크
        while index < len(temp):
            url = temp[index]
            if url:
                urlresult = urlparse(url)

                if (not urlresult.scheme in ['','http','https']) or (urlresult.path == '/' or not urlresult.path):
                    # scheme가 '', 'http', 'https'이 들어있지 않은 경우 도는 경로가 / 이거나 없다면 요소 삭제
                    self.url.pop(index)

                elif urlresult.netloc:

                    if subdomain:
                        # 만약 subdomain까지 URL을 파싱해야되는 경우 True
                        tld = extract(url)
                        # subdomain, domain, suffix를 가져오기 위한 tldextract 모듈 사용

                        if (tld.domain + tld.suffix) != (self.tmp_tld.domain + self.tmp_tld.suffix):
                            # 파싱한 URL의 domain + suffix와 요청한 URL의 domain + suffix가 일치하지 않는 경우 요소 삭제
                            self.url.pop(index)
                        else:
                            index += 1
                    else:
                        if urlresult.netloc != self._urlparams.netloc:
                            # 파싱한 url의 netloc와 요청한 URL의 netloc가 일치하지 않는 경우 요소 삭제
                            self.url.pop(index)

                        else:
                            index += 1
                else:
                    index += 1
            else:
                self.url.pop(index)

C = Crawler('https://www.naver.com')
C.tag(subdomain=True)