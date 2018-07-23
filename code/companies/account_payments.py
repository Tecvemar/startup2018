# -*- encoding: utf-8 -*-
import os
import sys
from csv2open import csv_2_openerp
from profit2open import profit_2_openerp


def load_account_voucher_purchase(dbcomp, dbprofit):
    '''

    Process & export payments

    '''
    p2o = profit_2_openerp('account.voucher', dbcomp, dbprofit)
    p2o.set_sql(
        '''
select rtrim(pg.co_cli) as partner_id, rd.mont_doc as amount,
       case rtrim(rd.cod_caja) when '002' then 'DCHI'
                               when '001' then 'DCEF'
                               when '999' then '9999'
                               else rtrim(rd.cod_caja) end as journal_id,
       pg.fec_cob as date, 'payment' as type, tip_cob, pg.cob_num,
       'COB '+cast(pg.cob_num as varchar) as name,
       rtrim(descrip) as narration,
       rtrim(tip_cob)+' '+rtrim(num_doc) as reference,
       case rtrim(rd.cod_caja) when '002' then 'cash'
                       when '001' then 'cash'
                       when '999' then 'cash'
                       else 'transfer' end as payment_doc
from pagos pg
left join reng_tcp rd on pg.cob_num = rd.cob_num
where pg.fec_cob >= '2017-01-01' and pg.anulado = 0 --and pg.monto != 0
order by pg.fec_cob, pg.cob_num
        ''')
    p2o.set_search_fields(['name', 'amount'])
    p2o.set_relational_fields([
        ('partner_id', 'res.partner', ['ref']),
        ('journal_id', 'account.journal', ['code']),
        ])
    p2o.load_data()
    for vou in p2o.data:
        partner = dbcomp.execute(
            'res.partner', 'read', vou['partner_id'], [])
        if not vou['reference']:
            vou['reference'] = '%s' % vou['cob_num']
        vou['account_id'] = partner['property_account_payable'][0]
        vou['id'] = p2o.write_data_row(vou) or 0
    p2o.done


def postprocess_acc_voucher_purchase(dbcomp, dbprofit):
    '''
    {u'ADEL_FACT': 12, u'ADEL_ADEL_FACT': 2, u'FACT_AJPA': 2,
     u'FACT_FACT': 1, u'FACT_AJNA': 1, u'FACT_AJNM': 50,
     u'ADEL_AJNM_FACT': 1, u'ADEL_FACT_N/DB': 1, u'FACT_AJNM_ISLR': 1,
     u'FACT_ISLR_AJNM': 43, u'ADEL': 24, u'FACT_ISLR': 7, u'FACT': 69}
    '''
    msg = '  Postprocesando: account.voucher (Purchases)'
    voucher_ids = dbcomp.execute(
        'account.voucher', 'search', [('type', '=', 'payment')])
    vouchers = sorted(
        dbcomp.execute('account.voucher', 'read', voucher_ids, [],),
        key=lambda k: k['name'])
    # ~ res = {}
    for voucher in vouchers:
        print msg + ' ' + voucher['name'] + ' ' * 40 + '\r',
        sys.stdout.flush()
        data = {'cob_num': voucher['name'].split()[1]}
        p2o = profit_2_openerp('account.voucher', dbcomp, dbprofit)
        p2o.set_sql(
            '''
select rtrim(pg.co_cli) as partner_id, pg.monto as amount,
       pg.fec_cob as date, pg.cob_num, rtrim(descrip) as narration,
       rd.tp_doc_cob, rd.doc_num, rd.nro_fact, rd.neto,
       'COB '+cast(pg.cob_num as varchar) as name,
       0 as invoice_id, 0 as move_line_id
from pagos pg
left join reng_pag rd on pg.cob_num = rd.cob_num
where pg.cob_num = %(cob_num)s
order by rd.reng_num
        ''' % data)
        p2o.update_records = True
        p2o.set_search_fields(['name'])
        p2o.set_relational_fields([
            ('partner_id', 'res.partner', ['ref']),
            ('invoice_id', 'account.invoice', ['supplier_invoice_number']),
            ])
        p2o.set_child_model_fields(['line_ids'])
        p2o.load_data()
        for line in p2o.data:
            if line['nro_fact'] and line['tp_doc_cob'] == 'FACT':
                invoice_id = dbcomp.execute(
                    'account.invoice', 'search',
                    [('supplier_invoice_number', '=', line['nro_fact']),
                     ('partner_id', '=', line['partner_id'])])
                if invoice_id and len(invoice_id) == 1:
                    line['invoice_id'] = invoice_id[0]
                    line.update(get_move_line_id(
                        dbcomp, dbprofit, line))
                    values = {
                        'name': line['name'],
                        'line_ids': [(0, 0, {
                            'move_line_id': line['move_line_id'],
                            'account_id': line['account_id'],
                            'type': 'dr',
                            'amount': line['amount'],
                            'name': line['invoice_name'],
                        })]}
                    p2o.write_data_row(values)
        op_key = '_'.join((x['tp_doc_cob'] for x in p2o.data))
        if op_key == 'ADEL':
            values = {
                'name': line['name'],
                'voucher_type': 'advance',
                }
            p2o.write_data_row(values)
        if op_key in ('ADEL', 'FACT', 'FACT_ISLR_AJNM') and voucher['amount']:
            dbcomp.execute_workflow(
                'account.voucher', 'proforma_voucher', voucher['id'])


