from tldextract import extract
from Storage.DB import Engine
from base64 import b64decode
from Search.Vulndb import * 

class VulnFuzz:
    def __init__(self, tabname, URL, **info):
        engine = Engine()
        engine.init_conn(tabname)
        data = engine.sqlite_engine_auto_load_select()
        # headers = content[attr['request_headers']], 
        # cookies = content[attr['request_cookies']], 
        # data = content[attr['data']],
        # method = content[attr['method']],
        ReflectedXSS(data, **info)
            # OpenRedirect(data)
        # SQLInjection(data)
        # LocalFileInclusion(data)