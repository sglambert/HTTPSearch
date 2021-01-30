import psycopg2
import configuration as config
from logger import log
import pyodbc
import textwrap
import traceback

#TODO Add logging
class Database(object):


    def __init__(self):
        self.user = config.db_user
        self.password = config.db_password
        self.conn = None
        self.cursor = None


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, tb):
        if self.cursor is not None:
            if exc_type is not None:
                self.rollback()
                traceback.print_exception(exc_type, exc_value, tb)
            else:
                self.commit()
        self.close()


    def connect(self):
        self.conn = psycopg2.connect(user=config.db_user,
                                     password=config.db_password,
                                     host=config.db_host,
                                     port=config.db_port,
                                     database=config.db_database)
        log.info('Connected to %s database with user %s' % (config.db_database, config.db_user))
        print(self.conn.encoding)
        self.cursor = self.conn.cursor()
        return self


    def close(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            log.info("Disconnected from %s database" % config.db_database)


    def execute(self, sql, parameters=None):
        self.cursor.execute(sql, parameters)


    def executemany(self, sql, parameters=None):
        assert self.cursor is not None
        self.cursor.executemany(sql, parameters)


    def commit(self):
        assert self.cursor is not None
        self.conn.commit()
        log.debug("COMMIT")


    def rollback(self):
        assert self.cursor is not None
        self.conn.rollback()
        log.debug("ROLLBACK")

    def select_all(self, sql, parameters=None):
        self.execute(sql, parameters)
        log.debug(sql)
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
