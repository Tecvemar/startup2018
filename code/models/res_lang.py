# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def update_res_lang(lnk):
    #~ Lang settings
    c2o = csv_2_openerp(
        '../data/common/res_lang.csv', 'res.lang', lnk)
    c2o.set_search_fields(['code'])
    c2o.set_boolean_fields(['active', 'translatable'])
    c2o.update_records = True
    c2o.process_csv()
