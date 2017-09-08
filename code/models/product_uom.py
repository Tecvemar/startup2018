# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_product_uom(lnk):
    c2o = csv_2_openerp(
        '../data/common/product_uom.csv', 'product.uom', lnk)
    c2o.set_search_fields(['name', 'category_id'])
    c2o.set_integer_fields(['category_id'])
    c2o.set_float_fields(['factor_inv', 'factor', 'rounding'])
    c2o.process_csv()
