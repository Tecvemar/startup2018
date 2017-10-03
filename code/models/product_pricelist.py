# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_product_pricelist(lnk):

    c2o = csv_2_openerp(
        '../data/common/product_pricelist.csv',
        'product.pricelist', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_relational_fields([
        ('currency_id', 'res.currency', ['name'])
        ])
    c2o.update_records = True

    c2o.process_csv()
