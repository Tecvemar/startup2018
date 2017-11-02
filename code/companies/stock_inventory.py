# -*- encoding: utf-8 -*-
import sys


def postprocess_stock_inventory(dbcomp, dbprofit):
    '''
    Confirm and set done stock_inventory model records
    This model don't use workflow
    '''
    msg = '  Postprocesando: stock.inventory.'
    inv_ids = dbcomp.execute(
        'stock.inventory', 'search', [('state', '=', 'draft')])
    for inv in dbcomp.execute('stock.inventory', 'read', inv_ids, []):
        print msg + ' ' + inv['name'] + ' ' * 40 + '\r',
        sys.stdout.flush()
        dbcomp.execute(
            'stock.inventory', 'action_confirm', [inv['id']])
        dbcomp.execute(
            'stock.inventory', 'action_done', [inv['id']])
    print msg + ' Done.' + ' ' * 40
