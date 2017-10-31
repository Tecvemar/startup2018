# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_ir_translation(lnk):

    work_dir = '../data/companies/%s/' % lnk.database
    c2o = csv_2_openerp(
        work_dir + 'ir_translation.csv', 'ir.translation', lnk)
    c2o.set_search_fields(['res_id','name'])
    c2o.set_integer_fields(['res_id'])
    c2o.update_records = True
    c2o.process_csv()
