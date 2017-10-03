# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_res_company(lnk):
    work_dir = '../data/companies/%s/' % lnk.database
    c2o = csv_2_openerp(
        work_dir + 'res_company.csv', 'res.company', lnk)
    c2o.set_search_fields(['id'])
    c2o.update_records = True
    c2o.process_csv()
