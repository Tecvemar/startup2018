# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_res_partner_address(lnk):

    work_dir = '../data/companies/%s/' % lnk.database
    c2o = csv_2_openerp(
        work_dir + 'res_partner_address_1.csv', 'res.partner.address', lnk)
    c2o.set_search_fields(['id'])
    c2o.set_relational_fields([
        ('country_id', 'res.country', ['name']),
        ('state_id', 'res.country.state', ['name']),
        ])
    c2o.update_records = True
    c2o.process_csv()
