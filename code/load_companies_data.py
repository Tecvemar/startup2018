# -*- encoding: utf-8 -*-
from open_lnk import openerp_link
from definitions import dbdata
import companies
#~
for database in dbdata['databases']:
#~ for database in []:
#~ for database in ['barcelona', 'guayana']:


    lnk_dbcom = openerp_link(
        dbdata['host'],
        dbdata['rpc_port'],
        database,
        dbdata['openerp_login'],
        dbdata['openerp_password'])

    print 'Cargando datos de compañias: %s...' % database

    #~ companies.load_stock_production_lot(lnk_dbcom)
    companies.load_res_company(lnk_dbcom)
    companies.load_stock_warehouse(lnk_dbcom)
    companies.load_sale_shop(lnk_dbcom)






