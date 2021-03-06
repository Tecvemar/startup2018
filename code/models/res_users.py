# -*- encoding: utf-8 -*-
from definitions import dbdata
import csv
import time


def load_res_users(lnk):
    msg = '  Cargando: res.users.'
    admin_id = lnk.execute(
        'res.users', 'search', [('login', '=', dbdata['openerp_login'])])
    admin_id = admin_id and len(admin_id) == 1 and admin_id[0] or None
    groups_id_adm = lnk.execute(
        'res.groups', 'search', [])
    lnk.execute(
        'res.users', 'write', admin_id, {'view': 'extended',
                                         'menu_tips': False,
                                         'groups_id': [(6, 0, groups_id_adm)],
                                         'context_lang': 'en_US'})
    res_users = csv.DictReader(open('../data/common/res_users.csv'))
    for user in res_users:
        print msg + ' ' + user['login'] + ' ' * 40 + '\r',
        user.update({
            'view': 'extended',
            'menu_tips': False,
            'groups_id': [(6, 0, groups_id_adm)],
            'context_lang': 'es_VE'})
        user_id = lnk.execute(
            'res.users', 'search', [('login', '=', user['login'])])
        if not user_id:
            lnk.execute('res.users', 'create', user)
    time.sleep(1)
    print msg + ' Listo.' + ' ' * 40
