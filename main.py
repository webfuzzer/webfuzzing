import sys
sys.dont_write_bytecode = True

from Crawler import URL
from Search.attack import VulnFuzz
from tldextract import extract
from timeit import default_timer as dt
import os

if __name__ == "__main__":
    if os.path.exists('.\\db\\url.db'):
            os.remove('.\\db\\url.db')
            print(f'[{os.getcwd()}\\db\\url.db] : remove')
    urls = [
        "http://18.179.206.187/"
    ]

    info = {}

    for url in urls:
        domain = extract(url).domain
        Crawling = URL(url, **info)
        Crawling.Crawler()
        Crawling.closed()
        VulnFuzz(domain, **info)