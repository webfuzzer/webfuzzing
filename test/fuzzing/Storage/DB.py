from sqlalchemy import create_engine, Table, Column, Integer, String, JSON, select
from sqlalchemy.orm import sessionmaker as SessionMaker
from .model.URL import CreateModel, base

class Engine():
    def __init__(self, sess=True) -> None:
        self.init_db()
        if sess:
            self.init_sess()

    def add(self, **data):
        INFO = self.URLGroup(
                **data
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
            Column('history', String),
            Column('history_len', Integer),
            Column('response_url', String),
            Column('response_cookies', JSON),
            Column('response_headers', JSON),
            Column('response_status', String),
            Column('body', String),
        )
        base.metadata.create_all(self.engine)
        self.URLGroup = CreateModel(self.Table)

    def init_db(self):
        self.engine = create_engine('sqlite:///db/url.db', echo=True)
    
    def init_sess(self):
        self._sess = SessionMaker(bind=self.engine)
        self.sess = self._sess()

    def init_conn(self):
        self.conn = self.engine.connect()

    def sqlite_engine_auto_load_select(self, tabname, column='*'):

        URLGroup = Table(tabname, base.metadata, autoload=True, autoload_with=self.engine)

        if column == '*':
            columns = [URLGroup]
        else:
            try:
                columns = [getattr(URLGroup.columns, select_column) for select_column in column]
                print(columns)
            except AttributeError:
                return
        sqlite_select_query = select(columns)
        result = self.conn.execute(sqlite_select_query)
        return result.fetchall()

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