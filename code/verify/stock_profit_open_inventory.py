# -*- encoding: utf-8 -*-
import sys
from profit2open import profit_2_openerp


'''
                 verify that the profit invoices
                 are equal to the openerp invoices
'''


def stock_profit_open_inventory(dbcomp, dbprofit):
profit_data = []
    lines_lot_data = []
    with open('inventory/2018/marzo.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                profit_data.append(row)
    report_id = lnk.execute(
        'tcv.stock.by.location.report', 'create', {
            'date': time.strftime('2018-03-31'),
            'report_type': 'normal'
            })
    lnk.execute(
        'tcv.stock.by.location.report', 'button_load_inventory', [report_id])
    line_ids = lnk.execute(
        'tcv.stock.by.location.report.lines', 'search',
        [('line_id', '=', report_id)])
    lines = lnk.execute(
        'tcv.stock.by.location.report.lines', 'read', line_ids,
        ['product_id', 'prod_lot_id'])
    #~ print lines
    for lot in lines:
        #~ lines_lot_data.append(lot['prod_lot_id'])
        stock_product_lot = lnk.execute(
            'stock.production.lot', 'read', lot['prod_lot_id'],['name'] )
        product = lnk.execute(
            'product.product', 'read', lot['product_id'],['name'] )
        print stock_product_lot, product
