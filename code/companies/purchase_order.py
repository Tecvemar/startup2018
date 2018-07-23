# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp
from profit2open import profit_2_openerp
import sys
import os


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


def load_purchase_order_extra(lnk, profit):
    work_dir = '../data/companies/%s/' % lnk.database
    work_csv = work_dir + 'purchase_order_extra.csv'
    if not os.path.isfile(work_csv):
        return
    c2o = csv_2_openerp(work_csv, 'purchase.order', lnk)
    c2o.set_search_fields(['origin'])
    c2o.set_relational_fields([
        ('partner_id', 'res.partner', ['ref']),
        ('location_id', 'stock.location', ['name']),
        ('pricelist_id', 'product.pricelist', ['name']),
        ('order_line.product_id', 'product.product', ['default_code']),
        ('order_line.concept_id', 'islr.wh.concept', ['name']),
        ('order_line.product_uom', 'product.uom', ['name']),
        ])
    c2o.set_m2m_fields([
        ('order_line.taxes_id', 'link', 'account.tax', ['name'])])
    c2o.set_child_model_fields(['order_line'])
    c2o.update_records = True
    c2o.process_csv()


def complete_purchase_invoice_data(dbcomp, dbprofit, order_id, journal_id):
    order = dbcomp.execute('purchase.order', 'read', order_id, [])
    params = {'nro_doc': int(order['origin'].split('-')[1])}
    dbprofit.set_sql_string('''
select c.fec_emis, rtrim(c.n_control) as n_control, monto_reten,
       case isnull(isv, 0) when 0 then 0 else
            round((ret_iva / isv) * 100, 0) end as wh_iva_rate,
       ret_iva, p.monto_reten,
       case c.fec_reg when '1900-01-01'
            then c.fec_emis else c.fec_reg end as fec_reg
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
            ('partner_id', '=', order['partner_id'][0]),
            ('id', '<=', order['id'])])
    if duplicated_ids:
        n_control = '%s-%s' % (n_control, len(duplicated_ids) - 1)
    data = {
        'date_invoice': profit_doc['fec_reg'].strftime('%Y-%m-%d %H:%M:%S'),
        'date_document': profit_doc['fec_emis'].strftime('%Y-%m-%d %H:%M:%S'),
        'comment': order.get('origin', ''),
        'nro_ctrl': n_control,
        'journal_id': journal_id[0],
        'wh_iva_rate': 0,
        'vat_apply': True,
        }
    data['date_invoice'] = data['date_document'] if data['date_invoice'] < data['date_document'] else data['date_invoice']
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
        if order['date_order'] < '2017-12-31' and order['name'][:5] == 'ODC18':
            data.update({'name': 'ODC17' + order['name'][5:]})
        if data:
            dbcomp.execute('purchase.order', 'write', order['id'], data)
        if order['state'] == 'draft' and not order['invoice_ids']:
            dbcomp.execute_workflow(
                'purchase.order', 'purchase_confirm', order['id'])
        complete_purchase_invoice_data(
            dbcomp, dbprofit, order['id'], journal_id)
    print msg + ' Listo.' + ' ' * 40
