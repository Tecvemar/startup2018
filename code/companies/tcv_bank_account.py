# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp


def load_tcv_bank_account(dbcomp, dbprofit):

    load_journal(dbcomp, dbprofit)
    if not dbprofit:
        return
    p2o = profit_2_openerp('tcv.bank.account', dbcomp, dbprofit)
    p2o.set_sql(
        '''
select    'bank' as type, c.num_cta as name,
         rtrim(c.cod_cta)  as journal_id, rtrim(co_banco)  as bank_id,
         23 as user_type, 't' as Active, 'f' as reconcile,
         1 as company_id, 'Cuenta bancaria migrada de Profit'
         as note
from cuentas c
left join bancos b on c.co_banco = b.co_ban
where c.co_banco != '0121'
            ''')
    p2o.load_data()
    print p2o.data[0]
    p2o.set_search_fields(['name'])
    p2o.set_relational_fields(
        [('bank_id', 'tcv.bank.list', ['code']),
         ('journal_id', 'account.journal', ['code'])])
    p2o.process_csv()


def load_journal(dbcomp, dbprofit):

    if not dbprofit:
        return
    p2o = profit_2_openerp('tcv.bank.account', dbcomp, dbprofit)
    p2o.set_sql(
        '''
select   1 as view_id, c.cod_cta as code, '[' + rtrim(c.cod_cta) + ']'
         + rtrim(des_ban) + ' ' + 'Cta:' + ' ' + num_cta
         as name, 'bank' as type, c.campo2 as bank_id,
         c.campo3  as journal_id,
         23 as user_type, 't' as Active, 'f' as reconcile,
         1 as company_id, 'Cuenta bancaria migrada de Profit'
         as note
from cuentas c
left join bancos b on c.co_banco = b.co_ban
where c.co_banco != '0121'
            ''')
    p2o.load_data()
    acc_jou = p2o.data
    for journal in acc_jou:
        dbcomp.execute('account.journal', 'create', journal)
