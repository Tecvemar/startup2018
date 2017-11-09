# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp
import sys


def load_sale_order(lnk, profit):
    if not profit:
        return
    p2o = profit_2_openerp('sale.order', lnk, profit)
    p2o.set_sql(
        '''
select c.fec_emis as date_order, nro_doc as partner_ref,
       observa as description, 1 as partner_shipping_id,
       1 as partner_order_id, 1 as partner_invoice_id,
       rtrim(tipo_doc) + '-' + ltrim(str(nro_doc)) as client_order_ref,
       rtrim(co_cli) as partner_id, 'Contado' as payment_term,
       'Stock' as location_id, 'Public Pricelist' as pricelist_id,
       'one' as picking_policy, 'manual' as order_policy,
       '2017-12-31' as date_due
from docum_cc c
where tipo_doc = 'FACT' and fec_emis >= '2017-01-01' and anulado = 0
order by nro_doc
        ''')
    p2o.set_search_fields(['client_order_ref'])
    p2o.set_relational_fields([
        ('partner_id', 'res.partner', ['ref']),
        ('location_id', 'stock.location', ['name']),
        ('pricelist_id', 'product.pricelist', ['name']),
        ('payment_term', 'account.payment.term', ['name']),
        ])
    p2o.process_csv()
    #~ p2o.test_data_file()


def complete_sale_invoice_data(dbcomp, dbprofit, order_id, journal_id):
    order = dbcomp.execute('sale.order', 'read', order_id, [])
    params = {'nro_doc': int(order['client_order_ref'].split('-')[1])}
    dbprofit.set_sql_string('''
select c.fec_emis, c.numcon as n_control, monto_reten,
       case isnull(isv, 0) when 0 then 0 else
            round((ret_iva / isv) * 100, 0) end as wh_iva_rate,
       ret_iva, p.monto_reten
from docum_cc c
left join reng_pag p on p.tp_doc_cob = 'FACT' and p.doc_num = c.nro_doc
where c.tipo_doc = 'FACT' and c.nro_doc = %(nro_doc)s
        ''' % params)
    profit_doc = dbprofit.execute_sql()[0]
    ##check n_control duplicated
    n_control = profit_doc['n_control'].strip()
    duplicated_ids = dbcomp.execute(
        'account.invoice', 'search', [
            ('nro_ctrl', 'ilike', n_control),
            ('partner_id', '=', order['partner_id'][0])])
    if duplicated_ids:
        n_control = '%s-%s' % (n_control, len(duplicated_ids))
    data = {
        'date_invoice': profit_doc['fec_emis'].strftime('%Y-%m-%d %H:%M:%S'),
        'date_document': profit_doc['fec_emis'].strftime('%Y-%m-%d %H:%M:%S'),
        'nro_ctrl': n_control,
        'journal_id': journal_id[0],
        'wh_iva_rate': float(profit_doc['wh_iva_rate']),
        'vat_apply': bool(profit_doc['ret_iva']),
        }
    dbcomp.execute(
        'account.invoice', 'write', order['invoice_ids'], data)
    for inv_id in order['invoice_ids']:
        dbcomp.execute_workflow(
            'account.invoice', 'invoice_open', inv_id)


def postprocess_sale_order(dbcomp, dbprofit):
    msg = '  Postprocesando: sale.order.'
    journal_id = dbcomp.execute(
        'account.journal', 'search', [
            ('name', '=', 'Diario / Ventas Nacionales')])
    order_ids = dbcomp.execute(
        'sale.order', 'search', [])
    orders = sorted(
        dbcomp.execute('sale.order', 'read', order_ids, []),
        key=lambda k: k['name'])
    for order in orders:
        print msg + ' ' + order['name'] + ' ' * 40 + '\r',
        sys.stdout.flush()
        data = {}
        if order['partner_shipping_id'][0] == 1:
            #~ Fix partner_address_id
            addrs_id = dbcomp.execute(
                'res.partner.address', 'search', [
                    ('type', '=', 'invoice'),
                    ('partner_id', '=', order['partner_id'][0]),
                    ])
            if addrs_id and len(addrs_id) == 1:
                data.update({
                    'partner_shipping_id': addrs_id[0],
                    'partner_order_id': addrs_id[0],
                    'partner_invoice_id': addrs_id[0],
                    })
            else:
                print '  No se encontró la dirección para: %s %s' % (
                    order['partner_id'], addrs_id)
        if data:
            dbcomp.execute('sale.order', 'write', order['id'], data)
        if order['state'] == 'draft' and not order['invoice_ids']:
            dbcomp.execute_workflow(
                'sale.order', 'order_confirm', order['id'])
            dbcomp.execute_workflow(
                'sale.order', 'manual_invoice', order['id'])
            complete_sale_invoice_data(
                dbcomp, dbprofit, order['id'], journal_id)
            stock_picking_approve(dbcomp, dbprofit, order['id'])

    print msg + ' Listo.' + ' ' * 40


def stock_picking_approve(dbcomp, dbprofit, order_id):

    '''
    Process and Confirm stock picking 'out'
    '''
    order = dbcomp.execute('sale.order', 'read', order_id, [])
    picking_ids = order['picking_ids']
    # Write default driver & vehicle to all pickins
    stock_journal_id = dbcomp.execute(
        'stock.journal', 'search', [('name', '=', 'Ordenes de Salida')])
    dbcomp.execute(
        'stock.picking', 'write', picking_ids,
        {'driver_id': 1, 'vehicle_id': 2,
         'stock_journal_id': stock_journal_id[0]})

    for picking_id in picking_ids:
        min_time = order['create_date'].split(' ')[1]
        min_date = order['date_order']
        dbcomp.execute(
            'stock.picking', 'write', [picking_id],
            {'min_date': '%s %s' % (min_date, min_time)})
        dbcomp.execute(
            'stock.picking', 'action_assign', [picking_id])
        dbcomp.execute_workflow(
            'stock.picking', 'button_done', picking_id)
