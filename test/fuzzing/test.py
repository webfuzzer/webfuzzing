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

from sqlalchemy import create_engine, Table, select, MetaData
from base64 import b64decode

engine = create_engine('sqlite:///db/url.db', echo=True)
conn = engine.connect()
Meta = MetaData()
url = Table('me2nuk', Meta, autoload=True, autoload_with=engine)
query = select([url.columns.current_url])
execute = conn.execute(query)
print(execute.fetchall())