# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp
import sys


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
        ('origin_country_id', 'res.country', ['code']),
        ('concept_id', 'islr.wh.concept', ['name'])
        ])
    c2o.process_csv()


def postprocess_product_product(dbref, dbdes):
    msg = 'Postprocesando: product.product.'
    properties = [
        ('account', 'property_account_income'),
        ('account', 'property_account_allowance'),
        ('account', 'property_stock_account_input'),
        ('account', 'property_stock_account_output'),
        ('account', 'property_account_return'),
        ('stock', 'property_stock_procurement'),
        ('stock', 'property_stock_production'),
        ('stock', 'property_stock_inventory'),
        ('account', 'property_account_creditor_price_difference'),
        ('account', 'property_account_expense'),
        ('wh_islr', 'concept_id'),
        ('taxes', 'supplier_taxes_id'),
        ('taxes', 'taxes_id'),
        ]
    product_ids = dbref.execute(
        'product.product', 'search', [])
    products = dbref.execute(
        'product.product', 'read', product_ids, [])
    for prd in products:
        sys.stdout.flush()
        base_prd_id = dbdes.execute(
            'product.product', 'search', [
                ('default_code', '=', prd['default_code'])])
        base_prds = dbdes.execute(
            'product.product', 'read', base_prd_id, [])
        for base_prd in base_prds:
            print msg + ' ' + base_prd['code'] + '\r',
            sys.stdout.flush()
            #~ data = {'default_code': base_prd['default_code']}
            data = {}
            for prop in properties:
                fld_type = prop[0]
                fld_name = prop[1]
                fld_value = base_prd[fld_name]
                if fld_type == 'account' and fld_value:
                    value = dbdes.execute(
                        'account.account', 'read', fld_value[0], ['code'])
                    ref_val_id = dbref.execute(
                        'account.account', 'search',
                        [('code', '=', value['code']),
                         ('company_id', '=', 1)])
                    if ref_val_id and len(ref_val_id) == 1:
                        data.update({fld_name: ref_val_id[0]})
                elif fld_type == 'stock' and fld_value:
                    value = dbdes.execute(
                        'stock.location', 'read', fld_value[0], ['name'])
                    ref_val_id = dbref.execute(
                        'stock.location', 'search',
                        [('name', '=', value['name'])])
                    if ref_val_id and len(ref_val_id) == 1:
                        data.update({fld_name: ref_val_id[0]})
                elif fld_type == 'wh_islr' and fld_value and  \
                        fld_value[1] != 'NO APLICA RETENCION':
                    value = fld_value[1]
                    ref_val_id = dbref.execute(
                        'islr.wh.concept', 'search',
                        [('name', '=', value)])
                    if ref_val_id and len(ref_val_id) == 1:
                        data.update({fld_name: ref_val_id[0]})
                elif fld_type == 'taxes' and fld_value:
                    value = dbdes.execute(
                        'account.tax', 'read', fld_value[0], ['name'])
                    ref_val_id = dbref.execute(
                        'account.tax', 'search',
                        [('name', '=', value['name'])])
                    if ref_val_id and len(ref_val_id) == 1:
                        data.update({fld_name: [(4, ref_val_id[0])]})
            if data:
                dbref.execute(
                    'product.product', 'write', prd['id'], data)
    print msg + ' Done.' + ' ' * 20
