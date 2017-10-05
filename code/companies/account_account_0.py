# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_account_account_0(lnk):

    work_dir = '../data/companies/%s/' % lnk.database
    c2o = csv_2_openerp(
        work_dir + 'account_account_0.csv', 'account.account', lnk)
    c2o.set_search_fields(['code'])
    c2o.update_records = True
    c2o.process_csv()
