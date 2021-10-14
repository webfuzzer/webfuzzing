from selenium.webdriver import Chrome, ChromeOptions
import os

drive = ChromeOptions()
options = ['window-size=1920x1080', 'disable-gpu', 'no-sandbox', 'disable-dev-shm-usage', '--log-level=3']
for _ in options:
    drive.add_argument(_)

driv = Chrome(os.getcwd() + '\\src\\Crawler\\webdriver\\chromedriver.exe', options=drive)
driv.implicitly_wait(5)
driv.set_page_load_timeout(5)
driv.get('http://localhost/')
driv.get('http://localhost/search.php?search=<script>alert("hello");</script>')
print(driv.page_source)
result = driv.switch_to.alert
print(result.text)
