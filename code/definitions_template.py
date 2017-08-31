# -*- encoding: utf-8 -*-

#~ Postgesql user and other private data
dbdata = {
    'dbgen': '',
    'host': 'localhost',
    'openerp': {
        'login': '',
        'password': '',
        },
    'postgresql': {
        'login': '',
        'password': '',
        },
    'config_file': '',
    'backup_file': '',
    'server_path': '',
    'addons_path': '',
    }

#~ To simply params use
dbdata.update({
    'openerp_login': dbdata['openerp']['login'],
    'openerp_password': dbdata['openerp']['password'],
    'postgresql_login': dbdata['postgresql']['login'],
    'postgresql_password': dbdata['postgresql']['password'],
    })

