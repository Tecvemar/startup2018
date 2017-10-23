# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp
import sys


def load_purchase_order(lnk, profit):
    if not profit:
        return
    p2o = profit_2_openerp('purchase.order', lnk, profit)
    p2o.set_sql(
        '''
select c.fec_emis as date_order, nro_fact as partner_ref,
       observa as description, 8 as partner_address_id,
       rtrim(tipo_doc) + '-' + ltrim(str(nro_doc)) as origin,
       rtrim(co_cli) as partner_id, 'Stock' as location_id,
       'Default Purchase Pricelist' as pricelist_id
from docum_cp c
where tipo_doc = 'FACT' and fec_emis >= '2017-01-01' and anulado = 0
order by nro_doc
        ''')
    p2o.set_search_fields(['origin'])
    p2o.set_relational_fields([
        ('partner_id', 'res.partner', ['ref']),
        ('location_id', 'stock.location', ['name']),
        ('pricelist_id', 'product.pricelist', ['name']),
        ])
    p2o.process_csv()
    #~ p2o.test_data_file()


def postprocess_purchase_order(dbcomp):
    msg = 'Postprocesando: purchase.order.'
    order_ids = dbcomp.execute(
        'purchase.order', 'search', [])
    for order in dbcomp.execute('purchase.order', 'read', order_ids, []):
        print msg + ' ' + order['name'] + '\r',
        sys.stdout.flush()
        data = {}
        if order['partner_address_id'] == 8:
            #~ Fix partner_address_id
            addrs_id = dbcomp.execute(
                'res.partner.address', 'search', [
                    ('type', '=', 'invoice'),
                    ('partner_id', '=', order['partner_id'][0]),
                    ])
            if addrs_id and len(addrs_id) == 1:
                data.update({'partner_address_id': addrs_id[0]})
        if data:
            dbcomp.execute('purchase.order', 'write', order['id'], data)
        if order['state'] == 'draft' and not order['invoice_ids']:
            dbcomp.execute_workflow(
                'purchase.order', 'purchase_confirm', order['id'])

    print msg + ' Done.' + ' ' * 20
