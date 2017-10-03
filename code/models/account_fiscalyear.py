# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_account_fiscalyear(lnk):

    c2o = csv_2_openerp(
        '../data/common/account_fiscalyear.csv', 'account.fiscalyear', lnk)
    c2o.set_search_fields(['name'])
    c2o.process_csv()
