# -*- encoding: utf-8 -*-
import os
from csv2open import csv_2_openerp
from profit2open import profit_2_openerp


def load_res_partner(lnk):
    # Update main partner data
    work_dir = '../data/companies/%s/' % lnk.database
    c2o = csv_2_openerp(
        work_dir + 'res_partner_1.csv', 'res.partner', lnk)
    c2o.set_search_fields(['id'])
    c2o.set_float_fields(['wh_iva_rate'])
    c2o.set_boolean_fields(['customer', 'supplier', 'islr_withholding_agent',
                            'spn', 'wh_iva_agent',
                            'group_wh_iva_doc', 'vat_subjected'])
    c2o.set_relational_fields([
        ('property_account_receivable', 'account.account', ['code']),
        ('property_account_payable', 'account.account', ['code']),
        ('property_account_advance', 'account.account', ['code']),
        ('property_account_prepaid', 'account.account', ['code']),
        ('property_stock_customer', 'stock.location', ['name']),
        ('property_stock_supplier', 'stock.location', ['name']),
        ])
    c2o.update_records = True
    c2o.process_csv()

    # Update common partners data (From common folder
    c2o = csv_2_openerp(
        '../data/common/res_partner.csv',  # Yes from common!
        'res.partner', lnk)
    c2o.set_search_fields(['vat'])
    c2o.set_float_fields(['wh_iva_rate'])
    c2o.set_boolean_fields(['customer', 'supplier', 'islr_withholding_agent',
                            'spn', 'wh_iva_agent',
                            'group_wh_iva_doc', 'vat_subjected'])
    c2o.set_relational_fields([
        ('property_account_receivable', 'account.account', ['code']),
        ('property_account_payable', 'account.account', ['code']),
        ('property_account_advance', 'account.account', ['code']),
        ('property_account_prepaid', 'account.account', ['code']),
        ('property_stock_customer', 'stock.location', ['name']),
        ('property_stock_supplier', 'stock.location', ['name']),
        ('address.country_id', 'res.country', ['code']),
        ('address.state_id', 'res.country.state', ['name']),
        ])
    c2o.set_child_model_fields(['address'])
    c2o.process_csv()


def load_res_partner_profit_pruchase(lnk, profit):
    if not profit:
        return
    p2o = profit_2_openerp('res.partner', lnk, profit)
    p2o.set_sql(
        '''
select rtrim(p.prov_des) as name, rtrim(p.rif) as vat,
       rtrim(p.co_prov) as ref, 'es_VE' as lang,
       't' as supplier, p.website, 'invoice' as "address.type",
       p.direc1 as "address.street1", p.direc2 as "address.street2",
       p.telefonos as  "address.phone", p.fax as  "address.fax",
       p.email as "address.email", p.ciudad as "address.city",
       p.zip as "address.zip", 't' as islr_withholding_agent,
       case p.contribu_e when 1 then 't' else 'f' end as wh_iva_agent,
       '1110299999' as property_account_receivable,
       '2120199999' as property_account_payable,
       '2180399999' as property_account_advance,
       '1110899999' as property_account_prepaid,
       'Customers' as property_stock_customer,
       'Suppliers' as property_stock_supplier,
       'VE' as "address.country_id"
from prov p
where p.co_prov in (
    select distinct co_cli from docum_cp
    where tipo_doc = 'FACT' and fec_emis >= '2017-01-01')
order by 3
        ''')
    p2o.set_search_fields(['vat'])
    p2o.set_boolean_fields(['supplier', 'islr_withholding_agent',
                            'wh_iva_agent'])
    p2o.set_relational_fields([
        ('property_account_receivable', 'account.account', ['code']),
        ('property_account_payable', 'account.account', ['code']),
        ('property_account_advance', 'account.account', ['code']),
        ('property_account_prepaid', 'account.account', ['code']),
        ('property_stock_customer', 'stock.location', ['name']),
        ('property_stock_supplier', 'stock.location', ['name']),
        ('address.country_id', 'res.country', ['code']),
        ])
    p2o.set_child_model_fields(['address'])
    p2o.set_vat_field = 'vat'
    p2o.process_csv()
    #~ p2o.test_data_file()


def load_res_partner_profit_sale(lnk, profit):
    if not profit:
        return
    p2o = profit_2_openerp('res.partner', lnk, profit)
    p2o.set_sql(
        '''
select rtrim(p.cli_des) as name, rtrim(p.rif) as vat,
       rtrim(p.co_cli) as ref, 'es_VE' as lang,
       't' as customer, p.website, 'invoice' as "address.type",
       p.direc1 as "address.street1", p.direc2 as "address.street2",
       p.telefonos as  "address.phone", p.fax as  "address.fax",
       p.email as "address.email", p.ciudad as "address.city",
       p.zip as "address.zip", 't' as islr_withholding_agent,
       case p.contribu_e when 1 then 't' else 'f' end as wh_iva_agent,
       '1110299999' as property_account_receivable,
       '2120199999' as property_account_payable,
       '2180399999' as property_account_advance,
       '1110899999' as property_account_prepaid,
       'Customers' as property_stock_customer,
       'Suppliers' as property_stock_supplier,
       'VE' as country_id
from clientes p
where p.co_cli in (
    select distinct co_cli from docum_cc
    where tipo_doc = 'FACT' and fec_emis >= '2017-01-01')
order by 3
        ''')
    p2o.set_search_fields(['vat'])
    p2o.set_boolean_fields(['customer', 'islr_withholding_agent',
                            'wh_iva_agent'])
    p2o.set_relational_fields([
        ('property_account_receivable', 'account.account', ['code']),
        ('property_account_payable', 'account.account', ['code']),
        ('property_account_advance', 'account.account', ['code']),
        ('property_account_prepaid', 'account.account', ['code']),
        ('property_stock_customer', 'stock.location', ['name']),
        ('property_stock_supplier', 'stock.location', ['name']),
        ('country_id', 'res.country', ['code']),
        ])
    p2o.set_child_model_fields(['address'])
    p2o.set_vat_field = 'vat'
    p2o.process_csv()
    #~ p2o.test_data_file()


def load_res_partner_companies_extra_data(lnk):
    # Update special data from companie's data folder
    work_dir = '../data/companies/%s/' % lnk.database
    work_csv = work_dir + 'res_partner.csv'
    if not os.path.isfile(work_csv):
        return
    c2o = csv_2_openerp(work_csv, 'res.partner', lnk)
    c2o.set_search_fields(['vat'])
    c2o.set_boolean_fields(['customer', 'supplier'])
    c2o.update_records = True
    c2o.process_csv()
