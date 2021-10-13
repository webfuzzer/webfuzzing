from .Crawler import *
from .payload import *

class fuzz:
    def __init__(self, CONFIG) -> None:

        if CONFIG['config']['db']['db']['isset']:
            print(CONFIG['config']['db']['db']['isset'])
            C = Crawler('http://localhost/', Page=True, db={'HOST':CONFIG['config']['db']['host'],'PORT':CONFIG['config']['db']['port'],'USER':CONFIG['config']['db']['user'],'PASSWORD':CONFIG['config']['db']['password'],'DB':(CONFIG['config']['db']['db']['name'] if CONFIG['config']['db']['db']['isset'] else 'fuzzing')})
            C()