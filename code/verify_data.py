# -*- encoding: utf-8 -*-
from open_lnk import openerp_link
from profit_lnk import profit_link
from definitions import dbdata
import verify

'''
               verify that the data that comes from profit
               are the same as the data stored in openerp

    '''

#~ for database in ['monagas']:
for database in dbdata['databases'][:6]:
    if dbdata[database]['profit']:
        lnk_dbprofit = profit_link(
            dbdata[database]['profit']['host'],
            dbdata[database]['profit']['db'],
            dbdata['profit_login'],
            dbdata['profit_password'])
    else:
        lnk_dbprofit = False

    lnk_dbcom = openerp_link(
        dbdata['host'],
        dbdata['rpc_port'],
        database,
        dbdata['openerp_login'],
        dbdata['openerp_password'])

    print 'Verificano datos: %s...' % database

    verify.check_account_invoice_purchases(lnk_dbcom, lnk_dbprofit)
