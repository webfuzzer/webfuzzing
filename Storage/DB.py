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
            Column('request_cookies', JSON),
            Column('request_headers', JSON),
            Column('data', JSON),
            Column('body', String),
        )
        base.metadata.create_all(self.engine)
        self.URLGroup = CreateModel(self.Table)

    def init_db(self):
        self.engine = create_engine('sqlite:///db/url.db') # echo=True)
    
    def init_sess(self):
        self._sess = SessionMaker(bind=self.engine)
        self.sess = self._sess()

    def init_conn(self, tabname):
        self.conn = self.engine.connect()
        self.URLGroup = Table(tabname, base.metadata, autoload=True, autoload_with=self.engine)
        self.row_to_dict = (lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns})

    def sqlite_engine_auto_load_select(self, column='*'):

        if column == '*':
            columns = [self.URLGroup]
        else:
            try:
                columns = [getattr(self.URLGroup.columns, select_column) for select_column in column]
            except AttributeError:
                return
        sqlite_select_query = select(columns)
        result = self.conn.execute(sqlite_select_query)
        a = result.fetchall()
        return a

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