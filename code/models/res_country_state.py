# -*- encoding: utf-8 -*-
#~ import csv
from csv2open import csv_2_openerp


def load_res_country_state(lnk):
    c2o = csv_2_openerp(
        '../data/common/res_country_state.csv', 'res.country.state', lnk)
    c2o.set_search_fields(['name', 'country_id'])
    c2o.set_integer_fields(['country_id'])
    c2o.process_csv()
