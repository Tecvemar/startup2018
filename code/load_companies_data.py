# -*- encoding: utf-8 -*-
from open_lnk import openerp_link
from profit_lnk import profit_link
from definitions import dbdata
import companies


#~ for database in dbdata['databases']:
for database in ['guayana']:
    lnk_dbprofit = profit_link(
        dbdata[database]['profit']['host'],
        dbdata[database]['profit']['db'],
        dbdata['profit_login'],
        dbdata['profit_password'])

    lnk_dbcom = openerp_link(
        dbdata['host'],
        dbdata['rpc_port'],
        database,
        dbdata['openerp_login'],
        dbdata['openerp_password'])

    print 'Cargando datos de compañias: %s...' % database

    #~ companies.load_bank_account_journal(lnk_dbcom, lnk_dbprofit)
    companies.load_stock_production_lot(lnk_dbcom, lnk_dbprofit)
    companies.load_res_company(lnk_dbcom)
    companies.load_stock_warehouse(lnk_dbcom)
    companies.load_sale_shop(lnk_dbcom)