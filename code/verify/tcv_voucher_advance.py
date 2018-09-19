# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp


'''
                 set advances to payments
'''


def check_tcv_voucher_advance(dbcomp, dbprofit):

    '''
                search for draft payments:
    '''
    if not dbprofit:
        return
    p2o = profit_2_openerp('tcv.voucher.advance', dbcomp, dbprofit)
    payments = dbcomp.execute(
        'account.voucher', 'search', [('state', '=', 'draft')])
    print len(payments)

