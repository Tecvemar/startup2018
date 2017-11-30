# -*- encoding: utf-8 -*-
#~ import sys
from csv2open import csv_2_openerp


def load_islr_wh_concept(dbcomp):
    c2o = csv_2_openerp(
        '../data/common/islr_wh_concept.csv', 'islr.wh.concept', dbcomp)
    c2o.set_search_fields(['name'])
    c2o.update_records = True
    c2o.set_relational_fields([
        ('property_retencion_islr_payable', 'account.account', ['code']),
        ('property_retencion_islr_receivable', 'account.account', ['code']),
        ])
    c2o.process_csv()
