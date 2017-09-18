# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_res_partnert(lnk):
    c2o = csv_2_openerp(
        '../data/common/res_partner.csv',
        'res.partner', lnk)
    c2o.set_search_fields(['name'])
    #~ c2o.set_integer_fields(['title'])
    c2o.set_boolean_fields(['active', 'customer', 'supplier',
                            'islr_withholding_agent', 'spn' ,
                            'wh_iva_rent' , 'group_wh_iva_doc'])
    c2o.process_csv()


