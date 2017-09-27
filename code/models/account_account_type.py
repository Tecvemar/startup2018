# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_account_account_type(lnk):

    c2o = csv_2_openerp(
        '../data/common/account_account_type.csv',
        'account.account.type', lnk)
    c2o.set_search_fields(['name', 'report_type'])
    c2o.process_csv()
