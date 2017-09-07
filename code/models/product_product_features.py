# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_product_product_features(lnk):
    c2o = csv_2_openerp(
        '../data/common/product_product_features.csv',
        'product.product.features', lnk)
    c2o.set_search_fields(['name', 'type'])
    c2o.process_csv()

