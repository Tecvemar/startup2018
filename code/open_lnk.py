# -*- encoding: utf-8 -*-
import xmlrpclib
import psycopg2
import psycopg2.extras


class openerp_link(object):

    def __init__(self, host, port, database, user, password,
                 postgresql_login=None, postgresql_password=None):
        self.host = host
        self.port = port
        self.database = database
        self.user_name = user
        self.password = password
        self.postgresql_login = postgresql_login
        self.postgresql_password = postgresql_password
        print 'Conectado a: %s\%s' % (host, database)
        self.open_link()

    def open_link(self):
        url = "http://%s:%s/xmlrpc/" % (self.host, self.port)
        self.common_proxy = xmlrpclib.ServerProxy(url + "common")
        self.object_proxy = xmlrpclib.ServerProxy(url + "object")
        self.uid = self.common_proxy.login(
            self.database, self.user_name, self.password)

    def execute(self, *args):
        res = False
        try:
            res = self.object_proxy.execute(
                self.database,
                self.uid,
                self.password, *args)
        except xmlrpclib.Fault as err:
            print u'\nException!'
            print err.faultCode        # the exception instance
            print err.faultString      # arguments stored in .args
            print args
            raise SystemExit(0)
        return res

    def execute_workflow(self, *args):
        '''
        args: ('model.name', 'workflow_signal', id)
        '''
        try:
            res = self.object_proxy.exec_workflow(
                self.database, self.uid, self.password, *args)
        except xmlrpclib.Fault as err:
            print u'Workflow exception!'
            print err.faultCode        # the exception instance
            print err.faultString      # arguments stored in .args
            raise SystemExit(0)
        return res

    def execute_sql(self, sql, params=None):
        '''
        usage:
        execute_sql(
            sql_string,
            params)
        '''
        if not self.postgresql_login or not self.postgresql_password:
            print u'Run execute_sql exception!'
            print u'    Undefined user or password for postgresql'
            raise SystemExit(0)
        #~ print 'Ejecutando SQL %s en: %s\%s' % (
            #~ sql.split(' ')[0], self.host, self.database)
        conn_string = "host=%s dbname=%s user=%s password=%s" % (
            self.host, self.database,
            self.postgresql_login, self.postgresql_password)
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if params:
            cursor.execute(sql % params)
        else:
            cursor.execute(sql)
        if 'select' in sql[:20].lower():
            ans1 = []
            for row in cursor.fetchall():
                ans1.append(dict(row))
            return ans1
        elif 'update' in sql.lower() or 'insert' in sql.lower():
            conn.commit()
        return True
