# from base64 import b64encode, b64decode
# from Crawler.DB import Engine

# group = {
#         'first_url':'https://www.google.com',
#         'current_url':'https://www.google.com/test',
#         'body':b64encode('<html></html>'.encode()).decode()
# }


# db = Engine()
# for i in range(1,10):
#     db.add(**group)
# for i in db.fetch():
#     print(i.first_url, i.current_url, b64decode(i.body).decode())

"""from sqlalchemy import create_engine, Table, select, MetaData
from base64 import b64decode

engine = create_engine('sqlite:///db/url.db', echo=True)
conn = engine.connect()
Meta = MetaData()
url = Table('me2nuk', Meta, autoload=True, autoload_with=engine)
test = [url.columns.current_url]
print(test)
query = select(test)
execute = conn.execute(query)
# print(execute.fetchall())"""

"""from sqlalchemy import create_engine, Table, Column, JSON, Integer
from sqlalchemy.orm import sessionmaker as SessionMaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///test.db", echo = True)
base = declarative_base()
db = Table(
    'test',
    base.metadata,
    Column('id', Integer, primary_key=True),
    Column('jsons', JSON),
)
base.metadata.create_all(engine)
a = SessionMaker(bind = engine)
sess = a()

class test(base):
    __table__ = db

    def __repr__(self) -> str:
        return f"<(jsons:{self.jsons})>"

group = test(jsons = {'test':'helloworld'})
sess.add(group)
sess.commit()

dicts = sess.query(test).all()
for i in dicts:
    print(i.__dict__)"""

# from Storage.DB import Engine

# engine = Engine(sess = False)
# engine.init_conn('stealien')
# print(engine.sqlite_engine_auto_load_select(column=['current_url']))

"""
from Storage.DB import Engine

engine = Engine(sess = False)
engine.init_conn()
print(engine.sqlite_engine_auto_load_select(tabname='me2nuk', column=['history']))"""
"""class a:
    def __init__(self):
        self.a = 'hello'

class exam(a):
    def __new__(self):
        return self.a

b = exam()
print(b)"""
"""
from re import L
from bs4 import BeautifulSoup

soup = BeautifulSoup('''<html>
<head>
</head>
<body>
<form method="POST">
<input name="name" type="text"/>
<input name="passsword" type="text"/>
<textarea name="contents">teasgdag</textarea>
</form></body>
</html>''', 'html.parser')
form_in_elements_data = {}
form_submit_elements = soup.find_all(name=['button', 'input', 'select', 'textarea'])
for SubmitElement in form_submit_elements:
    value = SubmitElement.attrs.get('value')
    form_in_elements_data.setdefault(SubmitElement.attrs.get('name'), (value if value else ''))

print(form_in_elements_data)"""
"""from timeit import default_timer as dt
from random import choice

d = dt()

def a():
    return choice([True,False])

def time():
    for i in range(1,10000):
        if a():
            pass
        else:
            continue

print(dt() - d)"""

# from random import choice
# from timeit import default_timer as dt
# from numpy.random import choice as ch
# a = dt()
# for i in range(1,1000000): choice([1,2,3])
# print(dt() - a)
# a = dt()
# for i in range(1,1000000): ch([1,2,3])
# print(dt()-a)
"""
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os

opt = ChromeOptions()
for _ in ['window-size=1920x1080', 'disable-gpu', 'no-sandbox', 'disable-dev-shm-usage', '--log-level=3']:
    opt.add_argument(_)
path = os.getcwd() + '\\chromedriver.exe'
print(path)

driver = Chrome(path)
driver.get('http://localhost')
driver.set_page_load_timeout(5)
driver.implicitly_wait(5)

f = open('xss_pay.txt', 'w+', encoding='UTF-8')
for xss_pay in pay.split('\n'):       
    print(xss_pay)      
    xss_pay = xss_pay.strip()                                        
    try:
        driver.get(f'data:text/html,{xss_pay}')
        warning = driver.switch_to.alert
        f.write(xss_pay + '\n')
        warning.accept()
        sleep(1)
    except:
        continue
driver.quit()"""

# f = open('xss_pay.txt', 'r', encoding='UTF-8').readlines()

"""f = open('payload/xss/simple_alert.txt', 'r', encoding='UTF-8').readlines()
test = []
for i in f:
    test.append(i.strip())

import json
f = open('xss.txt', 'w', encoding='UTF-8')
json.dump(test,f)"""

# import docker

# engine = docker.from_env()

# engine.containers.run('ubuntu:18.04', name='test', detach=True)
from Storage.DB import Engine

engine : Engine = Engine()
engine.init_conn('18.179.206.187')
data : tuple = engine.fetch_all_filter(method='POST')
print(data)