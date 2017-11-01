# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_tcv_to_dispatch_config(lnk):

    c2o = csv_2_openerp(
        '../data/common/tcv_to_dispatch_config.csv',
        'tcv.to.dispatch.config', lnk)
    c2o.set_search_fields(['date_from'])
    c2o.set_integer_fields(['driver_id', 'vehicle_id'])
    c2o.set_relational_fields([
        ('stock_journal_id', 'stock.journal', ['name']),
        ('location_id', 'stock.location', ['name']),
        ('location_dest_id', 'stock.location', ['name']),
        ])
    c2o.process_csv()
