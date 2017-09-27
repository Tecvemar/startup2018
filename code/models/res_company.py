# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def update_res_company(lnk):

    c2o = csv_2_openerp(
        '../data/common/res_company.csv', 'res.company', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_integer_fields(['lines_invoice'])
    c2o.set_relational_fields([('currency_id', 'res.currency', ['name'])])
    c2o.update_records = True
    c2o.process_csv()
