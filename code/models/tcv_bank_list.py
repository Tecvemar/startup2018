# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_tcv_bank_list(lnk):
    #~ list of  banks
    c2o = csv_2_openerp(
        '../data/common/tcv_bank_list.csv', 'tcv.bank.list', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_boolean_fields(['active'])
    c2o.process_csv()
