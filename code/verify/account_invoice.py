# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp


def check_account_invoice(dbcomp, dbprofit):

    '''
                verify that the profit invoices
                are equal to the openerp invoices

    '''
    if not dbprofit:
        return
    p2o = profit_2_openerp('account.invoice', dbcomp, dbprofit)
    p2o.set_sql(
        '''
select c.fec_emis as date_order, nro_fact as partner_ref,
       observa as description, 8 as partner_address_id,
       rtrim(tipo_doc) + '-' + ltrim(str(nro_doc)) as origin,
       rtrim(co_cli) as partner_id, 'Stock' as location_id,
       'Default Purchase Pricelist' as pricelist_id, monto_net
from docum_cp c
where tipo_doc = 'FACT' and fec_emis >= '2017-01-01' and anulado = 0
order by nro_doc
        ''')

    p2o.load_data()

    for item in p2o.data:
        order_id = dbcomp.execute(
            'purchase.order', 'search', [
                ('origin', '=', item.get('origin'))])
        for order in dbcomp.execute(
                'purchase.order', 'read', order_id, ['invoice_ids']):
            if order.get('invoice_ids'):

                for invoice in dbcomp.execute(
                        'account.invoice', 'read', order['invoice_ids'], []):

                    if invoice.get('supplier_invoice_number') == item.get('partner_ref') and \
                            invoice.get('date_document') == item.get('date_order') and \
                                invoice.get('amount_total') == item.get('monto_net'):

                        print 'ok'
                    else:
                        print invoice.get('supplier_invoice_number') , item.get('partner_ref')
                        print invoice.get('date_document') , item.get('date_order')
                        print invoice.get('amount_total') , float( item.get('monto_net'))

            else:
                print 'No se encontro la factura de compra: %s' % item.get('origin')
