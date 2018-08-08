# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp


def load_tcv_bank_deposit(dbcomp, dbprofit):
    if not dbprofit:
        return
    p2o = profit_2_openerp('tcv.bank.deposit', dbcomp, dbprofit)
    p2o.set_sql(
        '''
select 'DEP '+RTRIM(dep_num) as ref, rtrim(deposito) as name, fecha as date,
       rtrim(cod_cta) as bank_journal_id,
       total_efec+total_cheq+total_tarj as check_total,
       case che_dev when 1 then 'CHEQUE DEVUELTO' ELSE '' end as narration
from dep_caj
where fecha >= '2017-01-01'
order by 1
        ''')
    p2o.set_search_fields(['ref'])
    p2o.set_relational_fields([
        ('bank_journal_id', 'account.journal', ['code']),
        ])
    p2o.process_csv()
