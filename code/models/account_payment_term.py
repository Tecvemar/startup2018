# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_account_payment_term(lnk):
    #~ payment term table
    c2o = csv_2_openerp(
        '../data/common/account_payment_term.csv', 'account.payment.term', lnk)
    c2o.set_search_fields(['name'])
    c2o.process_csv()
