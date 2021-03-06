# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_account_tax(lnk):

    c2o = csv_2_openerp(
        '../data/common/account_tax.csv', 'account.tax', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_float_fields([
        'amount', 'base_sign', 'ref_base_sign', 'tax_sign', 'ref_tax_sign'])
    c2o.set_boolean_fields(['active', 'ret'])
    c2o.set_integer_fields(['sequence'])
    c2o.set_relational_fields([
        ('wh_vat_collected_account_id', 'account.account', ['code']),
        ('account_collected_id', 'account.account', ['code']),
        ('account_paid_id', 'account.account', ['code']),
        ('wh_vat_paid_account_id', 'account.account', ['code']),
        ])
    c2o.process_csv()
