from urllib.parse import parse_qs, urlencode, urlparse, urljoin
from Search.payloads import fuzzer_payloads
from bs4 import BeautifulSoup, Comment
from Utils.utils import RandomString, double_randint
from requests.exceptions import TooManyRedirects, ConnectTimeout
from base64 import b64decode
from Crawler import sessions
import warnings
import re

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

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

STRING_OR_COMMENT_REMOVE_REGEX = """([`'"](?!'"`).*?[`'"])|(\/\/.*)|(\/\*((.|\n)*)\*\/)"""
LINUX_DEFAULT_FILE_ETC_PASSWD_FORMAT_REGEX = r"^(#.*|[a-z]*:[^:]*:[0-9]*:[0-9]*:[^:]*:/[^:]*:/[^:]*)$"

class ReflectedXSS:
    def __init__(self, datatable, **info):
        self.element_eq_pay, \
            self.element_empty_value, \
                self.element_event, \
                    self.script_pay, \
                        self.alert_box_check, \
                            self.attribute_injection, \
                                self.cross_site_scriping_pay\
                                    = fuzzer_payloads.xss()
        self.datatable = datatable
        self.sess = sessions().init_sess()
        self.input_payload = ''
        self.message = False
        self.vuln_level = 0
        self.req_info = {}
        self.info = info

        self.exploit()

    def exploit(self):
        for content in self.datatable:
            self.body = b64decode(content[attr['body']]).decode()
            self.current_url = content[attr['current_url']]
            self.urinfo = urlparse(self.current_url)
            self.method = content[attr['method']]
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
        temp = self.req_info['input']
        rs = rs
        if self.req_info['vector'] == 'fragment':
            r = self.sess.request(self.method, self.urinfo._replace(**{self.req_info['vector']:rs}).geturl(), **self.info)
        elif self.req_info['vector'] == 'qs':
            temp[self.req_info['key']] = rs
            r = self.sess.request(self.method, self.urinfo._replace(query=urlencode(temp, doseq=True)).geturl(), **self.info)
        else:
            temp[self.req_info['key']] = rs
            r = self.sess.request(self.method, self.current_url, **{self.req_info['vector']:temp}, **self.info)

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
                    temp = re.sub(STRING_OR_COMMENT_REMOVE_REGEX, '', script_tag.string)
                    if True in [i in temp for i in [ 'alert()', 'prompt()', 'print()', 'confirm()']]:
                        print("="*50)
                        print('script 취약점 발견!')
                        print(self.current_url)
                        print(script_pay)
                        return True
        return False

