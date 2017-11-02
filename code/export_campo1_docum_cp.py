# -*- encoding: utf-8 -*-
from open_lnk import openerp_link
from profit_lnk import profit_link
from definitions import dbdata
from profit2open import profit_2_openerp


def export_purchase_data(dbcomp, dbprofit):
    '''
    '''
    p2o = profit_2_openerp('Export docum_cp campo1', dbcomp, dbprofit)
    p2o.set_sql(
        '''
select rtrim(c.tipo_doc) as tipo_doc, ltrim(str(c.nro_doc)) as nro_doc,
       rtrim(c.campo1) as campo1
from docum_cp c
where c.tipo_doc = 'FACT' and c.fec_emis >= '2017-01-01' and c.anulado = 0
      and c.nro_doc not in (select distinct fact_num from reng_com)
order by 1, 2
        ''')
    #~ p2o.test_data_file()
    p2o.load_data()
    file_name = '../data/companies/%s/docum_cp_campo1.csv' % dbcomp.database
    p2o.export_to_csv_file(file_name)


#~ for database in ['monagas']:
for database in dbdata['databases'][:6]:
    if dbdata[database]['profit']:
        lnk_dbprofit = profit_link(
            dbdata[database]['profit']['host'],
            dbdata[database]['profit']['db'],
            dbdata['profit_login'],
            dbdata['profit_password'])
    else:
        lnk_dbprofit = False

    lnk_dbcom = openerp_link(
        dbdata['host'],
        dbdata['rpc_port'],
        database,
        dbdata['openerp_login'],
        dbdata['openerp_password'])

    export_purchase_data(lnk_dbcom, lnk_dbprofit)
