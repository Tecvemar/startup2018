# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_stock_journal(lnk):

    c2o = csv_2_openerp(
        '../data/common/stock_journal.csv', 'stock.journal', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_relational_fields([('user_id', 'res.users', ['name'])])
    c2o.process_csv()