class OpenRedirect:
    def __init__(self, datatable, **info):
        self.database = datatable
        self.open_redirect_pay = fuzzer_payloads.openredirect()
        self.info = info        
        self.info.setdefault('allow_redirects', False)
        self.exploit()

    def exploit(self):
        for content in self.database:
            self.sess = sessions().init_sess()
            self.current_url = content[attr['current_url']]
            self.urinfo = urlparse(self.current_url)
            self.method = content[attr['method']]
            self.case_request(
                data = content[attr['data']],
                headers = content[attr['request_headers']],
                cookies = content[attr['request_cookies']],
            )
            self.sess.close()
            continue

    def case_request(self, data, headers, cookies):
        if headers.get('Content-Length'):
            headers['Content-Length'] = ''
        if self.urinfo.query:
            qs = parse_qs(self.urinfo.query)
            for key, value in qs.items():
                if type(value) == list:
                    value = value[0]
                self.req_info = {'vector':'qs','key':key, 'input':dict(qs)}
                self.payloads_injection()
        if data:
            for key, value in data.items():
                self.req_info = {'vector':'data', 'key':key, 'input':dict(data)}
                self.payloads_injection()
        if cookies:
            for key, value in cookies.items():
                self.req_info = {'vector':'cookies','key':key, 'input':dict(cookies)}
                self.payloads_injection()
        if headers:
            for key, value in headers.items():
                self.req_info = {'vector':'headers','key':key, 'input':dict(headers)}
                self.payloads_injection()

    def payloads_injection(self):
        self.is_redirect_check()
        for redirect_payloads in self.open_redirect_pay:
            r = self.redirect_check_before_request(redirect_payloads.format(self.urinfo.netloc))
            if r.is_redirect or r.headers.get('Location'):
                print('='*50)
                print('[header] : open redirect 취약점 감지됨')
                print(self.current_url)
                print(self.req_info)
                return
            soup = BeautifulSoup(r.text, 'html.parser')
            for script in soup.find_all('script'):
                for js in script.string.splitlines():
                    temp = re.sub(STRING_OR_COMMENT_REMOVE_REGEX, '', js)
                    if ('location' in temp or 'open' in temp) and ('example.com' in temp or 'google.com' in temp):
                        print('='*50)
                        print('[js] : open redirect 취약점 감지됨')
                        print(self.current_url)
                        print(self.req_info)
                        return

    def pay_request(self, pay = '', allow_redirects = False):
        if pay:
            temp = self.req_info['input']
            pay = pay
            if self.req_info['vector'] == 'fragment':
                r = self.sess.request(self.method, self.urinfo._replace(fragment=pay).geturl(), **(self.info | {'allow_redirects':allow_redirects}))
            elif self.req_info['vector'] == 'qs':
                temp[self.req_info['key']] = pay
                r = self.sess.request(self.method, self.urinfo._replace(query=urlencode(temp, doseq=True)).geturl(), **(self.info | {'allow_redirects':allow_redirects}))
            else:
                temp[self.req_info['key']] = pay
                r = self.sess.request(self.method, self.current_url, **{self.req_info['vector']:temp}, **(self.info | {'allow_redirects':allow_redirects}))
        else:
            if self.req_info['vector'] == 'fragment':
                r = self.sess.request(self.method, self.urinfo._replace(fragment='').geturl(), **(self.info | {'allow_redirects':allow_redirects}))
            elif self.req_info['vector'] == 'qs':
                r = self.sess.request(self.method, self.urinfo._replace(query='').geturl(), **(self.info | {'allow_redirects':allow_redirects}))
            else:
                r = self.sess.request(self.method, self.current_url, **{self.req_info['vector']:''}, **(self.info | {'allow_redirects':allow_redirects}))

        return r

    def is_redirect_check(self):
        r = self.pay_request(allow_redirects=False)
        if r.is_redirect:
            self.is_redirect = True
        else:
            self.is_redirect = False

    def redirect_check_before_request(self, pay):

        if self.is_redirect:
            r = self.pay_request(pay, allow_redirects=True)
            if not len(r.history):
                return r
            r.history = [r.history[-1]]

            return r

        else:
            r = self.pay_request(pay)
            return r

class ServerSideTemplateInjection:
    def __init__(self, datatable, **info) -> None:
        self.database = datatable
        self.info = info
        self.pay = fuzzer_payloads.ssti()
        self.exploit()
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
    
    def exploit(self):
        for content in self.database:
            self.sess = sessions().init_sess()
            self.body = b64decode(content[attr['body']]).decode()
            self.current_url = content[attr['current_url']]
            self.urinfo = urlparse(self.current_url)
            self.method = content[attr['method']]
            try:
                self.request_key = {
                    'data':content[attr['data']],
                    'headers':content[attr['request_headers']],
                    'cookies':content[attr['request_cookies']],
                }
                self.search_text()
            except Exception as e:
                continue

    def search_text(self):
        if self.urinfo.query:
            qs = parse_qs(self.urinfo.query)
            for key, value in qs.items():
                if type(value) == list:
                    value = value[0]
                self.req_info = {'vector':'qs','key':key, 'input':dict(qs)}
                if value in self.body:
                    self.template_syntax_injection()

        if self.request_key['data']:
            for key, value in self.request_key['data'].items():
                self.req_info = {'vector':'data', 'key':key, 'input':dict(self.request_key['data'])}
                if value in self.body:
                    self.template_syntax_injection()

        if self.request_key['cookies']:
            for key, value in self.request_key['cookies'].items():
                self.req_info = {'vector':'cookies','key':key, 'input':dict(self.request_key['cookies'])}
                if value in self.body:
                    self.template_syntax_injection()

        if self.request_key['headers']:
            for key, value in self.request_key['headers'].items():
                self.req_info = {'vector':'headers','key':key, 'input':dict(self.request_key['headers'])}
                if value in self.body:
                    self.template_syntax_injection()

    def string_search_text(self, rs):
        temp = self.req_info['input']
        rs = rs
        if self.req_info['vector'] == 'fragment':
            r = self.sess.request(self.method, self.urinfo._replace(**{self.req_info['vector']:rs}).geturl())
        elif self.req_info['vector'] == 'qs':
            temp[self.req_info['key']] = rs
            r = self.sess.request(self.method, self.current_url, params=urlencode(temp, doseq=True))
        else:
            temp[self.req_info['key']] = rs
            r = self.sess.request(self.method, self.current_url, **{self.req_info['vector']:temp})
        return r.text

    def template_syntax_injection(self):
        for pay in self.pay:
            for op in self.operator:
                oper = double_randint(2)
                calc = f'{oper[0]}{op}{oper[1]}'
                result = eval(calc)
                self.search_text(result)
                try:
                    if result in self.string_search_text(pay.format(result)):
                        print("="*50)
                        print('SSTI 취약점 발생함!')
                        print(self.current_url)
                        print(self.req_info, self.method, self.current_url)
                        return True
                except TooManyRedirects as e:
                    continue
        return False

