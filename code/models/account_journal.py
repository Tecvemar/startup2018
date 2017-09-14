# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_account_journal(lnk):

    c2o = csv_2_openerp(
        '../data/common/account_journal.csv', 'account.journal', lnk)
    c2o.set_search_fields(['code'])
    c2o.set_boolean_fields(['allow_date', 'update_posted'])
    c2o.set_integer_fields(['user_id', 'company_id'])
    c2o.set_relational_fields([
        ('default_debit_account_id', 'account.account', ['code']),
        ('default_credit_account_id', 'account.account', ['code']),
        ('currency', 'res.currency', ['name']),
        ('view_id', 'account.journal.view', ['name']),
        ])
    c2o.process_csv()
