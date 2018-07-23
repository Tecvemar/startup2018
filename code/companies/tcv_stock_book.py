# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp
#~ import sys


def load_tcv_stock_book(dbcomp):

    work_dir = '../data/common/'
    c2o = csv_2_openerp(
        work_dir + 'tcv_stock_book.csv', 'tcv.stock.book', dbcomp)
    c2o.set_search_fields(['period_id'])
    c2o.set_relational_fields([
        ('period_id', 'account.period', ['name']),
        ])
    c2o.load_data()
    c2o.done()

    msg = '  Postprocesando: tcv.stock.book'
    for book in c2o.data:
        print msg + ' ' + str(book['name']) + ' ' * 40 + '\r',
        book_id = c2o.write_data_row(book)
        if book_id:
            dbcomp.execute(
                'tcv.stock.book', 'button_update_book', [book_id])
            if book['name'] == u'Libro de Inventario Enero 2017':
                line_ids = dbcomp.execute(
                    'tcv.stock.book.lines', 'search',
                    [('book_id', '=', book_id)])
                if line_ids:
                    for line in dbcomp.execute(
                            'tcv.stock.book.lines', 'read', line_ids, []):
                        stock_init = line['stock_theoric'] - line['stock_end']
                        dbcomp.execute(
                            'tcv.stock.book.lines', 'write', line['id'],
                            {'stock_init': stock_init})
                dbcomp.execute(
                    'tcv.stock.book', 'button_update_book', [book_id])
    print msg + ', Done.' + ' ' * 40
    c2o.done()