class SQLInjection:
    def __init__(self, datatable) -> None:
        self.database = datatable
        self.sess = sessions().init_sess()

class NOSQLInjection:
    def __init__(self, datatable, **info) -> None:
        self.info = info
        self.database = datatable
        self.sess = sessions().init_sess()
        self.pay = fuzzer_payloads.NOSQLInjection()

        self.exploit()

    def exploit(self):
        for content in self.database:
            self.sess = sessions().init_sess()
            self.current_url = content[attr['current_url']]
            self.urinfo = urlparse(self.current_url)
            self.method = content[attr['method']]
            try:
                self.request_key = {
                    'data':content[attr['data']],
                    'headers':content[attr['request_headers']],
                    'cookies':content[attr['request_cookies']],
                }
                self.search_text()
            except Exception as e:
                print('NOSQLInjection :', e)
                continue

    def search_text(self):
        if self.urinfo.query:
            qs = parse_qs(self.urinfo.query)
            for key, value in qs.items():
                if type(value) == list:
                    value = value[0]
                self.req_info = {'vector':'qs','key':key, 'input':dict(qs)}
                self.nosql_where_sleep_injection()

        if self.request_key['data']:
            for key, value in self.request_key['data'].items():
                self.req_info = {'vector':'data', 'key':key, 'input':dict(self.request_key['data'])}
                self.nosql_where_sleep_injection()

        if self.request_key['cookies']:
            for key, value in self.request_key['cookies'].items():
                self.req_info = {'vector':'cookies','key':key, 'input':dict(self.request_key['cookies'])}
                self.nosql_where_sleep_injection()

        if self.request_key['headers']:
            for key, value in self.request_key['headers'].items():
                self.req_info = {'vector':'headers','key':key, 'input':dict(self.request_key['headers'])}
                self.nosql_where_sleep_injection()

    def string_search_text(self, rs, array = False,timeout=3):
        temp = self.req_info['input']
        rs = rs
        if self.req_info['vector'] == 'fragment':
            r = self.sess.request(self.method, self.urinfo._replace(**{self.req_info['vector']:rs}).geturl(), **(self.info | {'timeout':timeout}))
        elif self.req_info['vector'] == 'qs':
            temp[self.req_info['key']] = rs
            r = self.sess.request(self.method, self.current_url, params=urlencode(temp, doseq=True), **(self.info | {'timeout':timeout}))
        else:
            temp[self.req_info['key']] = rs
            r = self.sess.request(self.method, self.current_url, **{self.req_info['vector']:temp}, **(self.info | {'timeout':timeout}))
        return r.text

    def nosql_where_sleep_injection(self):
        for pay in self.pay:
            try:
                self.string_search_text(pay)
            except ConnectTimeout:
                print("="*50)
                print("NOSQL Injection 취약점 발견!!")
                print(self.req_info)
                return

