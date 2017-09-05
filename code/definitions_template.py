# -*- encoding: utf-8 -*-

#~ Postgesql user and other private data
dbdata = {
    'dbgen': 'bdd_ref',
    'host': 'localhost',
    'rpc_port': 8069,
    'openerp': {
        'login': '',
        'password': '',
        },
    'postgresql': {
        'login': '',
        'password': '',
        },
    'config_file': '',
    'backup_file': '../data/common/dbgen.backup',
    'server_path': '~/instancias/produccion/server/bin/',
    'addons_path': '~/instancias/produccion/modulos/',
    'databases': ('barcelona',
                  'guayana',
                  'monagas',
                  'valencia',
                  'barquisimeto',
                  'falcon',
                  'orinoco')
    }

#~ To simply params use
dbdata.update({
    'openerp_login': dbdata['openerp']['login'],
    'openerp_password': dbdata['openerp']['password'],
    'postgresql_login': dbdata['postgresql']['login'],
    'postgresql_password': dbdata['postgresql']['password'],
    })

