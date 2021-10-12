from pymysql import connect, cursors

class DATABASE:
    def __init__(self, host, port, user, passwd, db) -> None:

        self.host = host or 'localhost'
        self.port = port or 3306
        self.user = user or 'root'
        self.passwd = passwd or None
        self.db = db or None

        self.conn = connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db, cursorclass=cursors.DictCursor)

    def URL_SELECT(self, TABLE_NAME, QUERY = None) -> (dict or tuple):
        cursor = self.conn.cursor()
        cursor.execute(query=QUERY) \
            if QUERY else \
                cursor.execute(query=f"SELECT * FROM `{TABLE_NAME}`")
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

    def DOMAIN_TABLE_CHECK(self, domain) -> str:
        try:
            assert domain

            cursor = self.conn.cursor()
            cursor.execute(f'SELECT table_name FROM information_schema.tables WHERE table_schema="fuzzing" and table_name="{domain}"')
            return cursor.fetchone()
        except:
            pass

    def DOMAIN_CREATE_TABLE(self, domain) -> str:
        try:
            assert domain

            cursor = self.conn.cursor()
            cursor.execute(query=f'CREATE TABLE `{domain}`(first_url varchar(2048) NOT NULL, last_url varchar(2048) NOT NULL, empty_url varchar(2048) NOT NULL, body longtext)')
            self.conn.commit()
        except:
            return False

    def CREATE_DATABASE(self, db='fuzzing') -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(query=f'CREATE DATABASE `{db}`')
            self.conn.commit()
            return True
        except:
            return False