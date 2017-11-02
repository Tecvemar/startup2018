# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp


'''
                 verify that the profit invoices
                 are equal to the openerp invoices
'''


def check_account_invoice_purchases(dbcomp, dbprofit):

    '''
                purchases invoices verify:
    '''
    if not dbprofit:
        return
    p2o = profit_2_openerp('account.invoice', dbcomp, dbprofit)
    p2o.set_sql(
        '''
select c.fec_emis as date_document, nro_fact as supplier_invoice_number,
       observa as description, 8 as partner_address_id,
       rtrim(tipo_doc) + '-' + ltrim(str(nro_doc)) as origin,
       rtrim(co_cli) as partner_id, 'Stock' as location_id,
       'Default Purchase Pricelist' as pricelist_id, monto_net as amount_total
from docum_cp c
where tipo_doc = 'FACT' and fec_emis >= '2017-01-01' and anulado = 0
order by nro_doc
        ''')
    p2o.load_data()
    chk_fields = ('supplier_invoice_number',
                  'date_document',
                  'amount_total',
                  )
    for field in chk_fields:
        print field

    for item in p2o.data:

        #~ print item
        order_id = dbcomp.execute(
            'purchase.order', 'search', [
                ('origin', '=', item.get('origin'))])
        for order in dbcomp.execute(
                'purchase.order', 'read', order_id, ['invoice_ids']):
            if order.get('invoice_ids'):
                for invoice in dbcomp.execute(
                        'account.invoice', 'read', order['invoice_ids'], []):
                    for field in chk_fields:
                        if type (invoice.get(field)) == float and \
                                abs(invoice.get(field) - item.get(field)) < 0.1:
                            print 'ok'
                        elif invoice.get(field) == item.get(field):
                            print 'ok'
                        else:
                            print 'Error ' , field,  invoice.get(field), item.get(field)
                    if invoice.get('address_invoice_id') == 1:
                        print invoice.get('address_invoice_id')
                        print 'error en la dirección'
            else:
                print order, 'No se encontró la factura de compra: %s' \
                    % item.get('origin')


