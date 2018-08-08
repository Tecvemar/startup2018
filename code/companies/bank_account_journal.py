# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp
from profit2open import profit_2_openerp


def load_bank_account_journal(lnk, profit):
    #  Account.account --------------------------------------------------------
    if not profit:
        return
    p2o = profit_2_openerp('account.account', lnk, profit)
    p2o.set_sql(
        '''
select rtrim(b.des_ban) + ' - ' + rtrim(c.num_cta) as name,
       convert(varchar(10),
           1100300000 + ROW_NUMBER() OVER(ORDER BY b.fe_us_in)) as code,
       '11003' as parent_id, 'liquidity' as type, 'Efectivo' as user_type,
       1 as company_id
from cuentas c
left join bancos b on c.co_banco = b.co_ban
where c.moneda = 'BS'
union
select rtrim(b.des_ban) + ' - ' + rtrim(c.num_cta) as name,
       convert(varchar(10),
           1100400000 + ROW_NUMBER() OVER(ORDER BY b.fe_us_in)) as code,
       '11004' as parent_id, 'liquidity' as type, 'Efectivo' as user_type,
       1 as company_id
from cuentas c
left join bancos b on c.co_banco = b.co_ban
where c.moneda != 'BS'

        ''')
    p2o.set_search_fields(['code'])
    p2o.set_relational_fields(
        [('parent_id', 'account.account', ['code']),
         ('user_type', 'account.account.type', ['name'])])
    p2o.process_csv()

    #  Account.journal --------------------------------------------------------
    p2o = profit_2_openerp('account.journal', lnk, profit)
    p2o.set_sql(
        '''
select '['+rtrim(c.cod_cta)+'] '+rtrim(b.des_ban) + ' - ' + rtrim(c.num_cta) as
           name,
       rtrim(c.cod_cta) as code, 'bank' as type, 2 as view_id,
       'VEB' as currency_id,
       convert(varchar(10),
           1100300000 + ROW_NUMBER() OVER(ORDER BY b.fe_us_in)) as
           default_debit_account_id,
       convert(varchar(10),
           1100300000 + ROW_NUMBER() OVER(ORDER BY b.fe_us_in)) as
           default_credit_account_id,
       0 as user_id, 1 as company_id, 'f' as allow_date, 't' as update_posted
from cuentas c
left join bancos b on c.co_banco = b.co_ban
where c.moneda = 'BS'
union
select '['+rtrim(c.cod_cta)+'] '+rtrim(b.des_ban) + ' - ' + rtrim(c.num_cta) as
           name,
       rtrim(c.cod_cta) as code, 'bank' as type, 2 as view_id,
       '' as curency_id,
       convert(varchar(10),
           1100400000 + ROW_NUMBER() OVER(ORDER BY b.fe_us_in)) as
           default_debit_account_id,
       convert(varchar(10),
           1100400000 + ROW_NUMBER() OVER(ORDER BY b.fe_us_in)) as
           default_credit_account_id,
       0 as user_id, 1 as company_id, 'f' as allow_date, 't' as update_posted
from cuentas c
left join bancos b on c.co_banco = b.co_ban
where c.moneda != 'BS'
        ''')
    p2o.set_search_fields(['code'])
    p2o.set_relational_fields([
        ('default_debit_account_id', 'account.account', ['code']),
        ('default_credit_account_id', 'account.account', ['code']),
        ('currency_id', 'res.currency', ['name']),
        ])
    p2o.process_csv()
    # force allow_date to false
    journal_ids = lnk.execute(
        'account.journal', 'search', [('type', '=', 'bank')])
    lnk.execute(
        'account.journal', 'write', journal_ids, {'allow_date': False})

    #  tcv.bank.account -------------------------------------------------------
    work_dir = '../data/companies/%s/' % lnk.database
    c2o = csv_2_openerp(
        work_dir + 'tcv_bank_account.csv', 'tcv.bank.account', lnk)
    c2o.set_search_fields(['name'])
    c2o.set_relational_fields([
        ('bank_id', 'tcv.bank.list', ['name']),
        ('journal_id', 'account.journal', ['code']),
        ])
    c2o.process_csv()
