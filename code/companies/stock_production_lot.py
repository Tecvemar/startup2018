# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp
from csv2open import csv_2_openerp
import os


def load_stock_production_lot(lnk, profit):
    if not profit:
        return
    p2o = profit_2_openerp('stock.production.lot', lnk, profit)
    p2o.set_sql(
        '''
select rtrim(r.nro_lote) as name, rtrim(r.co_art) as product_id,
       e.fec_emis as date, rtrim(n.aux02) as aux02,
       n.prec_vta as property_cost_price
from factura f
left join reng_fac r on r.fact_num = f.fact_num
left join reng_com n on r.nro_lote = n.nro_lote and r.co_art = n.co_art
left join compras e on n.fact_num = e.fact_num
where f.fec_emis between '2017-01-01' and '2017-12-31' and
      e.fec_emis < '2017-01-01' and f.anulada = 0 and
      rtrim(r.nro_lote) != ''
group by r.nro_lote, r.co_art, e.fec_emis, n.aux02, n.prec_vta
        ''')
    p2o.set_search_fields(['name', 'product_id'])
    p2o.set_relational_fields([
        ('product_id', 'product.product', ['default_code']),
        ])
    p2o.set_aux02_fields(['heigth', 'length'])
    p2o.process_csv()
    #~ p2o.test_data_file()


def load_stock_production_lot_extra(lnk):
    '''
    Load extra lots from Profit data -> csv
    '''
    work_dir = '../data/companies/%s/' % lnk.database
    work_csv = work_dir + 'stock_production_lot.csv'
    if not os.path.isfile(work_csv):
        return
    c2o = csv_2_openerp(work_csv, 'stock.production.lot', lnk)
    c2o.set_search_fields(['name', 'product_id'])
    c2o.set_relational_fields([
        ('product_id', 'product.product', ['default_code']),
        ])
    c2o.set_aux02_fields(['heigth', 'length'])
    c2o.process_csv()
    #~ p2o.test_data_file()
