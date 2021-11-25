from threading import Thread
from tldextract import extract
from Storage.DB import Engine
from base64 import b64decode
from Search.Vulndb import * 

class VulnFuzz:
    def __init__(self, tabname : str, **info : dict) -> None:
        self.engine : Engine = Engine()
        self.engine.init_conn(tabname)
        self.data : tuple = self.engine.fetch_all()
        self.post_data : tuple = self.engine.fetch_all_filter(method='POST')
        self.info : dict = info
        self.init_vulns()
        self.start()

    def start(self) -> None:

        VulnerabilityThreads = []

        for vuln in self.vulns:
            if vuln[1] == 'POST':
                t1 = Thread(target=vuln[0], kwargs={'datatable':self.post_data, **self.info})
            else:
                t1 = Thread(target=vuln[0], kwargs={'datatable':self.data, **self.info})
            t1.start()
            VulnerabilityThreads.append(t1)

        for t in VulnerabilityThreads:
            t.join()
        
        # r1 = Thread(target=ReflectedXSS, kwargs={'datatable':self.data,**self.info})
        # r2 = Thread(target=OpenRedirect, kwargs={'datatable':self.data,**self.info})
        # r3 = Thread(target=ServerSideTemplateInjection, kwargs={'datatable':data,**self.info})
        # r1.start()
        # r2.start()
        # r3.start()
        # r1.join()
        # r2.join()
        # r3.join()

        # Thread(target=SQLInjection, kwargs={'datatable':data,**info}).start()
        # Thread(target=CrossSiteRequestForgery, kwargs={'datatable':data,**info}).start()
        # Thread(target=NOSQLInjection, kwargs={'datatable':data,**info}).start()
        # Thread(target=OSCommandInjection, kwargs={'datatable':data,**info}).start()
        # Thread(target=LocalFileInclusion, kwargs={'datatable':data,**info}).start()
        # Thread(target=RemoteFileInclusion, kwargs={'datatable':data,**info}).start()

    def init_vulns(self) -> None:
        self.vulns = [
            (ReflectedXSS, 'ALL'),
            (OpenRedirect, 'ALL'),
            (ServerSideTemplateInjection, 'ALL'),
            # SQLInjection, 'ALL'),
            # CrossSiteRequestForgery, 'POST'),
            (NOSQLInjection, 'ALL'),
            # OSCommandInjection, 'ALL'),
            # (LocalFileInclusion, 'ALL'),
            # (RemoteFileInclusion, 'ALL')
        ]
        return