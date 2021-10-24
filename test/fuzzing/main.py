from Crawler import URL
from Search.vuln import Vulndb
from tldextract import extract

if __name__ == "__main__":
    # Vulndb('me2nuk', 'https://me2nuk.com/')
    url = "http://localhost"
    domain = extract(url).domain
    Crawling = URL(url)
    Crawling.Crawler()
    Vulndb(domain, url)