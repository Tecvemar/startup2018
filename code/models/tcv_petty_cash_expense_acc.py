# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_tcv_petty_cash_expense_acc(lnk):
    '''
    Create petit cash expenses
    '''
    c2o = csv_2_openerp(
        '../data/common/tcv_petty_cash_expense_acc.csv',
        'tcv.petty.cash.expense.acc', lnk)
    c2o.set_search_fields(['ref'])
    c2o.set_relational_fields([
        ('account_id', 'account.account', ['code']),
        ])
    c2o.process_csv()
