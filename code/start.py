#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from definitions import dbdata

MODULES = 'base'
ACTION = 'drop-db'
print ACTION, dbdata['dbgen']
os.system('python oerp_ws.py '
            + '--root-path=%s ' % dbdata['server_path']
            + '--addons-path=%s ' % dbdata['addons_path']
            + '--database=%s ' % dbdata['dbgen']
            + '--password=%s ' % dbdata['openerp_password']
            + '--login=%s ' % dbdata['openerp_login']
            + '--modules=%s ' % MODULES
            + ' %s ' % ACTION
            )

MODULES =       'base'
ACTION =        'create-db'
print ACTION

os.system('python oerp_ws.py '
            + '--root-path=%s ' % dbdata['server_path']
            + '--addons-path=%s ' % dbdata['addons_path']
            + '--database=%s ' % dbdata['dbgen']
            + '--password=%s ' % dbdata['openerp_password']
            + '--login=%s ' % dbdata['openerp_login']
            + '--modules=%s ' % MODULES
            + ' %s ' % ACTION
            )

module_list = [
    'account',
    'account_accountant',
    'account_anglo_saxon',
    'account_cancel',
    'account_chart',
    #~ 'account_financial_report',
    'account_followup',
    'account_payment',
    'account_smart_unreconcile',
    'account_voucher',
    'analytic',
    'base',
    'base_action_rule',
    'base_calendar',
    'base_module_record',
    'base_report_creator',
    'base_report_designer',
    'base_setup',
    'base_vat',
    'board',
    'decimal_precision',
    'document',
    'document_ftp',
    #~ 'l10n_ve_account_financial_report',
    'l10n_ve_fiscal_book',
    'l10n_ve_fiscal_requirements',
    'l10n_ve_imex',
    'l10n_ve_sale_purchase',
    'l10n_ve_split_invoice',
    'l10n_ve_withholding',
    'l10n_ve_withholding_islr',
    'l10n_ve_withholding_iva',
    'product',
    'purchase',
    'sale',
    'stock',
    'tcv_account',
    'tcv_account_management',
    #~ 'tcv_account_sync',
    'tcv_account_voucher',
    'tcv_account_voucher_extra_wkf',
    'tcv_advance',
    'tcv_bank_deposit',
    'tcv_base_bank',
    'tcv_bounced_cheq',
    'tcv_calculator',
    'tcv_check_voucher',
    'tcv_fiscal_report',
    #~ 'tcv_hr',
    'tcv_igtf',
    #~ 'tcv_import_management',
    #~ 'tcv_legal_matters',
    'tcv_misc',
    'tcv_monthly_report',
    'tcv_municipal_tax',
    'tcv_payroll_import',
    'tcv_petty_cash',
    'tcv_purchase',
    'tcv_rrhh_ari',
    'tcv_sale',
    'tcv_stock',
    'tcv_stock_book',
    'tcv_stock_driver',
    ]

MODULES = ','.join(module_list)
ACTION = 'install-module'
print ACTION

os.system('python oerp_ws.py '
    + '--root-path=%s ' % dbdata['server_path']
    + '--addons-path=%s ' % dbdata['addons_path']
    + '--database=%s ' % dbdata['dbgen']
    + '--password=%s ' % dbdata['openerp_password']
    + '--login=%s ' % dbdata['openerp_login']
    + '--modules=%s ' % MODULES
    + ' %s ' % ACTION
    )


MODULES =       'base'
ACTION =        'start-server'
print ACTION

os.system('python oerp_ws.py '
            + '--root-path=%s ' % dbdata['server_path']
            + '--addons-path=%s ' % dbdata['addons_path']
            + '--database=%s ' % dbdata['dbgen']
            + '--password=%s ' % dbdata['openerp_password']
            + '--login=%s ' % dbdata['openerp_login']
            + '--modules=%s ' % MODULES
            + ' %s ' % ACTION
            )


