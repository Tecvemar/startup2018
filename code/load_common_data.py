# -*- encoding: utf-8 -*-
from open_lnk import openerp_link
from definitions import dbdata
import models

lnk_dbgen_admin = openerp_link(
    dbdata['host'],
    dbdata['rpc_port'],
    dbdata['dbgen'],
    dbdata['openerp_login'],
    dbdata['openerp_password'])

lnk_dbgen = openerp_link(
    dbdata['host'],
    dbdata['rpc_port'],
    dbdata['dbgen'],
    dbdata['migracion_login'],
    dbdata['migracion_password'])

lnk_dbdesarrollo = openerp_link(
    dbdata['host'],
    dbdata['rpc_port'],
    dbdata['dbdesarrollo'],
    dbdata['openerp_login'],
    dbdata['openerp_password'])

print 'Cargando datos comunes...'

models.load_res_users(lnk_dbgen_admin)
models.load_res_country_state(lnk_dbgen)
models.load_product_product_features(lnk_dbgen)
models.load_res_partner_title(lnk_dbgen)
models.load_product_uom(lnk_dbgen)
models.load_account_account_type(lnk_dbgen)
models.update_res_company(lnk_dbgen)
models.update_res_currency(lnk_dbgen)
models.update_res_lang(lnk_dbgen)
models.load_account_account(lnk_dbgen)
models.load_account_payment_term(lnk_dbgen)
models.load_account_payment_term_line(lnk_dbgen)
models.load_tcv_bank_list(lnk_dbgen)
models.load_l10n_ut(lnk_dbgen)
models.load_account_tax(lnk_dbgen)
models.load_account_journal(lnk_dbgen)
models.load_stock_journal(lnk_dbgen)
models.load_product_category(lnk_dbgen)
models.load_product_product_tile_format(lnk_dbgen)
models.load_tcv_stock_changes_method(lnk_dbgen)
models.load_product_product(lnk_dbgen)
models.postprocess_product_product(lnk_dbgen, lnk_dbdesarrollo)
models.load_tcv_driver_vehicle(lnk_dbgen)
models.load_product_pricelist(lnk_dbgen)
models.load_tcv_igtf(lnk_dbgen)
models.load_account_fiscalyear(lnk_dbgen)
models.load_account_period(lnk_dbgen)
models.load_res_partner_account(lnk_dbgen)
models.load_tcv_import_config(lnk_dbgen)
models.load_tcv_sale_order_config(lnk_dbgen)
models.load_stock_inventory(lnk_dbgen)
models.load_stock_location(lnk_dbgen)
models.load_ir_sequence(lnk_dbgen)
models.load_tcv_to_dispatch_config(lnk_dbgen)
