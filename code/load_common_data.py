# -*- encoding: utf-8 -*-
from open_lnk import openerp_link
from definitions import dbdata
import res_users

lnk_dbgen = openerp_link(
    dbdata['host'],
    dbdata['rpc_port'],
    dbdata['dbgen'],
    dbdata['openerp_login'],
    dbdata['openerp_password'])

res_users.common_res_users(lnk_dbgen)


print 'Cargando datos comunes...'

