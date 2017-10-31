# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_stock_inventory(lnk):

    c2o = csv_2_openerp(
        '../data/common/stock_inventory.csv', 'stock.inventory', lnk)
    c2o.set_search_fields(['name'])
    #~ c2o.set_integer_fields(['company_id'])
    c2o.update_records = True
    c2o.process_csv()
    #~ c2o.test_data_file()

