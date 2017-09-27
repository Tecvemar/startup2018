# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_product_product(lnk):

    c2o = csv_2_openerp(
        '../data/common/product_product.csv',
        'product.product', lnk)
    c2o.set_search_fields(['default_code'])
    c2o.set_integer_fields(['thickness', 'hardness'])
    c2o.set_boolean_fields(['sale_ok', 'purchase_ok', 'track_production',
                            'track_incoming', 'track_outgoing'])
    c2o.set_float_fields(['uos_coeff'])
    c2o.set_relational_fields([
        ('categ_id', 'product.category', ['code']),
        ('uom_id', 'product.uom', ['name']),
        ('uom_po_id', 'product.uom', ['name']),
        ('uos_id', 'product.uom', ['name']),
        ('layout_id', 'product.product.features', ['name']),
        ('material_id', 'product.product.features', ['name']),
        ('finish_id', 'product.product.features', ['name']),
        ('quality_id', 'product.product.features', ['name']),
        ('tile_format_id', 'product.product.tile.format', ['name']),
        ('origin_country_id', 'res.country', ['name']),
        ('concept_id', 'islr.wh.concept', ['name'])
        ])
    c2o.process_csv()
