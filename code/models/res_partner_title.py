# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_res_partner_title(lnk):
    c2o = csv_2_openerp(
        '../data/common/res_partner_title.csv',
        'res.partner.title', lnk)
    c2o.set_search_fields(['name', 'domain'])
    c2o.process_csv()


