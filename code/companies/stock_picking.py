# -*- encoding: utf-8 -*-
import sys

def postprocess_stock_picking(dbcomp, dbprofit):
    '''
    Process and Confirm stock in
    '''
    msg = '  Postprocesando: stock.picking'
    origin = dbcomp.execute(
        'stock.picking', 'search', [])
    for stock_in in dbcomp.execute('stock.picking', 'read', origin, []):
        print stock_in
        print msg + ' ' + stock_in['name'] + ' ' * 40 + '\r',
        sys.stdout.flush()
        if stock_in['state'] == 'assigned':
            dbcomp.execute(
                'stock.picking', 'action_process', [stock_in['id']])
            dbcomp.execute(
                'stock.picking', 'action_confirm', [stock_in['id']])
    print msg + ' Done.' + ' ' * 40
