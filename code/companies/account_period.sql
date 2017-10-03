select date_start, date_stop, substring(code, 5,12) as code, 
       'Mes ' || substring(code, 5,12) as name , 'draft' as state, special 
from account_period where fiscalyear_id = 19
union
select '2017-01-01' as date_start, '2017-01-01' as date_stop, 'Apertura 2017' as code, 
       'Período de apertura 2017' as name , 'draft' as state, True as special 
from account_period where id = 1
union
select '2017-12-31' as date_start, '2017-12-31' as date_stop, 'Cierre 2017' as code, 
       'Período de cierre 2017' as name , 'draft' as state, True as special 
from account_period where id = 1
order by date_stop, date_start