def postprocess_acc_voucher_purchase_manual(dbcomp, dbprofit):
    # ~ Postprocess manual payments
    work_dir = '../data/companies/%s/' % dbcomp.database
    work_csv = work_dir + 'account_voucher_purchase_manual.csv'
    if not os.path.isfile(work_csv):
        return
    c2o = csv_2_openerp(work_csv, 'account.voucher', dbcomp)
    c2o.load_data()
    for item in c2o.data:
        voucher_id = dbcomp.execute(
            'account.voucher', 'search', [
                ('name', '=', item['name'])])
        voucher = dbcomp.execute(
            'account.voucher', 'read', voucher_id[0], ['state'])
        if item['state'] == 'aprovee' and voucher['state'] == 'draft':
            dbcomp.execute_workflow(
                'account.voucher', 'proforma_voucher', voucher_id[0])
        elif item['state'] == 'cancel' and voucher['state'] == 'draft':
            dbcomp.execute_workflow(
                'account.voucher', 'cancel_voucher', voucher_id[0])
    c2o.done()

def get_move_line_id(dbcomp, dbprofit, line):
    invoice_id = line['invoice_id']
    invoice = dbcomp.execute(
        'account.invoice', 'read', invoice_id, [])
    move_line_id = dbcomp.execute(
        'account.move.line', 'search', [
            ('move_id', '=', invoice['move_id'][0]),
            ('account_id', '=', invoice['account_id'][0]),
            ])

    return {
        'move_line_id': move_line_id[0],
        'account_id': invoice['account_id'][0],
        'invoice_name': invoice['comment'],
        }


# Sales -----------------------------------------------------------------------


def load_account_voucher_sale(dbcomp, dbprofit):
    '''

    Process & export payments

    '''
    p2o = profit_2_openerp('account.voucher', dbcomp, dbprofit)
    p2o.set_sql(
        '''
select rtrim(pg.co_cli) as partner_id, rd.mont_doc as amount,
       case rtrim(rd.cod_caja) when '002' then 'DCHI'
                               when '001' then 'DCEF'
                               when '005' then 'DTDEB01'
                               when '007' then 'DTDEB01'
                               when '999' then '9999'

                               else rtrim(rd.cod_caja) end as journal_id,
       pg.fec_cob as date, 'receipt' as type, tip_cob, pg.cob_num,
       'PAG '+cast(pg.cob_num as varchar) as name,
       rtrim(descrip) as narration,
       rtrim(tip_cob)+' '+rtrim(num_doc) as reference,
       rd.cod_caja
from cobros pg
left join reng_tip rd on pg.cob_num = rd.cob_num
where pg.fec_cob >= '2017-01-01' and pg.anulado = 0 --and pg.monto != 0
order by pg.fec_cob, pg.cob_num
        ''')
    p2o.set_search_fields(['name', 'amount'])
    p2o.set_relational_fields([
        ('partner_id', 'res.partner', ['ref']),
        ('journal_id', 'account.journal', ['code']),
        ])
    p2o.load_data()
    for vou in p2o.data:
        partner = dbcomp.execute(
            'res.partner', 'read', vou['partner_id'], [])
        if not vou['reference']:
            vou['reference'] = '%s' % vou['cob_num']
        vou['account_id'] = partner['property_account_payable'][0]
        vou['id'] = p2o.write_data_row(vou) or 0
    p2o.done
