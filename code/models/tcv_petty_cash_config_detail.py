# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_tcv_petty_cash_config_detail(lnk):
    '''
    Create petit cash data
    '''
    c2o = csv_2_openerp(
        '../data/common/tcv_petty_cash_config_detail.csv',
        'tcv.petty.cash.config.detail', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_float_fields(['amount', 'max_amount'])
    c2o.set_relational_fields([
        ('acc_petty_cash_refund', 'account.account', ['code']),
        ('journal_id', 'account.journal', ['name']),
        ('currency_id', 'res.currency', ['name']),
        ('user_id', 'res.users', ['login']),
        ])
    c2o.process_csv()
