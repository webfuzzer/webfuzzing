"""
기본적인 공격 벡터 : QueryString, data(post data), cookies, headers, fragment, path
"""
from urllib.parse import parse_qs, urlencode, urlparse, urljoin
from Search.payloads import fuzzer_payloads
from bs4 import BeautifulSoup, Comment
from Utils.utils import RandomString, double_randint
from base64 import b64decode
from Crawler import sessions
import re

__all__ = [
    'ReflectedXSS',
    'OpenRedirect',
    'SQLInjection',
    'CrossSiteRequestForgery',
    'NOSQLInjection',
    'OSCommandInjection',
    'ServerSideTemplateInjection',
    'LocalFileInclusion',
    'RemoteFileInclusion'
]

def init_session():
    return sessions()(Site=False)

attr = {
    'first_url':1,
    'current_url':2,
    'method':3,
    'history':4,
    'history_len':5,
    'response_url':6,
    'response_cookies':7,
    'response_headers':8,
    'response_status':9,
    'request_cookies':10,
    'request_headers':11,
    'data':12,
    'body':13
}

class ReflectedXSS:
    def __init__(self, datatable):
        """
        ReflectedXSS Class:
            attack vector
                [
                    1:QueryString,
                    2:data(post data),
                    3:fragment,
                    4:cookies,
                    5:headers,
                    6:path,
                ]
        1. sqlite3 database의 정보를 가져와 response body안에 headers, cookies, querystring, data, path 등 request 정보가 response body에 담겨있는지 체크
        2. 만약 1번 조건에 종촉할 경우 request 정보를 하나 씩 랜덤값으로 바꾼 뒤 요청하여 response body를 가지고 랜덤값이 출력됐는지 체크
        3. 만약 2번 조건에 종촉할 경우 html injection을 시도하기 위해 request 정보를 html 태그로 바꾼 다음 bs4.BeautifulSoup를 이용하여 search
        4. 만약 4번 조건에 종촉할 경우 XSS를 발생시킬 수 있는(alert) 페이로드를 주입하여 해당 태그들의 attrs, tag name 비교하여 체크
        5. 만약 모든 조건에 만족할 경우 보고서 작성 또는 terminal에 print
        6. exit
        """
        self.element_eq_pay, \
            self.element_empty_value, \
                self.element_event, \
                    self.script_pay, \
                        self.alert_box_check, \
                            self.attribute_injection, \
                                self.cross_site_scriping_pay\
                                    = fuzzer_payloads.xss()
        self.REGEX_sub = """([`'"](?!'"`).*?[`'"])|(\/\/.*)|(\/\*((.|\n)*)\*\/)"""
        self.datatable = datatable
        self.sess = sessions().init_sess()
        self.input_payload = ''
        self.message = False
        self.vuln_level = 0
        self.req_info = {}

        self.exploit()

    def exploit(self):
        for content in self.datatable:
            self.body = b64decode(content[attr['body']]).decode()
            self.current_url = content[attr['current_url']]
            self.urinfo = urlparse(self.current_url)
            self.method = content[attr['method']]
            print(self.current_url)
            try:
                self.search_text(
                    data = content[attr['data']],
                    headers = content[attr['request_headers']],
                    cookies = content[attr['request_cookies']],
                )
            except:
                continue

    def search_text(self, data, headers, cookies):
        rs = RandomString(5)
        
        if self.urinfo.query:
            qs = parse_qs(self.urinfo.query)
            for key, value in qs.items():
                if type(value) == list:
                    value = value[0]
                self.req_info = {'vector':'qs','key':key, 'input':dict(qs)}
                if value in self.body and (rs in self.string_search_text(rs)):
                    self.html_injection_test()

        if data:
            for key, value in data.items():
                self.req_info = {'vector':'data', 'key':key, 'input':dict(data)}
                if value in self.body and (rs in self.string_search_text(rs)):
                    self.html_injection_test()

        if cookies:
            for key, value in cookies.items():
                self.req_info = {'vector':'cookies','key':key, 'input':dict(cookies)}
                if value in self.body and (rs in self.string_search_text(rs)):
                    self.html_injection_test()

        if headers:
            for key, value in headers.items():
                self.req_info = {'vector':'headers','key':key, 'input':dict(headers)}
                if value in self.body and (rs in self.string_search_text(rs)):
                    self.html_injection_test()

    def string_search_text(self, rs):
        """
        search for a random string in response body
        """
        temp = self.req_info['input']
        rs = rs
        if self.req_info['vector'] == 'fragment':
            r = self.sess.request(self.method, self.urinfo._replace(**{self.req_info['vector']:rs}).geturl())
        elif self.req_info['vector'] == 'qs':
            temp[self.req_info['key']] = rs
            r = self.sess.request(self.method, self.urinfo._replace(query=urlencode(temp, doseq=True)).geturl())
        else:
            temp[self.req_info['key']] = rs
            r = self.sess.request(self.method, self.current_url, **{self.req_info['vector']:temp})

        return r.text
    
    def html_injection_test(self):
        for attr in self.attribute_injection:
            attr_key = RandomString(5)
            attr_val = RandomString(5)
            rs = attr.format(attr_key, attr_val)
            test = self.string_search_text(rs)
            soup = BeautifulSoup(test, 'html.parser')
            if soup.find(attrs={attr_key.lower():attr_val}):
                self.message = (rs, self.req_info)
                if self.cross_site_scripting_test('attr'):
                    return
        for element in self.element_eq_pay:
            attribute_key_rs = RandomString(5)
            attribute_value_rs = RandomString(5)
            inner_text_rs = RandomString(5)
            rs = element.format(attribute_key_rs,attribute_value_rs, inner_text_rs)
            soup = BeautifulSoup(self.string_search_text(rs), 'html.parser')
            if soup.find(attrs={attribute_key_rs.lower():attribute_value_rs}, text=inner_text_rs) or soup.find(attrs={attribute_value_rs.lower():attribute_value_rs}) or soup.find(text=inner_text_rs):
                self.message = (rs, self.req_info)
                if self.cross_site_scripting_test('element'):
                    return
            elif [rs in i.text for i in soup.find_all('script')]:
                self.message = (rs, self.req_info)
                if self.cross_site_scripting_test('script'):
                    return
            elif [rs in i for i in soup.find_all(text=lambda s: isinstance(s, Comment))]:
                self.message = (rs, self.req_info)
                if self.cross_site_scripting_test('comment'):
                    return

    def cross_site_scripting_test(self, vector):
        """
        전체적으로 payloads 리스트 수정 할 계획( class으로 가져와 self 호출하기 )
        1. vector == 'attr':
            element_event in attr in box for loop
        2. vector in ['comment', 'element']:
            cross_site_scripting_pay for loop
        3. vector == 'script':
            
        4. vector == 'style'
        """
        if vector == 'attr':
            for element_event in self.element_event:
                for attr in self.attribute_injection:
                    for box in self.alert_box_check:
                        rs = attr.format(element_event, box)
                        soup = BeautifulSoup(self.string_search_text(rs), 'html.parser')
                        if soup.find(attrs={element_event.lower():box}):
                            print("="*50)
                            print('attrs 취약점 발견!')
                            print(self.current_url)
                            print(rs)
                            return True

        elif vector in ['comment', 'element']:
            for alert in self.cross_site_scriping_pay:
                alert_soup = BeautifulSoup(alert, 'html.parser').find()
                return_soup = BeautifulSoup(self.string_search_text(alert), 'html.parser')
                if return_soup.find(attrs=alert_soup.attrs, name=alert_soup.name, text=alert_soup.text):
                    print("="*50)
                    print('element 취약점 발견!!!!')
                    print(self.current_url)
                    print(return_soup)
                    return True
            return False
        elif vector == 'script':
            for script_pay in self.script_pay:
                soup = BeautifulSoup(self.string_search_text(script_pay), 'html.parser')
                for script_tag in soup.find_all('script'):
                    temp = re.sub(self.REGEX_sub, '', script_tag.string)
                    if True in [i in temp for i in [ 'alert()', 'prompt()', 'print()', 'confirm()']]:
                        print("="*50)
                        print('script 취약점 발견!')
                        print(self.current_url)
                        print(script_pay)
                        return True
        return False

