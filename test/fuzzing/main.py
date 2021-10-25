from Crawler import URL
from Search.vuln import Vulndb
from tldextract import extract
import os

if __name__ == "__main__":
    url = "http://localhost"
    domain = extract(url).domain
    Crawling = URL(url)
    Crawling.Crawler()
    Vulndb(domain, url)