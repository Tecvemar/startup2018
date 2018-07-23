# -*- encoding: utf-8 -*-

from csv2open import csv_2_openerp
import sys


def load_fiscal_book(dbcomp):

    work_dir = '../data/common/'
    c2o = csv_2_openerp(
        work_dir + 'fiscal_book.csv', 'fiscal.book', dbcomp)
    c2o.set_search_fields(['type', 'period_id'])
    c2o.set_relational_fields([
        ('period_id', 'account.period', ['name']),
        ])
    c2o.update_records = True
    c2o.process_csv()
    c2o.done()

    postprocess_fiscal_book(dbcomp, 'purchase')
    postprocess_fiscal_book(dbcomp, 'sale')


def postprocess_fiscal_book(dbcomp, book_type):

    '''
    Update and confirm fiscal books
    '''
    msg = '  Postprocesando: fiscal.book'
    book_ids = dbcomp.execute(
        'fiscal.book', 'search', [('state', '=', 'draft'),
                                  ('type', '=', book_type)])
    if book_type == 'sale':
        dbcomp.execute(
            'fiscal.book', 'write', book_ids,
            {'article_number': '76'}, {'type': book_type})
    for book_id in book_ids:
        print msg + ' ' + str(book_id) + ' ' + str(book_type) + ' ' * 40 + '\r',
        sys.stdout.flush()
        dbcomp.execute(
            'fiscal.book', 'update_book', [book_id])
        dbcomp.execute_workflow(
            'fiscal.book', 'act_confirm', book_id)
        dbcomp.execute_workflow(
            'fiscal.book', 'act_done', book_id)
    print msg + ' ' + str(book_type) + ' Done.' + ' ' * 40
