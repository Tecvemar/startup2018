# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_stock_location(lnk):

    c2o = csv_2_openerp(
        '../data/common/stock_location.csv', 'stock.location', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_boolean_fields(['active'])
    c2o.update_records = True
    c2o.process_csv()
    #~ c2o.test_data_file()

