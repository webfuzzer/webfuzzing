from pymysql import connect, cursors

class DATABASE:
    def __init__(self, host, port, user, passwd, db) -> None:

        self.host = host or 'localhost'
        self.port = port or 3306
        self.user = user or 'root'
        self.passwd = passwd or None
        self.db = db or None

        self.conn = connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db, cursorclass=cursors.DictCursor)

    def URL_SELECT(self, QUERY) -> (dict or tuple):
        cursor = self.conn.cursor()
        cursor.execute(query=QUERY) \
            if QUERY else \
                cursor.execute(query="SELECT * FROM URL")
        return cursor.fetchall()

    def URL_INSERT(self, QUERY) -> (dict or tuple):
        try:
            assert QUERY

            cursor = self.conn.cursor()
            cursor.execute(query=QUERY)
            self.conn.commit()

            return True
        except:
            return False