from tldextract import extract
from Search.payloads import *
from Storage.DB import Engine

class Vulndb:
    def __init__(self, tabname, URL, **info):
        engine = Engine()
        engine.init_conn(tabname)
        data = engine.sqlite_engine_auto_load_select()
        ReflectedXSS(data, URL, **info)
        # OpenRedirect(data)
        # SQLInjection(data)
        # LocalFileInclusion(data)