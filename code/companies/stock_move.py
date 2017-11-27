# -*- encoding: utf-8 -*-
import sys


def postprocess_stock_move(dbcomp):
    '''
    Fix stock move date
    '''
    msg = '  Postprocesando: stock.move.'
    print msg + '\r',
    fix_stock_inventory_moves(dbcomp, msg)
    fix_tcv_stock_changes_moves(dbcomp, msg)
    fix_purchase_order_moves(dbcomp, msg)
    fix_sale_order_moves(dbcomp, msg)

    print msg + ' Listo.' + ' ' * 40


def write_move_date(dbcomp, move_id, date):
    '''
    Launch SQL code to set new move date
    '''
    if not move_id or not date:
        print '\n\tError al asignar la fecha al movimiento: %d\n' % move_id
    sql = '''
    UPDATE stock_move set
           create_date = '%(date)s',
           date = '%(date)s',
           date_expected = '%(date)s'
          WHERE id = %(move_id)s
    '''
    params = {'move_id': move_id, 'date': date}
    dbcomp.execute_sql(sql, params)


def fix_picking_moves(dbcomp, picking_id, pk_date_fld, msg):
    '''
    Compute new date from stock picking and move data
    '''
    if picking_id:
        picking = dbcomp.execute(
            'stock.picking', 'read', picking_id, [])
        move_ids = picking['move_lines']
        print msg + ' ' + picking['name'] + ' ' * 40 + '\r',
        sys.stdout.flush()
        for move in dbcomp.execute('stock.move', 'read', move_ids, []):
            t_date = picking[pk_date_fld].split(' ')[0]
            t_time = move['date'].split(' ')[1]
            new_date = '%s %s' % (t_date, t_time)
            write_move_date(dbcomp, move['id'], new_date)


def fix_stock_inventory_moves(dbcomp, msg):
    inv_ids = dbcomp.execute(
        'stock.inventory', 'search', [])
    for inv in dbcomp.execute('stock.inventory', 'read', inv_ids, []):
        for move in dbcomp.execute('stock.move', 'read', inv['move_ids'], []):
            if move['prodlot_id']:
                lot = dbcomp.execute(
                    'stock.production.lot', 'read', move['prodlot_id'][0], [])
                print msg + ' ' + lot['name'] + ' ' * 40 + '\r',
                sys.stdout.flush()
                new_date = lot['date']
            else:
                new_date = inv['date']
            write_move_date(dbcomp, move['id'], new_date)


def fix_tcv_stock_changes_moves(dbcomp, msg):
    tsc_ids = dbcomp.execute(
        'tcv.stock.changes', 'search', [])
    for tsc in dbcomp.execute('tcv.stock.changes', 'read', tsc_ids, []):
        pk_id = tsc['picking_out_id'] and tsc['picking_out_id'][0]
        fix_picking_moves(dbcomp, pk_id, 'date', msg)
        pk_id = tsc['picking_in_id'] and tsc['picking_in_id'][0]
        fix_picking_moves(dbcomp, pk_id, 'date', msg)


def fix_purchase_order_moves(dbcomp, msg):
    po_ids = dbcomp.execute(
        'purchase.order', 'search', [])
    pk_ids = dbcomp.execute(
        'stock.picking', 'search', [('purchase_id', 'in', po_ids)])
    for pk_id in pk_ids:
        fix_picking_moves(dbcomp, pk_id, 'min_date', msg)


def fix_sale_order_moves(dbcomp, msg):
    so_ids = dbcomp.execute(
        'sale.order', 'search', [])
    pk_ids = dbcomp.execute(
        'stock.picking', 'search', [('sale_id', 'in', so_ids)])
    for pk_id in pk_ids:
        fix_picking_moves(dbcomp, pk_id, 'date', msg)
