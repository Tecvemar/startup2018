# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_res_partner(lnk):

    c2o = csv_2_openerp(
        '../data/common/res_partner.csv',
        'res.partner', lnk)
    c2o.set_search_fields(['vat'])
    c2o.set_float_fields(['wh_iva_rate'])
    c2o.set_boolean_fields(['customer', 'supplier', 'islr_withholding_agent',
                            'spn', 'wh_iva_agent',
                            'group_wh_iva_doc', 'vat_subjected'])
    c2o.set_relational_fields([
        ('property_account_receivable', 'account.account', ['code']),
        ('property_account_payable', 'account.account', ['code']),
        ('property_account_advance', 'account.account', ['code']),
        ('property_account_prepaid', 'account.account', ['code']),
        ('property_stock_customer', 'stock.location', ['name']),
        ('property_stock_supplier', 'stock.location', ['name']),
        ('property_stock_supplier', 'stock.location', ['name']),
        ])
    c2o.set_child_model_fields(['address'])
    c2o.test_data_file()
    #~ c2o.process_csv()
