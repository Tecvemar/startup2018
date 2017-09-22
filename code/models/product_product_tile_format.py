# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_product_product_tile_format(lnk):

    c2o = csv_2_openerp(
        '../data/common/product_product_tile_format.csv',
        'product.product.tile.format', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_boolean_fields(['kit'])
    c2o.set_float_fields(['length', 'heigth'])
    c2o.process_csv()
