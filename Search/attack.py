from threading import Thread
from tldextract import extract
from Storage.DB import Engine
from base64 import b64decode
from Search.Vulndb import * 

class VulnFuzz:
    def __init__(self, tabname, **info):
        engine = Engine()
        engine.init_conn(tabname)
        data = engine.sqlite_engine_auto_load_select()
        print('========== fuzzing start ==========')
        r1 = Thread(target=ReflectedXSS, kwargs={'datatable':data,**info})
        r2 = Thread(target=OpenRedirect, kwargs={'datatable':data,**info})
        r3 = Thread(target=ServerSideTemplateInjection, kwargs={'datatable':data,**info})
        r1.start()
        r2.start()
        r3.start()
        r1.join()
        r2.join()
        r3.join()

        # Thread(target=SQLInjection, kwargs={'datatable':data,**info}).start()
        # Thread(target=CrossSiteRequestForgery, kwargs={'datatable':data,**info}).start()
        # Thread(target=NOSQLInjection, kwargs={'datatable':data,**info}).start()
        # Thread(target=OSCommandInjection, kwargs={'datatable':data,**info}).start()
        # Thread(target=LocalFileInclusion, kwargs={'datatable':data,**info}).start()
        # Thread(target=RemoteFileInclusion, kwargs={'datatable':data,**info}).start()