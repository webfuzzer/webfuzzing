from Crawler import *
from payload import *

class fuzz:
    def __init__(self) -> None:
        C = Crawler('http://localhost/', Page=True)
        C()

fuzz()