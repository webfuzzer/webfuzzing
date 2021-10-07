from Crawler import *
from payload import *

class fuzz:
    def __init__(self) -> None:
        pass

C = Crawler('http://localhost/wordpress', Page=True)
C()