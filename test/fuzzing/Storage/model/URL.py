from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

def CreateModel(table):
    class URLGroup(base):
        __table__ = table

        def __repr__(self) -> str:
            return f"<{self.__tablename__}('{self.first_url}', '{self.current_url}', '{self.method}', '{self.history_len}', '{self.body}')>"

    return URLGroup
