# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_stock_warehouse(lnk):
    work_dir = '../data/companies/%s/' % lnk.database
    c2o = csv_2_openerp(
        work_dir + 'stock_warehouse.csv', 'stock.warehouse', lnk)
    c2o.set_search_fields(['id'])
    c2o.set_integer_fields(['id'])
    c2o.update_records = True
    c2o.process_csv()
