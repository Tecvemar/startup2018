# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp


def load_bank_moves(dbcomp, dbprofit):
    if not dbprofit:
        return
    p2o = profit_2_openerp('account.move', dbcomp, dbprofit)
    p2o.set_sql(
        '''
select 'MB '+lTRIM(STR(mov_num))+ ' - '+tipo_op+' '+doc_num as ref,
    rtrim(codigo) as journal_id, fecha as date, '0' as to_check,
    LTRIM(STR(YEAR(fecha)))+'-'+right(STR(100+MONTH(fecha)),2) as period_id,
    1 as company_id, 'draft' as 'state', descrip as narration,
    1 as 'line_id.company_id',
    case cta_egre
    -- Ajustar en cada acropolis segun corresponda
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
where origen = 'BAN' and fecha > '2017-01-01' and anulado = 0
order by fecha, mov_num
        ''')
    p2o.set_search_fields(['ref'])
    p2o.set_relational_fields([
        ('line_id.account_id', 'account.account', ['code']),
        ('journal_id', 'account.journal', ['code']),
        ('period_id', 'account.period', ['code']),
        ])
    p2o.load_data()
    for item in p2o.data:
        p2o.show_wait()
        journal = dbcomp.execute(
            'account.journal', 'read', item['journal_id'],
            ['default_debit_account_id'])
        move = {x: item[x] for x in (
            'ref', 'journal_id', 'date', 'company_id', 'state',
            'to_check', 'narration', 'period_id')}
        line_1 = {
            'auto': True,
            'company_id': item['company_id'],
            'account_id': item['line_id.account_id'],
            'name': item['narration'],
            'debit': item['line_id.debit'],
            'credit': item['line_id.credit'],
            'reconcile': False,
            }
        line_2 = line_1.copy()
        line_2.update({
            'account_id': journal['default_debit_account_id'][0],
            'debit': item['line_id.credit'],
            'credit': item['line_id.debit'],
            })
        move.update({
            'line_id': [(0, 0, line_1), (0, 0, line_2)]
            })
        move_id = dbcomp.execute(
            'account.move', 'create', move)
        dbcomp.execute(
            'account.move', 'post', [move_id])
    p2o.done
