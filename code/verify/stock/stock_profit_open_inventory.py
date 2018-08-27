# -*- encoding: utf-8 -*-
import csv

def stock_profit_open_inventory(dbcomp, dbprofit):

    profit_data = []              # Data  CSV (Porift)
    lines_lot_data = []           # Data lines  report (Open)
    open_product_name = []        # Products Names  (Open)
    prft_name_products = []       # Products Names (Profit)
    lots_not_checks = []          # Lots Profit not listed Open
    open_lot_numbers = []         # Lots numbers (Open)
    profit_not_lots = []          # Products  without number Lots (Profit)
    lots_qty_not_coincide = []    # Lots nots coincide en QTY
    lots_not_qty = []             # Lots not QTY (Profit)
    prft_not_lots_orders = []     # Products without  lots or sale orders
    with open('/home/dbernal/instancias/desarrollo/startup2018/code/' +
              'verify/stock/inventory/2018/mayo.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if ',' in row['cantidad']:
                row['cantidad'] = row['cantidad'].replace(',', '.')
            profit_data.append(row)
    # OPEN REPORT
    report_id = dbcomp.execute(
        'tcv.stock.by.location.report', 'create', {
            'date': '2018-05-31',
            'report_type': 'normal'
            })
    dbcomp.execute(
        'tcv.stock.by.location.report', 'button_load_inventory', [report_id])
    line_ids = dbcomp.execute(
        'tcv.stock.by.location.report.lines', 'search',
        [('line_id', '=', report_id)])
    # LINES REPORTS
    lines = dbcomp.execute(
        'tcv.stock.by.location.report.lines', 'read', line_ids,
        ['product_id', 'prod_lot_id', 'product_qty'])
    for lot in lines:
        stock_product_lot = dbcomp.execute(
            'stock.production.lot', 'read', lot['prod_lot_id'], ['name'])
        # QTY OF LOT IN LINE TO DICTIONARY 'stock_product_lot'
        stock_product_lot['product_qty'] = lot['product_qty']
        # ADD ALL DATA LINES TO LIST (DICTIONARY LIST)
        lines_lot_data.append(stock_product_lot)
        # ADD LOT NUMBER TO LIST
        open_lot_numbers.append(int(stock_product_lot['name']))
        # PRODUCTS NAMES OPEN
        product = dbcomp.execute(
            'product.product', 'read', lot['product_id'], ['name'])
        # ADD PRODUCTS NAMES OPEN TO LIST
        open_product_name.append(product['name'])
        # DELETE DUPLICATES NAMES PRODUCTS OPEN IN LIST NAMES PRODUCTS
    open_product_name = set(open_product_name)
    csv_lines = 1
    for item in profit_data:
        csv_lines += 1
        # VALIDATE LOT AND QTY IN CSV
        if item['lote_produccion'] and item['cantidad']:
            profit_lot_number = int(item['lote_produccion'])
            # VALIDATE LOT CSV EXISTENCE IN LOT NUMBER OPEN LIST
            if profit_lot_number in open_lot_numbers:
                if item['descripcion']:
                    profit_name_product = item['descripcion']
                    profit_qty = item['cantidad']
                    for lot in lines_lot_data:
                        open_qty = lot['product_qty']
                        open_lot_number = int(lot['name'])
                        open_qty = "{0:.4f}".format(lot['product_qty'])
                        # VALIDATE PROFIT LOT, OPEN LOT AN QUANTITIES BE EQUALS
                        if profit_lot_number == open_lot_number \
                                and profit_qty != open_qty:
                            # CREATE DICT
                            data = {'Lote': profit_lot_number,
                                    'ProfitQTY': profit_qty,
                                    'OpenQTY': open_qty,
                                    'Producto': profit_name_product,
                                    'LineaCSV': csv_lines
                                    }
                            lots_qty_not_coincide.append(data)  # DICT TO LIST
            # VALIDATE NOT EXISTENCE LOTS PROFIT IN LOTS OPEN
            elif profit_lot_number not in open_lot_numbers:
                # CREATE DICT
                data = {'Lote': profit_lot_number,
                        'Producto': item['descripcion'],
                        #~ 'LineaCSV': csv_lines
                        }
                lots_not_checks.append(data)                    # DICT TO LIST
        # VALIDATE LOT PROFIT WHITHOUT QTY
        elif item['lote_produccion'] and not item['cantidad']:
                # CREATE DICT
                data = {'Lote': item['lote_produccion'],
                        'Producto': item['descripcion'],
                        'LineaCSV': csv_lines
                        }
                lots_not_qty.append(data)                        # DICT TO LIST
        # VALIDATE NOT EXISTENCE LOT IN CSV
        elif not item['lote_produccion']:
            # VALIDATE  EXISTENCE SALE ORDER
            if item['descripcion'] and item['pedido']:
                # CREATE DICT
                data = {'Producto': item['descripcion'],
                        'Pedido': item['pedido'],
                        'LineaCSV': csv_lines
                        }
                profit_not_lots.append(data)                     # DICT TO LIST
            # VALIDATE PRODUCT PROFIT NAME AND PROFIT SALES ORDEN
            elif item['descripcion'] and not item['pedido']:
                # CREATE DICT
                data = {'Producto': item['descripcion'],
                        'LineaCSV': csv_lines
                        }
                prft_not_lots_orders.append(data)                # DICT TO LIST
        # VALIDATE EXISTENCE PRODUCT PROFIT NAME IN OPEN PRODUCTS NAME LIST
        if item['descripcion'] not in open_product_name:
            # ADD PRODUCT PROFIT NAME NON-EXISTENT LIST
            prft_name_products.append(item['descripcion'])
    # DELETE DUPLICATES PRODUCTS NAME IN LIST
    prft_name_products = set(prft_name_products)   # Delete duplicates products
    # LOTS PROFIT NOT LISTED IN OPEN DATA
    if len(lots_not_checks) > 0:
        # ORDER LIST
        for lote in lots_not_checks:
                d = {}
                for key, value in lote.items():
                    key = "\"{}\"".format(key)
                    value = "\"{}\"".format(value)
                    d[key] = value
                lots_not_checks.append(d)
        with open('/home/dbernal/instancias/desarrollo/startup2018/code/verify/stock/inventory/csv_lots_not_checks.csv', 'w') as csv_lots_not_checks:
            fieldnames = ["\"lote\"", "\"producto\""]
            #~ fieldnames = ['Lote', 'Producto']
            writer = csv.DictWriter(csv_lots_not_checks, fieldnames=fieldnames,
                                    quoting=csv.QUOTE_ALL, quotechar='"')
            writer.writeheader()
            writer.writerows(lots_not_checks)
        print '\n Los siguientes %s lotes no aparecen Open: \n' \
            % len(lots_not_checks)
        for prft_lot in lots_not_checks:
            print '%s \t %s \t LineaCSV: %s ' % (prft_lot['Lote'],
                                                 prft_lot['Producto'],
                                                 prft_lot['LineaCSV']
                                                 )
    # NOT COINCIDENTS QTY LOTS
    if len(lots_qty_not_coincide) > 0:
        lots_qty_not_coincide.sort(key=lambda lots: lots['Lote'])
        print '\n Los siguientes  %s lotes no coinciden en la cantidad: \n' \
            % len(lots_qty_not_coincide)
        for lots_qty in lots_qty_not_coincide:
            print '%s \t %s \t Profit: %s \t Open %s \t LineaCSV: %s '   \
                % (lots_qty['Lote'],
                   lots_qty['Producto'],
                   lots_qty['ProfitQTY'],
                   lots_qty['OpenQTY'],
                   lots_qty['LineaCSV'])
    #~ # CSV LOTS WITHOUT QTY
    if len(lots_not_qty) > 0:
        lots_not_qty.sort(key=lambda lots: lots['Lote'])
        print '\n Los siguientes %s lotes de Profit no registran cantidad:\n'\
            % len(lots_not_qty)
        for not_qty in lots_not_qty:
            print '%s \t %s \t LineaCSV: %s ' % (not_qty['Lote'],
                                                 not_qty['Producto'],
                                                 not_qty['LineaCSV'])
    # CSV DATA WITHOUT LOTS
    if len(profit_not_lots) > 0:
        print '\n Los siguientes %s Pedidos no tienen lotes en Profit \n'  \
              % len(profit_not_lots)
        for not_lot in profit_not_lots:
            print '%s \t %s \t LineaCSV: %s  ' % (not_lot['Producto'],
                                                  not_lot['Pedido'],
                                                  not_lot['LineaCSV'])
    # CSV DATA WITHOUT LOTS OR SALE ORDERS
    if len(prft_not_lots_orders) > 0:
        print '\n Los siguientes %s productos no tienen ni lote ni pedido: \n'\
            % len(prft_not_lots_orders)
        for lot_order in prft_not_lots_orders:
            print '%s \t Revisar linea %s del CSV ' % (lot_order['Producto'],
                                                       lot_order['LineaCSV'])
    # PRODUCTS NAMES PROFIT NOT LISTED IN OPEN
    if len(prft_name_products) > 0:
        print '\n Los siguientes %s productos no aparecen en Open: \n' \
            % len(prft_name_products)
        for name_product in prft_name_products:
            print name_product
