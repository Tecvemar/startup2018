# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_tcv_stock_changes_method(lnk):

    c2o = csv_2_openerp(
        '../data/common/tcv_stock_changes_method.csv',
        'tcv.stock.changes.method', lnk)
    c2o.set_search_fields(['name', 'type'])
    c2o.set_relational_fields([
        ('journal_id', 'account.journal', ['code']),
        ('stock_journal_id', 'stock.journal', ['name']),
        ('location_id', 'stock.location', ['name']),
        ])
    c2o.process_csv()
