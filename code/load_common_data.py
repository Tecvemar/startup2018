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

print 'Cargando datos comunes...'

models.common_res_users(lnk_dbgen)
models.load_res_country_state(lnk_dbgen)
models.load_product_product_features(lnk_dbgen)



