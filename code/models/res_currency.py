# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def update_res_currency(lnk):
    #~ disable unused currencies
    c2o = csv_2_openerp(
        '../data/common/res_currency_1.csv', 'res.currency', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_boolean_fields(['active', 'base'])
    c2o.update_records = True
    c2o.process_csv()

    #~ set rounding factor to VEB
    c2o = csv_2_openerp(
        '../data/common/res_currency_2.csv', 'res.currency', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_float_fields(['rounding'])
    c2o.update_records = True
    c2o.process_csv()

    #~ set rate to 1.0
    c2o = csv_2_openerp(
        '../data/common/res_currency_rate.csv', 'res.currency.rate', lnk)
    c2o.set_search_fields(['currency_id'])
    c2o.set_relational_fields([('currency_id', 'res.currency', ['name'])])
    c2o.set_float_fields(['rate', 'inv_rate'])
    c2o.update_records = True
    c2o.process_csv()

    #~ set base currency to VEB
    c2o = csv_2_openerp(
        '../data/common/res_currency_3.csv', 'res.currency', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_boolean_fields(['base'])
    c2o.update_records = True
    c2o.process_csv()
