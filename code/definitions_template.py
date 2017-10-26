# -*- encoding: utf-8 -*-

#~ Postgesql user and other private data
dbdata = {
    'dbgen': 'bdd_ref',
    'dbdesarrollo': 'desarrollo',
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
    'profit': {
        'login': '',
        'password': '',
        },
    'config_file': '/home/jmarquez/.openerp_serverrc',
    'backup_file': '../data/common/dbgen.backup',
    'server_path': '~/instancias/produccion/server/bin/',
    'addons_path': '~/instancias/produccion/modulos/',
    'databases': (
        'barcelona',
        'guayana',
        'monagas',
        'valencia',
        'barquisimeto',
        'falcon',
        'orinoco',
        ),
    'barcelona': {
        'profit': {
            'host': '192.168.0.21',
            'db': 'ACROPOLI',
            }
        },
    'guayana': {
        'profit': {
            'host': '192.168.0.21',
            'db': 'ACROGUAA',
            }
        },
    'monagas': {
        'profit': {
            'host': '192.168.0.21',
            'db': 'ACROMOA',
            }
        },
    'valencia': {
        'profit': {
            'host': '192.168.0.21',
            'db': 'DACRO_A',
            }
        },
    'barquisimeto': {
        'profit': {
            'host': '192.168.0.21',
            'db': 'ACBARQ_A',
            }
        },
    'falcon': {
        'profit': {
            'host': '192.168.0.21',
            'db': 'ACFALC_A',
            }
        },
    'orinoco': {
        'profit': {}
        },
        },
    }

#~ To simply params use
dbdata.update({
    'openerp_login': dbdata['openerp']['login'],
    'openerp_password': dbdata['openerp']['password'],
    'postgresql_login': dbdata['postgresql']['login'],
    'postgresql_password': dbdata['postgresql']['password'],
    'profit_login': dbdata['profit']['login'],
    'profit_password': dbdata['profit']['password'],
    })
