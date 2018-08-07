# -*- encoding: utf-8 -*-
import csv
import time


def stock_profit_open_inventory(dbcomp, dbprofit):

    profit_data = []
    lines_lot_data = []
    open_product_name = []
    with open('/home/dbernal/instancias/desarrollo/startup2018/code/verify/stock/inventory/2017/marzo.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            profit_data.append(row)
    productos = [x.get('descripcion') for x in profit_data]
    productos = set(productos)
    report_id = dbcomp.execute(
        'tcv.stock.by.location.report', 'create', {
            'date': time.strftime('2018-03-31'),
            'report_type': 'normal'
            })
    dbcomp.execute(
        'tcv.stock.by.location.report', 'button_load_inventory', [report_id])
    line_ids = dbcomp.execute(
        'tcv.stock.by.location.report.lines', 'search',
        [('line_id', '=', report_id)])
    lines = dbcomp.execute(
        'tcv.stock.by.location.report.lines', 'read', line_ids,
        ['product_id', 'prod_lot_id', 'product_qty'])
    for lot in lines:
        stock_product_lot = dbcomp.execute(
            'stock.production.lot', 'read', lot['prod_lot_id'], ['name'])
        lines_lot_data.append(stock_product_lot)
        product = dbcomp.execute(
            'product.product', 'read', lot['product_id'], ['name'])
        open_product_name.append(product['name'])
    open_product_name = set(open_product_name)
    for item in profit_data:
        if item['lote_produccion']:
            reg = int(item['lote_produccion'])
            prftname = item['descripcion']
            for lot in lines_lot_data:
                lot = int(lot['name'])
                if reg == lot and prftname in open_product_name:
                    print 'coinciden', lot, prftname
                else:
                    'no coinciden', lot, prftname
