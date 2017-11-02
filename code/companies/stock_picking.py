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
    dbcomp.execute('stock.picking', 'write', picking_ids,
                   {'driver_id': 1, 'vehicle_id': 2})
    for picking in dbcomp.execute('stock.picking', 'read', picking_ids,
                                  []):
        print msg + ' ' + picking['name'] + ' ' * 40 + '\r',
        sys.stdout.flush()
        dbcomp.execute_workflow(
            'stock.picking', 'button_done', picking['id'])
    print msg + ' Done.' + ' ' * 40
