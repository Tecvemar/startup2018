# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_res_partner(lnk):

    work_dir = '../data/%s/' % lnk.database
    c2o = csv_2_openerp(
        work_dir + 'res_partner.csv', 'res.partner', lnk)
    c2o.set_search_fields(['id'])
    c2o.set_float_fields(['wh_iva_rate', ])
    c2o.set_boolean_fields([
        'supplier', 'customer', 'vat_subjected',
        'islr_withholding_agent', 'wh_iva_agent', 'group_wh_iva_doc'])
    c2o.update_records = True
    c2o.set_relational_fields([
        ('property_account_receivable', 'account.account', ['code']),
        ('property_account_advance', 'account.account', ['code']),
        ('property_account_payable', 'account.account', ['code']),
        ('property_account_prepaid', 'account.account', ['code']),
        ])
    c2o.process_csv()
