# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp
import sys


def load_purchase_order(lnk, profit):
    if not profit:
        return
    p2o = profit_2_openerp('purchase.order', lnk, profit)
    p2o.set_sql(
        '''
select c.fec_emis as date_order, rtrim(nro_fact) as partner_ref,
       rtrim(observa) as description, 1 as partner_address_id,
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


def complete_purchase_invoice_data(dbcomp, dbprofit, order_id, journal_id):
    order = dbcomp.execute('purchase.order', 'read', order_id, [])
    params = {'nro_doc': int(order['origin'].split('-')[1])}
    dbprofit.set_sql_string('''
select c.fec_emis, rtrim(c.n_control) as n_control, monto_reten,
       case isnull(isv, 0) when 0 then 0 else
            round((ret_iva / isv) * 100, 0) end as wh_iva_rate,
       ret_iva, p.monto_reten
from docum_cp c
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


def postprocess_purchase_order(dbcomp, dbprofit):
    msg = '  Postprocesando: purchase.order.'
    order_ids = dbcomp.execute(
        'purchase.order', 'search', [])
    journal_id = dbcomp.execute(
        'account.journal', 'search', [
            ('name', '=', 'Diario / Compras Nacionales')])
    orders = sorted(
        dbcomp.execute('purchase.order', 'read', order_ids, [],),
        key=lambda k: k['name'])
    for order in orders:
        print msg + ' ' + order['name'] + ' ' * 40 + '\r',
        sys.stdout.flush()
        data = {}
        if order['partner_address_id'][0] == 1:
            #~ Fix partner_address_id
            addrs_id = dbcomp.execute(
                'res.partner.address', 'search', [
                    ('type', '=', 'invoice'),
                    ('partner_id', '=', order['partner_id'][0]),
                    ])
            if addrs_id and len(addrs_id) == 1:
                data.update({'partner_address_id': addrs_id[0]})
            else:
                print '  No se encontró la dirección para: %s %s' % (
                    order['partner_id'], addrs_id)
        if data:
            dbcomp.execute('purchase.order', 'write', order['id'], data)
        if order['state'] == 'draft' and not order['invoice_ids']:
            dbcomp.execute_workflow(
                'purchase.order', 'purchase_confirm', order['id'])
        complete_purchase_invoice_data(
            dbcomp, dbprofit, order['id'], journal_id)
    print msg + ' Listo.' + ' ' * 40
