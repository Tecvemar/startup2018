# -*- encoding: utf-8 -*-
import sys


def postprocess_stock_picking(dbcomp, dbprofit):
    '''
    Process and Confirm stock picking 'in'
    '''
    msg = '  Postprocesando: stock.picking'
    picking_ids = dbcomp.execute(
        'stock.picking', 'search', [('state', '=', 'assigned'),
                                    ('type', '=', 'in')])

    # Write default driver & vehicle to all pickins
    stock_journal_id = dbcomp.execute(
        'stock.journal', 'search', [('name', '=', 'Compras Nacionales')])
    dbcomp.execute(
        'stock.picking', 'write', picking_ids,
        {'driver_id': 1, 'vehicle_id': 2,
         'stock_journal_id': stock_journal_id[0]})

    # Set lor location to B99
    b99_id = dbcomp.execute(
        'stock.location', 'search', [('name', '=', 'B99')])
    stock_id = dbcomp.execute(
        'stock.location', 'search', [('name', '=', 'Stock')])
    if b99_id and len(b99_id) == 1:
        move_ids = dbcomp.execute(
            'stock.move', 'search', [('pickind_id', 'in', picking_ids),
                                     ('location_dest_id', '=', stock_id[0])])
        dbcomp.execute(
            'stock.move', 'write', move_ids, {'location_dest_id': b99_id[0]})

    # Set pickings to done
    pickings = sorted(
        dbcomp.execute('stock.picking', 'read', picking_ids, []),
        key=lambda k: k['name'])
    for picking in pickings:
        print msg + ' ' + picking['name'] + ' ' * 40 + '\r',
        sys.stdout.flush()
        dbcomp.execute_workflow(
            'stock.picking', 'button_done', picking['id'])
    print msg + ' Done.' + ' ' * 40