class LocalFileInclusion:
    def __init__(self, datatable, **info) -> None:
        self.info = info
        self.database = datatable
        self.sess = sessions().init_sess()
        self.pay = fuzzer_payloads.lfi()
        self.OPTIONS = (re.MULTILINE | re.IGNORECASE | re.DOTALL)

        self.exploit()

    def exploit(self):
        for content in self.database:
            self.sess = sessions().init_sess()
            self.body = b64decode(content[attr['body']]).decode()
            self.current_url = content[attr['current_url']]
            self.urinfo = urlparse(self.current_url)
            self.method = content[attr['method']]
            try:
                self.request_key = {
                    'data':content[attr['data']],
                    'headers':content[attr['request_headers']],
                    'cookies':content[attr['request_cookies']],
                }
                self.search_text()
            except Exception as e:
                print('LFI :', e)
                continue

    def search_text(self):
        if self.urinfo.query:
            qs = parse_qs(self.urinfo.query)
            for key, value in qs.items():
                if type(value) == list:
                    value = value[0]
                self.req_info = {'vector':'qs','key':key, 'input':dict(qs)}
                self.etc_passwd_search()

        if self.request_key['data']:
            for key, value in self.request_key['data'].items():
                self.req_info = {'vector':'data', 'key':key, 'input':dict(self.request_key['data'])}
                self.etc_passwd_search()

        if self.request_key['cookies']:
            for key, value in self.request_key['cookies'].items():
                self.req_info = {'vector':'cookies','key':key, 'input':dict(self.request_key['cookies'])}
                self.etc_passwd_search()

        if self.request_key['headers']:
            for key, value in self.request_key['headers'].items():
                self.req_info = {'vector':'headers','key':key, 'input':dict(self.request_key['headers'])}
                self.etc_passwd_search()

    def string_search_text(self, rs):
        temp = self.req_info['input']
        rs = rs
        if self.req_info['vector'] == 'fragment':
            r = self.sess.request(self.method, self.urinfo._replace(**{self.req_info['vector']:rs}).geturl(), **self.info)
        elif self.req_info['vector'] == 'qs':
            temp[self.req_info['key']] = rs
            r = self.sess.request(self.method, self.current_url, params=urlencode(temp, doseq=True), **self.info)
        else:
            temp[self.req_info['key']] = rs
            r = self.sess.request(self.method, self.current_url, **{self.req_info['vector']:temp}, **self.info)
        return r.text

    def etc_passwd_search(self):
        for pay in self.pay:
            r = self.string_search_text(pay)
            compile = re.compile(LINUX_DEFAULT_FILE_ETC_PASSWD_FORMAT_REGEX, self.OPTIONS)
            if len(compile.findall(r)):
                print("="*50)
                print("LFI 취약점 발견(maybe?)!!")
                print(self.req_info)
                print(self.current_url)
                return

class CrossSiteRequestForgery:
    def __init__(self, datatable, **info) -> None:
        self.info = info
        self.database = datatable
        self.sess = sessions().init_sess()

    def exploit(self):
        for content in self.database:
            self.sess = sessions().init_sess()
            self.body = b64decode(content[attr['body']]).decode()
            self.current_url = content[attr['current_url']]
            self.urinfo = urlparse(self.current_url)
            self.method = content[attr['method']]
            try:
                self.request_key = {
                    'data':content[attr['data']],
                    'headers':content[attr['request_headers']],
                    'cookies':content[attr['request_cookies']],
                }
                self.search_text()
            except Exception as e:
                print('NOSQLInjection :', e)
                continue
    
    def search_text(self):
        if self.urinfo.query:
            qs = parse_qs(self.urinfo.query)
            for key, value in qs.items():
                if type(value) == list:
                    value = value[0]
                self.req_info = {'vector':'qs','key':key, 'input':dict(qs)}
                self.nosql_where_sleep_injection()

        if self.request_key['data']:
            for key, value in self.request_key['data'].items():
                self.req_info = {'vector':'data', 'key':key, 'input':dict(self.request_key['data'])}
                self.nosql_where_sleep_injection()

        if self.request_key['cookies']:
            for key, value in self.request_key['cookies'].items():
                self.req_info = {'vector':'cookies','key':key, 'input':dict(self.request_key['cookies'])}
                self.nosql_where_sleep_injection()

        if self.request_key['headers']:
            for key, value in self.request_key['headers'].items():
                self.req_info = {'vector':'headers','key':key, 'input':dict(self.request_key['headers'])}
                self.nosql_where_sleep_injection()

    def string_search_text(self, rs, timeout=3):
        temp = self.req_info['input']
        rs = rs
        if self.req_info['vector'] == 'fragment':
            r = self.sess.request(self.method, self.urinfo._replace(**{self.req_info['vector']:rs}).geturl(), **(self.info | {'timeout':timeout}))
        elif self.req_info['vector'] == 'qs':
            temp[self.req_info['key']] = rs
            r = self.sess.request(self.method, self.current_url, params=urlencode(temp, doseq=True), **(self.info | {'timeout':timeout}))
        else:
            temp[self.req_info['key']] = rs
            r = self.sess.request(self.method, self.current_url, **{self.req_info['vector']:temp}, **(self.info | {'timeout':timeout}))
        return r.text

    def csrf_token_matching(self):
        pass

class OSCommandInjection:
    def __init__(self, datatable) -> None:
        self.database = datatable
        self.sess = sessions().init_sess()

class RemoteFileInclusion:
    def __init__(self, datatable) -> None:
        self.database = datatable
        self.sess = sessions().init_sess()