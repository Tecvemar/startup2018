# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp


def load_sale_order(lnk, profit):
    if not profit:
        return
    p2o = profit_2_openerp('sale.order', lnk, profit)
    p2o.set_sql(
        '''
select c.fec_emis as date_order, nro_doc as partner_ref,
       observa as description, 8 as partner_shipping_id,
       8 as partner_order_id, 8 as partner_invoice_id,
       rtrim(tipo_doc) + '-' + ltrim(str(nro_doc)) as client_order_ref,
       rtrim(co_cli) as partner_id, 'Contado' as payment_term,
       'Stock' as location_id,'Public Pricelist' as pricelist_id
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
