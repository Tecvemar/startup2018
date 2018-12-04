# -*- encoding: utf-8 -*-
import sys
from profit2open import profit_2_openerp


def update_secuences(dbcomp, dbprofit):
    '''

    Set updated values in secuences

    '''
    p2o = profit_2_openerp('ir.sequence', dbcomp, dbprofit)
    p2o.set_sql(
        '''
        select 'Diario / Ventas Nacionales' as name,
               cast(max(number) as int ) + 1 as number_next
        from account_invoice
        where type = 'out_invoice'
        union
        select 'Withholding vat purchase' as name,
               cast(substring(max(number),10,8) as int) + 1 as number_next
        from account_wh_iva
        where type = 'in_invoice'
        ''')
    p2o.set_search_fields(['name'])
    p2o.set_integer_fields(['number_next'])
    p2o.update_records = True
    # ~ p2o.process_csv()
    p2o.test_data_file()
    p2o.done


