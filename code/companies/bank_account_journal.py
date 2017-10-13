# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp


def load_bank_account_journal(lnk, profit):
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
