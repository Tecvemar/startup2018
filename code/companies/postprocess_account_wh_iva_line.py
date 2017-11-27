# -*- encoding: utf-8 -*-
import sys
from profit2open import profit_2_openerp


def postprocess_account_wh_iva_line(dbcomp, dbprofit):

    p2o = profit_2_openerp('account.wh.iva.line', dbcomp)
    p2o.set_search_fields(['code'])
    p2o.set_relational_fields([
    ('invoice_id', 'account.invoice', ['supplier_invoice_number']),
    ('fb_id', 'fiscal.book', ['supplier_invoice_number']),
    ])
    p2o.process_csv()
#~ #~
    '''
    Update and confirm fiscal books
    '''
    #~ msg = '  Postprocesando: account.invoice'
#~
    #~ for item in invoice_id:
        #~ print msg + ' ' * 40 + '\r'
        #~ sys.stdout.flush()
        #~ dbcomp.execute(
            #~ 'adjust.wh.islr.doc', 'write', invoice_id,
            #~ {'boolean': True})
        #~ dbcomp.execute(
            #~ 'account.invoice', 'adjust_wh_islr_doc', [invoice_id])
    #~ print msg + ' ' + 'invoice_id' + 'Done.' + ' ' * 40
#~ #~






















