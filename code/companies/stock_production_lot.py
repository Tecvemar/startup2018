# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_stock_production_lot(lnk):
    work_dir = '../data/companies/%s/' % lnk.database
    c2o = csv_2_openerp(
        work_dir + 'stock_production_lot.csv', 'stock.production.lot', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_float_fields([
        'length', 'heigth', 'property_cost_price',])
    c2o.set_relational_fields([
        ('product_id', 'product.product', ['default_code']),
        ])
    c2o.process_csv()
