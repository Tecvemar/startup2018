# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp


def load_sale_order_line_profit_detail(lnk, profit):
    if not profit:
        return
    p2o = profit_2_openerp('sale.order.line', lnk, profit)
    p2o.set_sql(
        '''
select rtrim(c.tipo_doc) + '-' + ltrim(str(c.nro_doc)) as order_id,
       rtrim(r.co_art) as product_id,
       'NO APLICA RETENCION' as concept_id,
       total_art as product_uom_qty, total_art as product_uos_qty,
       CASE rtrim(r.co_art)
          WHEN 'URISEUBLA673937' then 'PCE'
          WHEN 'SANHERBL' then 'PCE'
          WHEN 'MIN0029' then 'PCE'
          WHEN 'GALCLARP101L' then 'ml'
          ELSE 'm2' END as product_uom,
       a.art_des as name, c.fec_emis as date_planned,
       r.prec_vta as price_unit,
       rtrim(nro_lote) as "prod_lot_id",
       r.aux02 as "aux02",
       case str(r.tipo_imp) when 1 then 'IVA 12% Ventas'
                            when 7 then 'IVA 7% Ventas'
                            when 8 then 'IVA 9% Ventas'
                            else '0' end as tax_id
from reng_fac r
left join docum_cc c on r.fact_num = c.nro_doc and c.tipo_doc = 'FACT'
left join art a on r.co_art = a.co_art
where c.tipo_doc = 'FACT' and c.fec_emis >= '2017-01-01' and c.anulado = 0
order by r.fact_num, r.reng_num
        ''')
    p2o.set_relational_fields([
        ('order_id', 'sale.order', ['client_order_ref']),
        ('product_id', 'product.product', ['default_code']),
        ('prod_lot_id', 'stock.production.lot', ['name']),
        ('concept_id', 'islr.wh.concept', ['name']),
        ('product_uom', 'product.uom', ['name']),
        ])
    p2o.aux02_field = 'aux02'
    p2o.set_aux02_fields(['pieces'])
    p2o.set_m2m_fields([('tax_id', 'link', 'account.tax', ['name'])])
    p2o.process_csv()
    #~ p2o.test_data_file(False)
