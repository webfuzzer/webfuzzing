from Crawler import URL
from Search.vuln import Vulndb
from tldextract import extract
from timeit import default_timer as dt
import os

if __name__ == "__main__":
    if os.path.exists('.\\db\\url.db'):
        os.remove('.\\db\\url.db')
        print(f'[{os.getcwd()}\\db\\url.db] : remove')
    url = "http://18.179.206.187"
    domain = extract(url).domain
    Crawling = URL(url)
    Crawling.Crawler()
    Vulndb(domain, url)