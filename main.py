import sys
sys.dont_write_bytecode = True
# sys.setrecursionlimit(1000000000)
from Search.attack import VulnFuzz
from tldextract import extract
from Crawler import URL
import argparse
import os

if __name__ == "__main__":
    # if os.path.exists('.\\db\\url.db'):
    #     os.remove('.\\db\\url.db')
    #     print(f'[{os.getcwd()}\\db\\url.db] : remove')
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='input URL', dest='url')
    
    args = parser.parse_args()
    url = (args.url)

    if url:
        domain = extract(url).domain
        Crawling = URL(url, **{})
        Crawling.Crawler()
        Crawling.closed()
        VulnFuzz(domain, **{})