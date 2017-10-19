# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp


def create_stock_production_lot_purchase_order_line(lnk, profit):
    '''
    To create stock.peoduction.lot records before load lines
    '''
    if not profit:
        return
    p2o = profit_2_openerp('stock.production.lot', lnk, profit)
    p2o.set_sql(
        '''
select rtrim(r.co_art) as "product_id",
       rtrim(nro_lote) as "name",
       c.fec_emis as "date",
       r.prec_vta as "property_cost_price",
       r.aux02 as "aux02"
from reng_com r
left join docum_cp c on r.fact_num = c.nro_doc and c.tipo_doc = 'FACT'
left join art a on r.co_art = a.co_art
where c.tipo_doc = 'FACT' and c.fec_emis >= '2017-01-01' and c.anulado = 0
order by r.fact_num, r.reng_num
        ''')
    p2o.set_search_fields(['name'])
    p2o.set_relational_fields([
        ('product_id', 'product.product', ['default_code']),
        ])
    p2o.aux02_field = 'aux02'
    p2o.set_aux02_fields(['heigth', 'length'])
    p2o.process_csv()
    #~ p2o.test_data_file()


def load_purchase_order_line_profit_detail(lnk, profit):
    create_stock_production_lot_purchase_order_line(lnk, profit)
    if not profit:
        return
    p2o = profit_2_openerp('purchase.order.line', lnk, profit)
    p2o.set_sql(
        '''
select rtrim(c.tipo_doc) + '-' + ltrim(str(c.nro_doc)) as order_id,
       rtrim(r.co_art) as product_id,
       'NO APLICA RETENCION' as concept_id, total_art as product_qty,
       'm2' as product_uom,
       a.art_des as name, c.fec_emis as date_planned,
       r.prec_vta as price_unit,
       rtrim(nro_lote) as "prod_lot_id",
       r.aux02 as "aux02",
       case str(r.tipo_imp) when 1 then 'IVA 12% Compras'
                            when 7 then 'IVA 7% Compras'
                            when 8 then 'IVA 9% Compras'
                            else '0' end as taxes_id
from reng_com r
left join docum_cp c on r.fact_num = c.nro_doc and c.tipo_doc = 'FACT'
left join art a on r.co_art = a.co_art
where c.tipo_doc = 'FACT' and c.fec_emis >= '2017-01-01' and c.anulado = 0
order by r.fact_num, r.reng_num
        ''')
    p2o.set_search_fields([])
    p2o.set_relational_fields([
        ('order_id', 'purchase.order', ['origin']),
        ('product_id', 'product.product', ['default_code']),
        ('prod_lot_id', 'stock.production.lot', ['name']),
        ('concept_id', 'islr.wh.concept', ['name']),
        ('product_uom', 'product.uom', ['name']),
        ])
    p2o.aux02_field = 'aux02'
    p2o.set_aux02_fields(['pieces'])
    p2o.set_m2m_fields([('taxes_id', 'link', 'account.tax', ['name'])])
    p2o.process_csv()
    #~ p2o.test_data_file()




def load_purchase_order_no_details(lnk, profit):
    if not profit:
        return
    p2o = profit_2_openerp('purchase.order.line', lnk, profit)
    p2o.set_sql(
        '''
select rtrim(c.tipo_doc) + '-' + ltrim(str(c.nro_doc)) as order_id,
       '7230100003' as product_id,
       'NO APLICA RETENCION' as concept_id, 1 as product_qty,
       'PCE' as product_uom, c.monto_bru as price_unit,
       rtrim(c.observa) as name, c.fec_emis as date_planned,
       case str(c.tipo) when 1 then 'IVA 12% Compras'
                        when 5 then 'IVA 0% Compras'
                        when 6 then 'IVA 0% Compras'
                        when 7 then 'IVA 7% Compras'
                        when 8 then 'IVA 9% Compras'
                        when 9 then 'IVA 8% Compras'
                        else str(c.tipo) end as taxes_id,
        rtrim(p.prov_des) as "x"
from docum_cp c
left join prov p on c.co_cli = p.co_prov
where c.tipo_doc = 'FACT' and c.fec_emis >= '2017-01-01' and c.anulado = 0
      and c.nro_doc not in (select distinct fact_num from reng_com)
union
select rtrim(c.tipo_doc) + '-' + ltrim(str(c.nro_doc)) as order_id,
       '7230100003' as product_id,
       'NO APLICA RETENCION' as concept_id, 1 as product_qty,
       'PCE' as product_uom, c.monto_otr as price_unit,
       rtrim(c.observa) as name, c.fec_emis as date_planned,
       'IVA 0% Compras' as taxes_id,
        rtrim(p.prov_des) as "x"
from docum_cp c
left join prov p on c.co_cli = p.co_prov
where c.tipo_doc = 'FACT' and c.fec_emis >= '2017-01-01' and c.anulado = 0
      and c.nro_doc not in (select distinct fact_num from reng_com) and
      c.monto_otr != 0
order by 1
        ''')
    p2o.set_search_fields([])
    p2o.set_relational_fields([
        ('order_id', 'purchase.order', ['origin']),
        ('product_id', 'product.product', ['default_code']),
        ('concept_id', 'islr.wh.concept', ['name']),
        ('product_uom', 'product.uom', ['name']),
        ])
    p2o.aux02_field = 'aux02'
    p2o.set_aux02_fields(['pieces'])
    p2o.set_m2m_fields([('taxes_id', 'link', 'account.tax', ['name'])])
    p2o.process_csv()
    #~ p2o.test_data_file()