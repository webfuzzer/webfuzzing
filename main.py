from Crawler import URL
from Search.attack import VulnFuzz
from tldextract import extract
from timeit import default_timer as dt
import os

if __name__ == "__main__":
    url = "https://www.stealien.com/"
    domain = extract(url).domain
    # if os.path.exists('.\\db\\url.db'):
    #     os.remove('.\\db\\url.db')
    #     print(f'[{os.getcwd()}\\db\\url.db] : remove')
    # Crawling = URL(url)
    # Crawling.Crawler()
    # Crawling.closed()
    VulnFuzz(domain, url)