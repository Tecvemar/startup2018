# -*- encoding: utf-8 -*-
import os
from csv2open import csv_2_openerp
from profit2open import profit_2_openerp


def create_stock_production_lot_purchase_order_line(lnk, profit):
    '''
    To create stock.production.lot records before load lines
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
where c.tipo_doc = 'FACT' and c.fec_emis >= '2017-01-01' and c.anulado = 0 and
      rtrim(nro_lote) != ''
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
    if not profit:
        return
    create_stock_production_lot_purchase_order_line(lnk, profit)
    p2o = profit_2_openerp('purchase.order.line', lnk, profit)
    p2o.set_sql(
        '''
select rtrim(c.tipo_doc) + '-' + ltrim(str(c.nro_doc)) as order_id,
       rtrim(r.co_art) as product_id,
       'NO APLICA RETENCION' as concept_id, total_art as product_qty,
       CASE rtrim(r.co_art)
          WHEN 'ADSELLGA130' then 'PCE'
          ELSE 'm2' END as product_uom,
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
    # p2o.set_search_fields(['order_id']) No search, allways add lines!
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
       rtrim(c.campo1) as product_id,
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
where (c.tipo_doc = 'FACT' and c.fec_emis >= '2017-01-01' and c.anulado = 0
      and c.nro_doc not in (select distinct fact_num from reng_com))
      or c.campo8='openerp'
union
select rtrim(c.tipo_doc) + '-' + ltrim(str(c.nro_doc)) as order_id,
       rtrim(c.campo1) as product_id,
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


def load_sale_order_line_profit_detail(lnk, profit):
    if not profit:
        return
    p2o = profit_2_openerp('sale.order.line', lnk, profit)
    p2o.set_sql(
        '''
select rtrim(c.tipo_doc) + '-' + ltrim(str(c.nro_doc)) as order_id,
       rtrim(r.co_art) as product_id,
       'NO APLICA RETENCION' as concept_id, total_art as product_qty,
       CASE rtrim(r.co_art)
          WHEN 'URISEUBLA673937' then 'PCE'
          WHEN 'SANHERBL' then 'PCE'
          WHEN 'MIN0029' then 'PCE'
          ELSE 'm2' END as product_uom,
       a.art_des as name, c.fec_emis as date_planned,
       r.prec_vta as price_unit,
       rtrim(nro_lote) as "prod_lot_id",
       r.aux02 as "aux02",
       case str(r.tipo_imp) when 1 then 'IVA 12% Ventas'
                            when 7 then 'IVA 7% Ventas'
                            when 8 then 'IVA 9% Ventas'
                            else '0' end as taxes_id
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
    p2o.set_m2m_fields([('taxes_id', 'link', 'account.tax', ['name'])])
    #~ p2o.process_csv()
    p2o.test_data_file(False)


def load_extra_purchase_detail(dbcomp, dbprofit):
    '''
    Profit's adjustements migration
    Need a csv list manually created with "extra purchase detail"
    '''
    work_dir = '../data/companies/%s/' % dbcomp.database
    work_csv = work_dir + 'extra_purchase_detail.csv'
    if not os.path.isfile(work_csv):
        return
    c2o = csv_2_openerp(work_csv, 'purchase.order.line', dbcomp)
    c2o.set_search_fields([])
    c2o.set_relational_fields([
        ('order_id', 'purchase.order', ['origin']),
        ('product_id', 'product.product', ['default_code']),
        ('concept_id', 'islr.wh.concept', ['name']),
        ('product_uom', 'product.uom', ['name']),
        ])
    c2o.aux02_field = 'aux02'
    c2o.set_aux02_fields(['pieces'])
    c2o.set_m2m_fields([('taxes_id', 'link', 'account.tax', ['name'])])
    procesed = []
    c2o.load_data()
    for line in c2o.data:
        order_id = line.get('order_id')
        if order_id not in procesed:
            #  First time, delete any existing sale order line
            procesed.append(order_id)
            line_ids = dbcomp.execute(
                'purchase.order.line', 'search', [('order_id', '=', order_id)])
            dbcomp.execute(
                'purchase.order.line', 'unlink', line_ids)
        c2o.write_data_row(line)
    c2o.done
