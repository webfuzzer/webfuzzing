from tldextract import extract
from Storage.DB import Engine
from base64 import b64decode
from Search.Vulndb import *

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

class VulnFuzz:
    def __init__(self, tabname, URL, **info):
        engine = Engine()
        engine.init_conn(tabname)
        data = engine.sqlite_engine_auto_load_select()
        # headers = content[attr['request_headers']], 
        #             cookies = content[attr['request_cookies']], 
        #             data = content[attr['data']],
        #             method = content[attr['method']],
        for content in data:
            args = {
                'current_url':content[attr['current_url']],
                'html':b64decode(content[attr['body']]).decode(),
                'headers':content[attr['request_headers']], 
                'cookies':content[attr['request_cookies']], 
                'data':content[attr['data']],
                'method':content[attr['method']],
            }
            ReflectedXSS(**args, **info)
            # OpenRedirect(data)
        # SQLInjection(data)
        # LocalFileInclusion(data)