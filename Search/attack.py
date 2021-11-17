from threading import Thread
from tldextract import extract
from Storage.DB import Engine
from base64 import b64decode
from Search.Vulndb import * 

class VulnFuzz:
    def __init__(self, tabname, URL, **info):
        engine = Engine()
        engine.init_conn(tabname)
        data = engine.sqlite_engine_auto_load_select()
        print('========== fuzzing start ==========')
        Thread(target=ReflectedXSS, kwargs={'datatable':data,**info}).start()
        Thread(target=OpenRedirect, kwargs={'datatable':data,**info}).start()
        # SQLInjection(data)
        # LocalFileInclusion(data)