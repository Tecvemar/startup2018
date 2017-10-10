# -*- encoding: utf-8 -*-
import pymssql


class profit_link(object):

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user_name = user
        self.password = password
        self.open_link()
        self.sql = ''
        self.args = {}

    def open_link(self):
        print 'Conectando a mssql server (%s)...' % self.host
        self.conn_profit = pymssql.connect(
            host=self.host,
            user=self.user_name,
            password=self.password,
            database=self.database,
            as_dict=True)
        self.cur_profit = self.conn_profit.cursor()

    def set_sql_string(self, sql_string):
        self.sql = sql_string

    def set_sql_args(self, *args):
        self.args = args

    def execute_sql(self):
        res = False
        try:
            self.cur_profit.execute(self.sql, self.args)
            res = self.cur_profit.fetchall()
        except pymssql.Error as err:
            print u'Exception!'
            print err.args        # the exception instance
            raise SystemExit(0)
        return res
