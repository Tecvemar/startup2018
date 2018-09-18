# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp
from profit2open import profit_2_openerp
import sys
import os


def load_bank_moves(lnk, profit):
    if not profit:
        return
    p2o = profit_2_openerp('account.move', lnk, profit)
    p2o.set_sql(
        '''
select top 2000 'MB '+lTRIM(STR(mov_num))+ ' - '+tipo_op+' '+doc_num as ref,
    codigo as journal_id, fecha as date, '0' as to_check,
    lTRIM(STR(YEAR(fecha)))+'-'+right(STR(100+MONTH(fecha)),2) as period_id,
    1 as company_id, 'draft' as 'state', descrip as narration,
    1 as 'line_id.company_id',
    case cta_egre
        when '11002' then '1100100006'
        when '11320' then '8110600002'
        when '11403' then '1110400002'
        when '71301' then '7310200005'
        when '91130' then '7230300002'
        end as 'line_id.account_id',
    monto_d+idb as 'line_id.debit',
    monto_h as 'line_id.credit',
    '0' as 'line_id.reconcile'
from mov_ban
where origen = 'BAN' and fecha > '2017-01-01'
order by fecha, mov_num
        ''')
    p2o.set_search_fields(['ref'])
    p2o.set_relational_fields([
        ('journal_id', 'res.partner', ['ref']),
        ('line_id.account_id', 'account.account', ['name']),
        ('pricelist_id', 'product.pricelist', ['name']),
        ])
    p2o.test_csv()


