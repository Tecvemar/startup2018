# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_ir_sequence(lnk):

    c2o = csv_2_openerp(
        '../data/common/ir_sequence.csv', 'ir.sequence', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_integer_fields(['padding'])
    c2o.update_records = True
    c2o.process_csv()