class OpenRedirect:
    def __init__(self, datatable):
        self.database = datatable
        self.sess = sessions().init_sess()
        self.open_redirect_pay = fuzzer_payloads.openredirect()

        self.exploit()

    def exploit(self):
        for content in self.database:
            self.body = b64decode(content[attr['body']]).decode()
            self.current_url = content[attr['current_url']]
            self.urinfo = urlparse(self.current_url)
            self.method = content[attr['method']]
            try:
                self.request(
                    data = content[attr['data']],
                    headers = content[attr['request_headers']],
                    cookies = content[attr['request_cookies']],
                )
            except:
                continue

    def request(self, data, headers, cookies):
        if self.urinfo.query:
            qs = parse_qs(self.urinfo.query)
            for key, value in qs.items():
                if type(value) == list:
                    value = value[0]
                self.req_info = {'vector':'qs','key':key, 'input':dict(qs)}
                self.redirect_check()
        if data:
            for key, value in data.items():
                self.req_info = {'vector':'data', 'key':key, 'input':dict(data)}
                self.redirect_check()
        if cookies:
            for key, value in cookies.items():
                self.req_info = {'vector':'cookies','key':key, 'input':dict(cookies)}
                self.redirect_check()
        if headers:
            for key, value in headers.items():
                self.req_info = {'vector':'headers','key':key, 'input':dict(headers)}
                self.redirect_check()

    def pay_request(self, pay):
        """
        search for a random string in response body
        """
        temp = self.req_info['input']
        pay = pay
        if self.req_info['vector'] == 'fragment':
            r = self.sess.request(self.method, self.urinfo._replace(**{self.req_info['vector']:pay}).geturl())
        elif self.req_info['vector'] == 'qs':
            temp[self.req_info['key']] = pay
            r = self.sess.request(self.method, self.urinfo._replace(query=urlencode(temp, doseq=True)).geturl())
        else:
            temp[self.req_info['key']] = pay
            r = self.sess.request(self.method, self.current_url, **{self.req_info['vector']:temp})

        return r

    def redirect_check(self):
        for redirect in self.open_redirect_pay:
            self.r = self.pay_request(redirect)
            if self.r.headers['Location']:
                print('open redirect 취약점 감지됨')
            soup = BeautifulSoup(self.r.text, 'html.parser')
            for script in soup.find_all('script'):
                for js in script.string.splitlines():
                    if js in ['locatio', 'open'] and redirect in js:
                        print('open redirect 취약점 감지됨')

