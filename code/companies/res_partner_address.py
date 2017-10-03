# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_res_partner_address(lnk):

    work_dir = '../data/%s/' % lnk.database
    c2o = csv_2_openerp(
        work_dir + 'res_partner_address.csv', 'res.partner.address', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_integer_fields(['partner_id', 'country_id', 'company_id', ])
    c2o.set_boolean_fields(['active'])
    c2o.set_relational_fields([
        ('country_id', 'res.country', ['code']),
        ('state_id', 'res.country.state', ['code']),
        ('partner_id', 'res.partner', ['id']),
        ])
    c2o.update_records = True
    c2o.process_csv()
