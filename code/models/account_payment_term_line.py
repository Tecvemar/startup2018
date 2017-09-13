# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_account_payment_term_line(lnk):
    #~ payment term table line
    c2o = csv_2_openerp(
        '../data/common/account_payment_term_line.csv',
        'account.payment.term.line', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_integer_fields(['value_amount', 'sequence', 'days2', 'days'])
    c2o.set_relational_fields([('payment_id', 'account.payment.term', ['name']
                                )])
    c2o.process_csv()
