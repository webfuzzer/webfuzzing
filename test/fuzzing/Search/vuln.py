from Storage.DB import Engine
from Search.payloads import *

class Vulndb:
    def __init__(self, tabname):
        engine = Engine()
        engine.init_conn(tabname=tabname)
        data = engine.sqlite_engine_auto_load_select()
        # ReflectedXSS(data)
        # OpenRedirect(data)
        # SQLInjection(data)
        # LocalFileInclusion(data)