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

from sqlalchemy import create_engine, Table, Column, JSON, Integer
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
    print(i.__dict__)
"""
from Storage.DB import Engine

engine = Engine(sess = False)
engine.init_conn()
print(engine.sqlite_engine_auto_load_select(tabname = 'me2nuk', column=['current_url']))"""
"""from Storage.DB import Engine

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