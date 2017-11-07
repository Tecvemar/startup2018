# -*- encoding: utf-8 -*-
import sys


def load_sale_order_confirm(dbcomp):
    '''
     Confirm    Sale Orders
    '''
    msg = '  Procesando: sale.order.'
    order_ids = dbcomp.execute(
        'sale.order', 'search', [])
    for order in dbcomp.execute('sale.order', 'read', order_ids, []):
        print msg + ' ' + order['name'] + ' ' * 40 + '\r',
        sys.stdout.flush()
        if order['state'] == 'draft':
            dbcomp.execute_workflow(
                'sale.order', 'order_confirm', order['id'])
    print msg + ' Done.' + ' ' * 40



