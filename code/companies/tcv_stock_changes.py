# -*- encoding: utf-8 -*-
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
    c2o.set_search_fields(['name'])
    c2o.set_relational_fields([
        ('method_id', 'tcv.stock.changes.method', ['name']),
        ])
    c2o.process_csv()
    load_tcv_stock_changes_lines(dbcomp, dbprofit)
    postprocess_tcv_stock_changes(dbcomp, dbprofit)


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
                from reng_aju where ajue_num=%s
                ''' % adj['name'])
            p2o.set_aux02_fields(['heigth', 'length'])
            p2o.set_relational_fields([
                ('line_id', 'tcv.stock.changes', ['name']),
                ('product_id', 'product.product', ['default_code']),
                ('prod_lot_id', 'stock.production.lot', ['name']),
                ('product_uom', 'product.uom', ['name']),
                ('location_id', 'stock.location', ['name']),
                ])
            p2o.test_data_file()
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
                item['pieces'] = 0
                item['new_qty'] = spl['lot_factor']
                item['cost_price'] = spl['property_cost_price']
                p2o.write_data_row(item)
            p2o.done()


def postprocess_tcv_stock_changes(dbcomp, dbprofit):
    msg = '  Postprocesando: tcv.stock.changes.'
    adjust_ids = dbcomp.execute(
        'tcv.stock.changes', 'search', [])
    adjusts = sorted(
        dbcomp.execute('tcv.stock.changes', 'read', adjust_ids, []),
        key=lambda k: k['name'])
    for adjust in adjusts:
        print msg + ' ' + adjust['name'] + ' ' * 40 + '\r',
        sys.stdout.flush()
        if adjust['state'] == 'draft':
            dbcomp.execute_workflow(
                'tcv.stock.changes', 'button_confirm', adjust['id'])
            dbcomp.execute_workflow(
                'tcv.stock.changes', 'button_done', adjust['id'])
            approved = dbcomp.execute(
                'tcv.stock.changes', 'read', adjust['id'], [])
            # First aproval out picking
            if approved['picking_out_id']:
                dbcomp.execute(
                    'stock.picking', 'action_assign',
                    [approved['picking_out_id']])
                dbcomp.execute_workflow(
                    'stock.picking', 'button_done', approved['picking_out_id'])
            # Then aproval in picking
            if approved['picking_in_id']:
                dbcomp.execute_workflow(
                    'stock.picking', 'button_done', approved['picking_in_id'])

    print msg + ' Listo.' + ' ' * 40
