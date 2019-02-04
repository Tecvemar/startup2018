# -*- encoding: utf-8 -*-
from profit2open import profit_2_openerp


def load_bank_moves(dbcomp, dbprofit):
    if not dbprofit:
        return
    p2o = profit_2_openerp('account.move', dbcomp, dbprofit)
    p2o.set_sql(
        '''
select 'MB '+lTRIM(STR(mov_num))+ ' - '+tipo_op+' '+doc_num as ref,
    rtrim(codigo) as journal_id, fecha as date, '0' as to_check,
    LTRIM(STR(YEAR(fecha)))+'-'+right(STR(100+MONTH(fecha)),2) as period_id,
    1 as company_id, 'draft' as 'state', descrip as narration,
    1 as 'line_id.company_id',
    case cta_egre
    -- Ajustar en cada acropolis segun corresponda
    -- ver query: load_bank_moves.sql
--  Falcon
--        when '01501' then '5212025030' -- INVENTARIO DE MATERIA PRIMA
--        when '11404' then '1110799999' -- PRESTAMOS A EMPLEADOS
--        when '21501' then '1110599999' -- DIRECTORES Y ACCIONISTAS POR PAGAR
--        when '51201' then '7220100100' -- REMUNERACIONES DIRECTOS
--        when '521001' then '7220100150' -- BONIFICACIONES AL PERSONAL
--        when '61405' then '7220100260' -- I.N.C.E. POR ENTERAR
--        when '71301' then '7310200005' -- IMPUESTOS A LAS TRANSACCIONES FINANCIERAS
--        when '91130' then '7230300002' -- COMISIONES BANCARIAS
--        when 'NO' then '7230700025' -- NO CONFIGURADO
--  Monagas
--        when '10001' then '7230700025' -- C X C. ARBELO JESUS
--        when '11001' then '7230700025' -- C X C. BARRIOS NAVAS
--        when '11002' then '7230700025' -- CAJAS VARIAS Y TRANSFERENCIAS
--        when '11320' then '7230700025' -- CUENTAS POR COBRAR CLIENTES
--        when '22103' then '7230700025' -- CUENTAS DE AFILIACION
--        when '71301' then '7310200005' -- IMPUESTOS A LAS TRANSACCIONES FINANCIERAS
--        when '91110' then '7230700025' -- EGRESOS VARIOS
--        when '91130' then '7230300002' -- COMISIONES BANCARIAS
--        end as 'line_id.account_id',
--  Barquisimeto
        when '01501' then '7230700025' -- INVENTARIO DE MATERIA PRIMA
        when '11002' then '7230700025' -- CAJAS VARIAS Y TRANSFERENCIAS
        when '11320' then '7230700025' -- CUENTAS POR COBRAR CLIENTES
        when '11620' then '7230700025' -- ANTICIPOS A PROVEEDORES
        when '13402' then '7230700025' -- PATENTE
        when '21201' then '7230700025' -- CUENTAS POR PAGAR COMERCIALES
        when '21409' then '7230700025' -- OTRAS CUENTAS POR PAGAR
        when '51312' then '7230700025' -- ALQUILERES
        when '51606' then '7230700025' -- RETENCIONES FIEL CUPLIMIENTO
        when '61302' then '7230300002' -- COMISIONES Y GASTOS BANCARIOS
        when '61401' then '7230700025' -- ISLR POR ENTERAR
        when '61403' then '7230700025' -- L.P.H. POR ENTERAR
        when '61405' then '7220100260' -- I.N.C.E. POR ENTERAR
        when '61412' then '7230700025' -- IVA RETENIDO POR ENTERAR
        when '621071' then '7230700025' -- SEGURIDAD INDUSTRIAL
        when '661408' then '7230700025' -- DECLARACION DE RENTAS DEFINITIVAS
        when '71301' then '7310200005' -- IMPUESTOS A LAS TRANSACCIONES FINANCIERAS
        when '71302' then '7230300002' -- COMISIONES Y GASTOS BANCARIOS
        when '721074' then '7220100100' -- DIETAS DIRECTORES Y ACCIONISTAS
        when '81140' then '7230700025' -- REINTEGROS
        when '91130' then '7230300002' -- COMISIONES BANCARIAS
        when 'ISLRXP' then '7230700025' -- ISLR POR PAGAR
        end as 'line_id.account_id',
    monto_d+idb as 'line_id.debit',
    monto_h as 'line_id.credit',
    '0' as 'line_id.reconcile'
from mov_ban
where origen = 'BAN' and fecha > '2017-01-01' and anulado = 0
order by fecha, mov_num
        ''')
    p2o.set_search_fields(['ref'])
    p2o.set_relational_fields([
        ('line_id.account_id', 'account.account', ['code']),
        ('journal_id', 'account.journal', ['code']),
        ('period_id', 'account.period', ['code']),
        ])
    p2o.load_data()
    for item in p2o.data:
        p2o.show_wait()
        journal = dbcomp.execute(
            'account.journal', 'read', item['journal_id'],
            ['default_debit_account_id'])
        move = {x: item[x] for x in (
            'ref', 'journal_id', 'date', 'company_id', 'state',
            'to_check', 'narration', 'period_id')}
        line_1 = {
            'auto': True,
            'company_id': item['company_id'],
            'account_id': item['line_id.account_id'],
            'name': item['narration'],
            'debit': item['line_id.debit'],
            'credit': item['line_id.credit'],
            'reconcile': False,
            }
        line_2 = line_1.copy()
        line_2.update({
            'account_id': journal['default_debit_account_id'][0],
            'debit': item['line_id.credit'],
            'credit': item['line_id.debit'],
            })
        move.update({
            'line_id': [(0, 0, line_1), (0, 0, line_2)]
            })
        move_id = dbcomp.execute(
            'account.move', 'create', move)
        dbcomp.execute(
            'account.move', 'post', [move_id])
    p2o.done
