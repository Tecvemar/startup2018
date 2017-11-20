# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp
#~ from csv2open import csv_2_openerp
#~ import os


def load_stock_inventory_line(dbcomp, dbprofit):
    if not dbprofit:
        return
    p2o = profit_2_openerp('stock.inventory.line', dbcomp, dbprofit)
    p2o.set_sql(
        '''
select 'Inventario Inicial Migración' as inventory_id, 'B99' as location_id,
        rtrim(r.nro_lote) as prod_lot_id, rtrim(r.co_art) as product_id,
        max(n.total_art) as product_qty,
        rtrim(n.aux02) as aux02,
        'm2' as product_uom, 1 as pieces_qty
from factura f
left join reng_fac r on r.fact_num = f.fact_num
left join reng_com n on r.nro_lote = n.nro_lote and r.co_art = n.co_art
left join compras e on n.fact_num = e.fact_num
where  f.fec_emis  >= '2017-01-01' and
      e.fec_emis < '2017-01-01' and
      rtrim(r.nro_lote) != ''
group by r.nro_lote, r.co_art, e.fec_emis, n.aux02, n.prec_vta
union
select 'Inventario Inicial Migración (Lotes adicionales)' as inventory_id,
       'B99' as location_id,
        rtrim(r.nro_lote) as prod_lot_id, rtrim(r.co_art) as product_id,
        max(n.total_art) as product_qty,
        rtrim(n.aux02) as aux02,
        CASE rtrim(r.co_art)
          WHEN 'URISEUBLA673937' then 'PCE'
          WHEN 'SANHERBL' then 'PCE'
          WHEN 'MIN0029' then 'PCE'
          WHEN 'GALCLARP101L' then 'ml'
          ELSE 'm2' END as product_uom, 1 as pieces_qty
from factura f
left join reng_fac r on r.fact_num = f.fact_num
left join reng_ndr n on r.nro_lote = n.nro_lote and r.co_art = n.co_art
left join not_rec e on n.fact_num = e.fact_num
where r.nro_lote in ('05200001244', -- barcelona
                     '91016', --guayana
                     '93048', '57895', '4381', '4223',  --monagas
                     '65808', '65806', '56568', '56567', '65703',  --sigue..
                     '65702', '65701', '10544', '56569',  --valencia
                     '62424', '56228',  --barquisimeto
                     '05200005043' --falcon
                     )
group by r.nro_lote, r.co_art, e.fec_emis, n.aux02, n.prec_vta
order by 1,4,3
        ''')

    p2o.set_search_fields(['prod_lot_id'])
    p2o.set_relational_fields([
        ('inventory_id', 'stock.inventory', ['name']),
        ('location_id', 'stock.location', ['name']),
        ('prod_lot_id', 'stock.production.lot', ['name']),
        ('product_id', 'product.product', ['default_code']),
        ('product_uom', 'product.uom', ['name']),
        ])
    p2o.process_csv()
    #~ p2o.test_data_file()



