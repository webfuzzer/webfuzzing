import sys
sys.dont_write_bytecode = True
# sys.setrecursionlimit(1000000000)

from Search.attack import VulnFuzz
from tldextract import extract
from Crawler import URL
import argparse

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='input URL', dest='url')
    parser.add_argument('-d', '--domain', help='input domain', dest='domain', default=False)
    
    args = parser.parse_args()
    url = args.url

    if url:
        domain = extract(url).domain
        Crawling = URL(url, **{})
        Crawling.Crawler()
        Crawling.closed()
        print('vuln exploit!')
        VulnFuzz(domain, **{})