class SQLInjection:
    def __init__(self, datatable) -> None:
        self.database = datatable
        self.sess = sessions.init_sess()

class CrossSiteRequestForgery:
    def __init__(self, datatable) -> None:
        self.database = datatable
        self.sess = sessions.init_sess()

class NOSQLInjection:
    def __init__(self, datatable) -> None:
        self.database = datatable
        self.sess = sessions.init_sess()

class OSCommandInjection:
    def __init__(self, datatable) -> None:
        self.database = datatable
        self.sess = sessions.init_sess()

class ServerSideTemplateInjection:
    def __init__(self, datatable) -> None:
        self.database = datatable
        self.sess = sessions.init_sess()
        self.pay = fuzzer_payloads.ssti()
        self.operator = [
            '+',
            '-',
            '*',
            '/',
            '%',
            '**',
            '^',
            '&',
            '|',
        ]
        
        self.exploit()
    
    def exploit(self):
        for content in self.datatable:
            self.body = b64decode(content[attr['body']]).decode()
            self.current_url = content[attr['current_url']]
            self.urinfo = urlparse(self.current_url)
            self.method = content[attr['method']]
            self.request_key = {
                'data':content[attr['data']],
                'headers':content[attr['request_headers']],
                'cookies':content[attr['request_cookies']],
            }
            self.random_operator()

    def search_text(self, rs):
        if self.urinfo.query:
            qs = parse_qs(self.urinfo.query)
            for key, value in qs.items():
                if type(value) == list:
                    value = value[0]
                self.req_info = {'vector':'qs','key':key, 'input':dict(qs)}
                if value in self.body and (rs in self.string_search_text(rs)):
                    print('SSTI 취약점 발생함!')
                    print(self.req_info, self.method, self.current_url)

        if self.request_key['data']:
            for key, value in self.request_key['data'].items():
                self.req_info = {'vector':'data', 'key':key, 'input':dict(self.request_key['data'])}
                if value in self.body and (rs in self.string_search_text(rs)):
                    print('SSTI 취약점 발생함!')
                    print(self.req_info, self.method, self.current_url)

        if self.request_key['cookies']:
            for key, value in self.request_key['cookies'].items():
                self.req_info = {'vector':'cookies','key':key, 'input':dict(self.request_key['cookies'])}
                if value in self.body and (rs in self.string_search_text(rs)):
                    print('SSTI 취약점 발생함!')
                    print(self.req_info, self.method, self.current_url)

        if self.request_key['headers']:
            for key, value in self.request_key['headers'].items():
                self.req_info = {'vector':'headers','key':key, 'input':dict(self.request_key['headers'])}
                if value in self.body and (rs in self.string_search_text(rs)):
                    print('SSTI 취약점 발생함!')
                    print(self.req_info, self.method, self.current_url)

    def string_search_text(self, rs):
        """
        search for a random string in response body
        """
        temp = self.req_info['input']
        rs = rs
        if self.req_info['vector'] == 'fragment':
            r = self.sess.request(self.method, self.urinfo._replace(**{self.req_info['vector']:rs}).geturl())
        elif self.req_info['vector'] == 'qs':
            temp[self.req_info['key']] = rs
            r = self.sess.request(self.method, self.urinfo._replace(query=urlencode(temp, doseq=True)).geturl())
        else:
            temp[self.req_info['key']] = rs
            r = self.sess.request(self.method, self.current_url, **{self.req_info['vector']:temp})

        return r.text
    def random_operator(self):
        for op in self.operator:
            oper = double_randint(2)
            result = eval(f'{oper[0]}{op}{oper[1]}')
            self.search_text(result)

class LocalFileInclusion:
    def __init__(self, datatable) -> None:
        self.database = datatable
        self.sess = sessions.init_sess()

class RemoteFileInclusion:
    def __init__(self, datatable) -> None:
        self.database = datatable
        self.sess = sessions.init_sess()