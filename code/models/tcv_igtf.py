# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_tcv_igtf(lnk):

    c2o = csv_2_openerp(
        '../data/common/tcv_igtf.csv', 'tcv.igtf', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_integer_fields(['company_id'])
    c2o.set_boolean_fields(['active', ])
    c2o.set_float_fields(['rate'])
    c2o.set_relational_fields(
        [('account_id', 'account.account', ['code']),
         ])
    c2o.process_csv()
