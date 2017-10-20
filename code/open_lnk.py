# -*- encoding: utf-8 -*-
import xmlrpclib


class openerp_link(object):

    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user_name = user
        self.password = password
        self.open_link()
        print 'Conectado a: %s\%s' % (host, database)

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
            print u'Exception!'
            print err.faultCode        # the exception instance
            print err.faultString      # arguments stored in .args
            raise SystemExit(0)
        return res
