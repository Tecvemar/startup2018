# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_l10n_ut(lnk):

    c2o = csv_2_openerp(
        '../data/common/l10n_ut.csv', 'l10n.ut', lnk)
    c2o.set_search_fields(['date'])
    c2o.set_float_fields(['amount'])
    c2o.process_csv()
