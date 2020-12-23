import psycopg2
import configuration as config
import textwrap

#TODO Add logging
class Database(object):


    def __init__(self):
        self.user = config.db_user
        self.password = config.db_password
        self.conn = None
        self.cursor = None


    def __enter__(self):
        return self


    def __exit__(self, exc_type):
        if self.cursor is not None:
            if exc_type:
                self.rollback()
            else:
                self.commit()
        self.close()


    def connect(self):
        self.conn = psycopg2.connect(user=config.db_user,
                                     password=config.db_password,
                                     host=config.db_host,
                                     port=config.db_port,
                                     database=config.db_database)
        print("PostgreSQL server information")
        print(self.conn.get_dsn_parameters(), "\n")
        self.cursor = self.conn.cursor()
        return self


    def close(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.conn is not None:
            self.conn.close()
            self.conn = None


    def execute(self, sql):
        self.cursor.execute(sql)


    def executemany(self, sql):
        assert self.cursor is not None
        self.cursor.executemany(sql)


    def commit(self):
        assert self.cursor is not None
        self.conn.commit()


    def rollback(self):
        assert self.cursor is not None
        self.conn.rollback()


    def select_all(self, sql):
        self.execute(sql)
        return self.cursor.fetchall()


    def select_one(self, sql):
        self.execute(sql)
        assert self.cursor.rowcount <= 1
        return self.cursor.fetchone()


    def select_array(self, sql):
        rows = self.select_all(sql)
        return [r[0] for r in rows]


    def select_single_value(self, sql):
        row = self.select_one(sql)
        if row:
            assert len(row) == 1
        return row and row[0]


    def select_yield(self, sql):
        with self.conn.cursor(True) as dynamic_cursor:
            self.execute(sql, dynamic_cursor)
            while True:
                rows = dynamic_cursor.fetchmany(1000)
                if not rows:
                    break
                for row in rows:
                    yield row


# Simple test case of database connection and retrieving data from a table
database = Database()
connection = database.connect()
sql = textwrap.dedent("SELECT * FROM public.test")
print(connection.select_all(sql))
