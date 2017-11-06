# -*- encoding: utf-8 -*-
import os
from csv2open import csv_2_openerp
from profit2open import profit_2_openerp


def load_tcv_stock_changes(dbcomp, dbprofit):
    '''
    Profit's adjustements migration
    Need a csv list manually created with "To migrate adjusts"
    '''
    work_dir = '../data/companies/%s/' % dbcomp.database
    work_csv = work_dir + 'tcv_stock_changes.csv'
    if not os.path.isfile(work_csv):
        return
    c2o = csv_2_openerp(work_csv, 'tcv.stock.changes', dbcomp)
    c2o.set_search_fields(['name'])
    c2o.set_relational_fields([
        ('method_id', 'tcv.stock.changes.method', ['name']),
        ])
    c2o.process_csv()
    load_tcv_stock_changes_lines(dbcomp, dbprofit)


def load_tcv_stock_changes_lines(dbcomp, dbprofit):
    '''
    Profit's adjustements migration (lines)
    '''
    adjust_ids = dbcomp.execute('tcv.stock.changes', 'search', [])
    adjusts = sorted(
        dbcomp.execute('tcv.stock.changes', 'read', adjust_ids, [],),
        key=lambda k: k['name'])
    p2o = profit_2_openerp('stock.inventory.line', dbcomp, dbprofit)
    for adj in adjusts:
        if adj['state'] == 'draft' and not adj['line_ids']:
            p2o.set_sql(
                '''
                select ajue_num as line_id, rtrim(nro_lote) as prod_lot_id,
                rtrim(co_art) as product_id, aux02, 1 as pieces,
                'm2' as product_uom
                from reng_aju where ajue_num=%s
                ''' % adj['name'])
            p2o.set_aux02_fields(['heigth', 'length'])
            p2o.set_relational_fields([
                ('line_id', 'tcv.stock.changes', ['name']),
                ('product_id', 'product.product', ['default_code']),
                ('prod_lot_id', 'stock.production.lot', ['name']),
                ('product_uom', 'product.uom', ['name']),
                ])
            p2o.test_data_file()
