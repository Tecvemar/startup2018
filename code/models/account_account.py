# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_account_account(lnk):
    c2o = csv_2_openerp(
        '../data/common/account_account.csv', 'account.account', lnk)
    c2o.set_search_fields(['code'])
    c2o.set_boolean_fields(['user_type', 'active', 'reconcile'])
    c2o.set_relational_fields([('parent_id', 'account.account', ['code'])])
    c2o.process_csv()
