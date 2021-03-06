# -*- encoding: utf-8 -*-
'''
Migrate tcv_stock_changes
'''
import os
import sys
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
    c2o.set_search_fields(['ref'])
    c2o.set_relational_fields([
        ('method_id', 'tcv.stock.changes.method', ['name']),
        ])
    c2o.process_csv()
    load_tcv_stock_changes_lines(dbcomp, dbprofit)
    load_tcv_stock_changes_lines_extra(dbcomp)
    postprocess_tcv_stock_changes(dbcomp)


def load_tcv_stock_changes_lines(dbcomp, dbprofit):
    '''
    Profit's adjustements migration (lines)
    '''
    adjust_ids = dbcomp.execute('tcv.stock.changes', 'search', [])
    adjusts = sorted(
        dbcomp.execute('tcv.stock.changes', 'read', adjust_ids, [],),
        key=lambda k: k['name'])
    p2o = profit_2_openerp('tcv.stock.changes.lines', dbcomp, dbprofit)
    for adj in adjusts:
        if adj['state'] == 'draft' and not adj['line_ids']:
            p2o.set_sql(
                '''
                select ajue_num as line_id, rtrim(nro_lote) as prod_lot_id,
                rtrim(co_art) as product_id, aux02, 1 as pieces,
                'm2' as product_uom, 'B99' as location_id
                from reng_aju
                where ajue_num=%s and
                      nro_lote not in ('05200005442', '0520004705',
                                       '05200005447', '90583'
                                       )
                ''' % adj['ref'])
            p2o.set_aux02_fields(['heigth', 'length'])
            p2o.set_relational_fields([
                ('line_id', 'tcv.stock.changes', ['ref']),
                ('product_id', 'product.product', ['default_code']),
                ('prod_lot_id', 'stock.production.lot', ['name']),
                ('product_uom', 'product.uom', ['name']),
                ('location_id', 'stock.location', ['name']),
                ])
            # Can't use Process_csv, do it "by hand"
            p2o.load_data()
            for item in p2o.data:
                # Complete adjust data before create
                item['new_heigth'] = item['heigth']
                item['new_length'] = item['length']
                item['new_pieces'] = item['pieces']
                spl = dbcomp.execute(
                    'stock.production.lot', 'read', item['prod_lot_id'], [])
                item['heigth'] = spl['heigth']
                item['length'] = spl['length']
                item['pieces'] = 1
                item['new_qty'] = spl['lot_factor']
                item['cost_price'] = spl['property_cost_price']
                p2o.write_data_row(item)
    p2o.done()


def load_tcv_stock_changes_lines_extra(dbcomp):
    '''
    Profit's adjustements migration (lines)
    '''
    work_dir = '../data/companies/%s/' % dbcomp.database
    work_csv = work_dir + 'tcv_stock_changes_lines.csv'
    if not os.path.isfile(work_csv):
        return
    c2o = csv_2_openerp(work_csv, 'tcv.stock.changes.lines', dbcomp)
    c2o.set_search_fields(['line_id', 'prod_lot_id'])
    c2o.set_relational_fields([
        ('line_id', 'tcv.stock.changes', ['ref']),
        ('product_id', 'product.product', ['default_code']),
        ('prod_lot_id', 'stock.production.lot', ['name']),
        ('product_uom', 'product.uom', ['name']),
        ('location_id', 'stock.location', ['name']),
        ])
    c2o.set_float_fields([
        'length', 'heigth', 'new_length', 'new_heigth', 'qty_diff',
        'new_qty', 'qty', 'width', 'new_width', 'cost_price'])
    c2o.set_integer_fields(['pieces', 'new_pieces'])
    c2o.update_records = True
    c2o.process_csv()


def postprocess_tcv_stock_changes(dbcomp):
    '''
    tcv_stock_changes approval process
    '''
    msg = '  Postprocesando: tcv.stock.changes.'
    adjust_ids = dbcomp.execute(
        'tcv.stock.changes', 'search', [])
    adjusts = sorted(
        dbcomp.execute('tcv.stock.changes', 'read', adjust_ids, []),
        key=lambda k: k['name'])
    for adjust in adjusts:
        print msg + ' ' + adjust['ref'] + ' ' * 40 + '\r',
        sys.stdout.flush()
        if adjust['state'] == 'draft':
            dbcomp.execute_workflow(
                'tcv.stock.changes', 'button_confirm', adjust['id'])
            dbcomp.execute_workflow(
                'tcv.stock.changes', 'button_done', adjust['id'])
            approved = dbcomp.execute(
                'tcv.stock.changes', 'read', adjust['id'], [])
            # First aproval the 'out' picking
            if approved['picking_out_id']:
                dbcomp.execute(
                    'stock.picking', 'draft_validate',
                    [approved['picking_out_id'][0]])
                dbcomp.execute_workflow(
                    'stock.picking', 'button_done',
                    approved['picking_out_id'][0])
            # Then, aproval the 'in' picking
            if approved['picking_in_id']:
                dbcomp.execute(
                    'stock.picking', 'draft_validate',
                    [approved['picking_in_id'][0]])
                dbcomp.execute_workflow(
                    'stock.picking', 'button_done',
                    approved['picking_in_id'][0])

    print msg + ' Listo.' + ' ' * 40
