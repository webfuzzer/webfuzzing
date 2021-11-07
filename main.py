from Crawler import URL
from Search.attack import VulnFuzz
from tldextract import extract
from timeit import default_timer as dt
import os

if __name__ == "__main__":
    # url = "https://www.stealien.com/"
    url = "http://18.179.206.187/"
    domain = extract(url).domain
    if os.path.exists('.\\db\\test.db'):
        os.remove('.\\db\\test.db')
        print(f'[{os.getcwd()}\\db\\test.db] : remove')
    Crawling = URL(url)
    Crawling.Crawler()
    Crawling.closed()
    VulnFuzz(domain, url)