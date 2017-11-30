# -*- encoding: utf-8 -*-
from open_lnk import openerp_link
from profit_lnk import profit_link
from definitions import dbdata
import companies


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
        dbdata['migracion_login'],
        dbdata['migracion_password'],
        dbdata['postgresql_login'],
        dbdata['postgresql_password'],
        )

    print 'Cargando datos de compañias: %s...' % database

    companies.load_bank_account_journal(lnk_dbcom, lnk_dbprofit)
    companies.load_stock_production_lot(lnk_dbcom, lnk_dbprofit)
    companies.load_stock_production_lot_extra(lnk_dbcom)
    companies.load_stock_production_lot_update(lnk_dbcom)
    companies.load_res_company(lnk_dbcom)
    companies.load_stock_warehouse(lnk_dbcom)
    companies.load_stock_location(lnk_dbcom)
    companies.load_ir_translation(lnk_dbcom)
    companies.load_sale_shop(lnk_dbcom)
    companies.load_account_account_0(lnk_dbcom)
    companies.load_product_product(lnk_dbcom)
    companies.load_res_partner_address(lnk_dbcom)
    companies.load_res_partner(lnk_dbcom)
    # Purchases ---------------------------------------------------------------
    companies.load_res_partner_profit_pruchase(lnk_dbcom, lnk_dbprofit)
    companies.load_purchase_order(lnk_dbcom, lnk_dbprofit)
    companies.load_purchase_order_line_profit_detail(lnk_dbcom, lnk_dbprofit)
    companies.load_purchase_order_no_details(lnk_dbcom, lnk_dbprofit)
    companies.postprocess_purchase_order(lnk_dbcom, lnk_dbprofit)
    companies.load_stock_inventory_line(lnk_dbcom, lnk_dbprofit)
    companies.postprocess_stock_inventory(lnk_dbcom, lnk_dbprofit)
    companies.postprocess_stock_picking(lnk_dbcom, lnk_dbprofit)
    companies.load_tcv_stock_changes(lnk_dbcom, lnk_dbprofit)
    # Sales -------------------------------------------------------------------
    companies.load_res_partner_profit_sale(lnk_dbcom, lnk_dbprofit)
    companies.load_res_partner_companies_extra_data(lnk_dbcom)
    companies.load_sale_order(lnk_dbcom, lnk_dbprofit)
    companies.load_sale_order_line_profit_detail(lnk_dbcom, lnk_dbprofit)
    companies.postprocess_sale_order(lnk_dbcom, lnk_dbprofit)
    companies.postprocess_stock_move(lnk_dbcom)
    # Payments ----------------------------------------------------------------
    companies.load_account_wh_iva(lnk_dbcom, lnk_dbprofit)
    companies.load_islr_wh_doc(lnk_dbcom, lnk_dbprofit)
    # Books -------------------------------------------------------------------
    companies.load_fiscal_book(lnk_dbcom)
    companies.load_tcv_stock_book(lnk_dbcom)

    if lnk_dbprofit:
        lnk_dbprofit.close()
