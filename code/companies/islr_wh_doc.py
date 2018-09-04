# -*- encoding: utf-8 -*-
#~ import sys
from profit2open import profit_2_openerp


__islr_wh_concepts__ = {
    '1002': 2, '1005': 12, '1006': 3, '1020': 4, '1021': 25, '1022': 25,
    '1023': 26, '1025': 5, '1029': 32, '1030': 6,
    }


def load_islr_wh_doc(dbcomp, dbprofit):
    '''

    Charge whitholdings ISLR
    Let OpenERP assign wh numbres!
    '''
    p2o = profit_2_openerp('islr.wh.doc', dbcomp, dbprofit)
    p2o.set_sql(
        '''
        Select i.co_islr, 'FACT-' + cast(i.fact_num as varchar) as code,
               fec_cob as date_ret,
               p.fec_cob as date_uid, i.monto_obj, i.monto_reten, i.sustraen,
               i.porc_retn, p.cob_num, p.co_cli, d.nro_fact,
               rtrim(d.co_cli) as partner_id,
               CAST(year(p.fec_cob) as varchar) + '-' +
               right(CAST(month(p.fec_cob) + 100 as varchar), 2) + '-' +
               p.descrip as name
        from reng_pag r
        left join pagos p on r.cob_num = p.cob_num
        left join reng_isl i on i.doc_num = p.cob_num
        left join docum_cp d on d.tipo_doc='FACT' and d.nro_doc = i.fact_num
        where r.tp_doc_cob= 'ISLR' and p.fec_cob > '2017-01-01' and
              d.fec_emis > '2017-01-01' and p.anulado = 0
        order by p.fec_cob, p.cob_num
        ''')
    p2o.set_relational_fields([
        ('partner_id', 'res.partner', ['ref']),
        ])
    p2o.load_data()
    for ret in p2o.data:
        p2o.show_wait()
        ret['concept_id'] = __islr_wh_concepts__[ret['co_islr']]
        invoice_id = dbcomp.execute(
            'account.invoice', 'search',
            [('supplier_invoice_number', '=', ret['nro_fact']),
             ('partner_id', '=', ret['partner_id'])])
        ret['invoice_id'] = invoice_id and len(invoice_id) == 1 and \
            invoice_id[0]
        inv_line_ids = dbcomp.execute(
            'account.invoice.line', 'search',
            [('invoice_id', '=', invoice_id)])
        inv_lines = dbcomp.execute(
            'account.invoice.line', 'read', inv_line_ids, [])
        if ret['monto_obj'] != inv_lines[0]['price_subtotal']:
            split_invoice_line(dbcomp, ret, inv_lines)
        create_islr_doc(dbcomp, ret, inv_lines)
    p2o.done


def split_invoice_line(dbcomp, ret, inv_lines):
    ivl = False
    if len(inv_lines) != 1:
        maxmnt = 0
        for line in inv_lines:
            if line['price_subtotal'] > maxmnt:
                ivl = line
                maxmnt = line['price_subtotal']
        print '\n',ret
        print 'split_invoice_line: More than 1 line to split using', ivl
    else:
        ivl = inv_lines[0]
    if not ivl:
         raise ValueError('split_invoice_line: No lines to split')
    amount = ret['monto_obj']
    amount_diff = ivl['price_subtotal'] - amount
    sql = '''
    insert into account_invoice_line (
           create_uid, create_date, write_date, write_uid,
           origin, uos_id, account_id, name, invoice_id, price_unit,
           price_subtotal, company_id, note, discount,
           account_analytic_id, partner_id, product_id,
           concept_id, apply_wh, wh_xml_id,
           pieces, prod_lot_id, quantity)
    select create_uid, create_date, write_date, write_uid,
           origin, uos_id, account_id, name, invoice_id, price_unit,
           price_subtotal, company_id, note, discount,
           account_analytic_id, partner_id, product_id,
           concept_id, apply_wh, wh_xml_id,
           pieces, prod_lot_id, quantity
    from account_invoice_line where id = %(id)s
    '''
    dbcomp.execute_sql(sql, {'id': ivl['id']})
    new_line_ids = dbcomp.execute(
        'account.invoice.line', 'search',
        [('invoice_id', '=', ivl['invoice_id'][0])])
    upd_sql = '''
        update account_invoice_line set
        price_unit = %(new_price)s,
        price_subtotal = %(new_price)s
        where id = %(id)s
        '''
    for new_id in new_line_ids:
        params = {'id': new_id,
                  'new_price': (amount if new_id == ivl['id'] else
                                amount_diff)}
        dbcomp.execute_sql(upd_sql, params)


def create_islr_doc(dbcomp, ret, inv_lines):
    ivl = inv_lines[0]
    data = {'invoice_line_id': ivl['id'],
            'concept_id': ret['concept_id'],
            'withholdable_islr': True}
    dbcomp.execute(
        'account.invoice.line', 'write', ivl['id'], data)
    ret_id = dbcomp.execute(
        'account.invoice', 'create_islr_wh_doc', ivl['invoice_id'][0], {})
    dbcomp.execute(
        'islr.wh.doc', 'write', [ret_id], {
            'name': ret['name'] or u'Retención ISLR (Migración)',
            'date_ret': ret['date_ret'],
            'date_uid': ret['date_uid'],
            'code': ret['code'],
            'period_id': dbcomp.execute(
                'account.period', 'find', ret['date_uid'])[0]
            })
    dbcomp.execute_workflow(
        'islr.wh.doc', 'act_confirm', ret_id)
    dbcomp.execute_workflow(
        'islr.wh.doc', 'act_done', ret_id)
