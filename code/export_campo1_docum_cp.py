# -*- encoding: utf-8 -*-
from open_lnk import openerp_link
from profit_lnk import profit_link
from definitions import dbdata
from profit2open import profit_2_openerp


def export_purchase_data(dbcomp, dbprofit):
    '''
--select rtrim(c.tipo_doc) as tipo_doc, ltrim(str(c.nro_doc)) as nro_doc,
--       rtrim(c.campo1) as campo1
    '''
    p2o = profit_2_openerp('Export docum_cp campo1', dbcomp, dbprofit)
    key = '--update_str_%s' % dbprofit.database
    p2o.set_sql(
        '''
select 'update docum_cp set campo1 = |' + rtrim(c.campo1) +
       '| where tipo_doc = |FACT| and nro_doc = ' +
       cast(nro_doc as varchar) + ';' as '%s'
from docum_cp c
where c.tipo_doc = 'FACT' and c.fec_emis >= '2017-01-01' and c.anulado = 0
      and c.nro_doc not in (select distinct fact_num from reng_com)
      order by c.nro_doc
        ''' % key)
    #~ p2o.test_data_file()
    p2o.load_data()
    for l in p2o.data:
        l[key] = l[key].replace('|', "'")
    file_name = '../data/companies/%s/docum_cp_campo1.sql' % dbcomp.database
    p2o.export_to_csv_file(file_name)


def export_payment_orders_data(dbcomp, dbprofit):
    '''
    '''
    p2o = profit_2_openerp('Export ord_pago campo1', dbcomp, dbprofit)
    key = '--update_str_%s' % dbprofit.database
    p2o.set_sql(
        '''
select 'update ord_pago set campo1 = |' + rtrim(op.campo1) +
       '| where ord_num = ' +
       cast(ord_num as varchar) + ';' as '%s'
from ord_pago op
where op.fecha >= '2017-01-01' and op.anulada = 0
order by op.ord_num
        ''' % key)
    #~ p2o.test_data_file()
    p2o.load_data()
    for l in p2o.data:
        l[key] = l[key].replace('|', "'")
    file_name = '../data/companies/%s/ord_pago_campo1.sql' % dbcomp.database
    p2o.export_to_csv_file(file_name)


for database in dbdata['databases']:
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
    export_payment_orders_data(lnk_dbcom, lnk_dbprofit)
