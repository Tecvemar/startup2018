# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_res_partner(lnk):
    c2o = csv_2_openerp(
        '../data/common/res_partner.csv',
        'res.partner', lnk)
    c2o.set_search_fields(['vat'])
    c2o.set_float_fields(['wh_iva_rate'])
    c2o.set_boolean_fields(['customer', 'supplier', 'islr_withholding_agent',
                            'spn', 'wh_iva_agent', 'group_wh_iva_doc', 'vat_subjected'])
    c2o.set_relational_fields([
                               ('account_kind_rec', 'res.partner.account', ['name']),
                               ('account_kind_pay', 'res.partner.account', ['name']),

                               ('property_account_receivable', 'account.account', ['parent_id']),

                               ('property_account_payable', 'account.account', ['parent_id']),
                               ('property_account_advance', 'account.account', ['parent_id']),
                               ('property_account_prepaid', 'account.account', ['parent_id']),

                               ])
    c2o.process_csv()




#~ "","","last_reconciliation_date",


"",
#~ "","","",
#~ "",""
