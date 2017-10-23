# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_res_partner_account(lnk):

    c2o = csv_2_openerp(
        '../data/common/res_partner_account.csv',
        'res.partner.account', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_boolean_fields(['use_adbance'])
    c2o.set_integer_fields(['company_id'])
    c2o.set_relational_fields([
        ('property_account_partner', 'account.account', ['code']),
        ('property_account_partner_default', 'account.account', ['code']),
        ('property_parent_advance', 'account.account', ['code']),
        ('property_account_advance_default', 'account.account', ['code']),
        ('user_type', 'account.account.type', ['name']),
        ('user_type_advance', 'account.account.type', ['name']),
        ])
    c2o.process_csv()
    #~ c2o.test_data_file()
