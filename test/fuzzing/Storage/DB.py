from sqlalchemy import create_engine, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker as SessionMaker
from .model.URL import CreateModel, base

class Engine():
    def __init__(self) -> None:
        self.init_db()
        self.init_sess()

    def add(self, first_url, current_url, method, history_len, body):

        INFO = self.URLGroup(
                first_url = first_url,
                current_url = current_url,
                method = method,
                history_len = history_len,
                body = body,
        )

        self.sess.add(INFO)
        self.sess.commit()

    def fetch(self):
        return self.sess.query(self.Table).all()

    def init_table(self, tabname):

        self.Table = Table(
            tabname,
            base.metadata,
            Column('id', Integer, primary_key=True),
            Column('first_url', String),
            Column('current_url', String),
            Column('method', String(5)),
            Column('history_len', Integer),
            Column('body', String),
        )
        base.metadata.create_all(self.engine)
        self.URLGroup = CreateModel(self.Table)

    def init_db(self):
        self.engine = create_engine('sqlite:///db/url.db', echo=True)
    
    def init_sess(self):
        self._sess = SessionMaker(bind=self.engine)
        self.sess = self._sess()

    def __del__(self):
        self._sess.close_all()

"""
engine = Engine()
engine.init_table('url')
engine.add(
    first_url = 'https://www.google.com/',
    current_url = 'https://www.google.com/a/a',
    method = 'GET',
    body = '<html>html source code</html>',
)
print(engine.fetch())
"""
