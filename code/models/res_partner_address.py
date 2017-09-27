# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_res_partner_address(lnk):

    c2o = csv_2_openerp(
        '../data/common/res_partner_address.csv',
        'res.partner.address', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_integer_fields(['partner_id', 'country_id', 'company_id', ])
    c2o.set_boolean_fields(['active'])
    c2o.process_csv()
