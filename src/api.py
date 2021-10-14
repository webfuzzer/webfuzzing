from .Crawler import *
from .payload import *

class fuzz:
    def __init__(self, CONFIG) -> None:

        if CONFIG['config']['db']['db']['isset']:
            db = {'HOST':CONFIG['config']['db']['host'],'PORT':CONFIG['config']['db']['port'],'USER':CONFIG['config']['db']['user'],'PASSWORD':CONFIG['config']['db']['password'],'DB':(CONFIG['config']['db']['db']['name'] if CONFIG['config']['db']['db']['isset'] else 'fuzzing')}
            callCONFIG = {
                'URL':'',
                'Page':False,
                'db':db
            }
            for dynamic_URL in CONFIG['dynamic']:
                callCONFIG['URL'] = dynamic_URL
                callCONFIG['Page'] = True
                C = Crawler(**callCONFIG)
                C()
                Fuzzing(**callCONFIG)