# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_tcv_import_config(lnk):

    c2o = csv_2_openerp(
        '../data/common/tcv_import_config.csv', 'tcv.import.config', lnk)
    c2o.set_search_fields(['company_id'])
    c2o.set_integer_fields(['company_id'])
    c2o.set_relational_fields([
        ('journal_id', 'account.journal', ['name']),
        ('account_id', 'account.account', ['code']),
        ])
    c2o.update_records = True
    c2o.process_csv()
