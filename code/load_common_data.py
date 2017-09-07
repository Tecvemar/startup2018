# -*- encoding: utf-8 -*-
from open_lnk import openerp_link
from definitions import dbdata
import models

lnk_dbgen = openerp_link(
    dbdata['host'],
    dbdata['rpc_port'],
    dbdata['dbgen'],
    dbdata['openerp_login'],
    dbdata['openerp_password'])

models.common_res_users(lnk_dbgen)
models.common_res_country_state(lnk_dbgen)


print 'Cargando datos comunes...'

