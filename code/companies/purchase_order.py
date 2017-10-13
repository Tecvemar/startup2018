# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp


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
