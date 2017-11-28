# -*- encoding: utf-8 -*-
import sys
from profit2open import profit_2_openerp


def load_account_wh_iva(dbcomp, dbprofit):
    '''

    Charge whitholdings IVA

    '''
    fixed_wh_numbers = []
    p2o = profit_2_openerp('account.wh.iva', dbcomp, dbprofit)
    p2o.set_sql(
        '''
        SELECT a.tipo_doc +'-'+cast(a.nro_doc as varchar) as code,
            isnull(b.fec_emis,getdate()) as date,a.fec_emis as date_ret,
            year(a.fec_emis) as y, MONTH(a.fec_emis) as m,
            rtrim(cast(year(a.fec_emis) as varchar) + '-' +
            right(100 + month(a.fec_emis), 2) + '-' + a.nro_che) as number,
            ltrim(rtrim(a.co_cli)) as partner_id, a.observa as name,
            case when rtrim(B.n_control)= '' then left(a.campo7,20) else
            B.n_control end as nro_ctrl, a.co_sucu,a.nro_orig,a.doc_orig,
            a.aut,a.moneda,a.monto_net, a.campo8,a.anulado,
            b.dis_cen as inf_iva,b.monto_net as net_iva,
            ltrim(rtrim(b.nro_fact))  as invoice_id ,ltrim(rtrim(b.nro_fact))
            as supplier_invoice_number , b.nro_fact as donde,
            b.doc_orig as fac_orig, b.nro_fact as nfacori,
            cast(round((a.monto_net / b.monto_imp) *100, 0) as Int)
            as pct_ret, 'in_invoice' as type
        FROM docum_cp a
            left join docum_cp b on A.nro_orig = B.nro_doc and
                                    A.doc_orig = B.tipo_doc
        WHERE ltrim(rtrim(a.campo8))='IVA' and a.anulado=0 and
            a.fec_emis > '01/01/2017' and b.fec_emis > '01/01/2017' and
            (a.tipo_doc= 'AJPM' or a.tipo_doc= 'AJNM') and
            b.nro_orig =0 and b.doc_orig =''
        ''')
    p2o.set_search_fields(['number'])
    p2o.set_relational_fields([
        ('partner_id', 'res.partner', ['ref']),
        ])
    p2o.load_data()
    for ret in p2o.data:
        partner = dbcomp.execute(
            'res.partner', 'read', ret['partner_id'], [])
        ret['account_id'] = partner['property_account_payable'][0]
        wh_id = p2o.write_data_row(ret)
        if wh_id:
            fixed_wh_numbers.append({
                'wh_id': wh_id,
                'number': ret['number'],
                'fixed': '%04d%02d%s' % (ret['y'], ret['m'], ret['number']),
                })
    p2o.done
    print
    load_account_wh_iva_line(dbcomp, dbprofit)
    print
    #  Postprocess wh_iva
    msg = '  Postprocesando: account.wh.iva.'
    print msg + '\r',
    sys.stdout.flush()
    if fixed_wh_numbers:
        retention_ids = list(set([x['wh_id'] for x in fixed_wh_numbers]))
        dbcomp.execute(
            'account.wh.iva', 'compute_amount_wh', retention_ids)
        for ret_id in retention_ids:
            dbcomp.execute_workflow(
                'account.wh.iva', 'wh_iva_confirmed', ret_id)
            dbcomp.execute_workflow(
                'account.wh.iva', 'wh_iva_done', ret_id)
    print msg + ' Listo.' + ' ' * 40


def load_account_wh_iva_line(dbcomp, dbprofit):
    p2o = profit_2_openerp('account.wh.iva.line', dbcomp, dbprofit)
    p2o.set_sql(
        '''
SELECT rtrim(cast(year(a.fec_emis) as varchar) + '-' +
       right(100 + month(a.fec_emis), 2) + '-' + a.nro_che) as retention_id,
       a.observa as name, ltrim(rtrim(b.nro_fact)) as invoice_id,
       ltrim(rtrim(b.nro_fact)) as nro_fact,
       ltrim(rtrim(a.co_cli)) as partner_id,
       cast(round((a.monto_net / b.monto_imp) *100, 0) as Int) as pct_ret
FROM docum_cp a
     left join docum_cp b on A.nro_orig = B.nro_doc and
     A.doc_orig = B.tipo_doc
WHERE ltrim(rtrim(a.campo8))='IVA' and a.anulado=0 and
      a.fec_emis > '01/01/2017' and b.fec_emis > '01/01/2017' and
      (a.tipo_doc= 'AJPM' or a.tipo_doc= 'AJNM') and
      b.nro_orig =0 and b.doc_orig =''
        ''')
    p2o.set_search_fields(['invoice_id'])
    p2o.set_relational_fields([
        ('partner_id', 'res.partner', ['ref']),
        ('invoice_id', 'account.invoice', ['supplier_invoice_number']),
        ('retention_id', 'account.wh.iva', ['number']),
        ])
    p2o.load_data()
    for line in p2o.data:
        if not line['invoice_id']:
            invoice_id = dbcomp.execute(
                'account.invoice', 'search',
                [('supplier_invoice_number', '=', line['nro_fact']),
                 ('partner_id', '=', line['partner_id'])])
            if invoice_id and len(invoice_id) == 1:
                line['invoice_id'] = invoice_id[0]
        dbcomp.execute(
            'res.partner', 'write', [line['partner_id']],
            {'wh_iva_rate': line['pct_ret']})
        p2o.write_data_row(line)
    p2o.done
