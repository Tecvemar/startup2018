# -*- encoding: utf-8 -*-
import sys


def postprocess_stock_picking(dbcomp, dbprofit):
    '''
    Process and Confirm stock in
    '''
    msg = '  Postprocesando: stock.picking'
    origin = dbcomp.execute(
        'stock.picking', 'search', [])
    for picking in dbcomp.execute('stock.picking', 'read', origin, []):
        print msg + ' ' + picking['name'] + ' ' * 40 + '\r',
        sys.stdout.flush()
        if picking['state'] == 'assigned':
            dbcomp.execute_workflow(
                'stock.picking', 'button_done', picking['id'])
    print msg + ' Done.' + ' ' * 40
