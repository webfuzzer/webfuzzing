from .Crawler import *
from .payload import *

class fuzz:
    def __init__(self, CONFIG) -> None:
        print(CONFIG)

        if CONFIG['config']:
            if CONFIG['config']['db'] or None:
               raise  Exception

        if CONFIG['config']['db']['db']['isset']:
            print(CONFIG['config']['db']['db']['isset'])
            C = Crawler('http://localhost/', Page=True, db={'HOST':CONFIG['config']['db']['host'],'PORT':CONFIG['config']['db']['host'],'USER':CONFIG['config']['db']['host'],'PASSWORD':CONFIG['config']['db']['host'],'DB':CONFIG['config']['db']['host']})
            C()