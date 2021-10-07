tags = {
    # HTML href attribute
    'href':[
            'a', 
            'link', 
            'area', 
            'base',
        ],
    # HTML src attribute
    'src':[
            'img', 
            'script', 
            'iframe', 
            'embed', 
            'audio', 
            'input', 
            'script', 
            'source', 
            'track', 
            'video',
        ],
    # HTML action attribute
    'action':[
            'form',
        ],
    # HTML data attribute
    'data':[
            'object',
        ],
}

# https://developers.whatismybrowser.com/useragents/explore/software_type_specific/crawler/
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}
TIMEOUT = 3

# selenium bot ChromeOptions
SELENIUM_CONFIG =['window-size=1920x1080', 'disable-gpu', 'no-sandbox', 'disable-dev-shm-usage', '--log-level=3']

# webdriver Path
NT_PATH = '\\src\\Crawler\\webdriver\\chromedriver.exe'
POSIX_PATH = '/src/Crawler/webdriver/chromedriver'

HOST = 'localhost'
PORT = 3306
USER = 'root'
PASSWORD = 'autoset'
DB = 'fuzzing'