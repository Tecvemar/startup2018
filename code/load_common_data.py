# -*- encoding: utf-8 -*-
from open_lnk import openerp_link
from definitions import dbdata
import models

lnk_dbgen = openerp_link(
    dbdata['host'],
    dbdata['rpc_port'],
    dbdata['dbgen'],
    dbdata['openerp_login'],
    dbdata['openerp_password'])

print 'Cargando datos comunes...'

#~ models.load_res_users(lnk_dbgen)
#~ models.load_res_country_state(lnk_dbgen)
#~ models.load_product_product_features(lnk_dbgen)
#~ models.load_res_partner_title(lnk_dbgen)
#~ models.load_product_uom(lnk_dbgen)
#~ models.load_account_account_type(lnk_dbgen)
#~ models.update_res_currency(lnk_dbgen)
#~ models.update_res_company(lnk_dbgen)
#~ models.load_account_account(lnk_dbgen)
#~ models.load_account_payment_term(lnk_dbgen)
#~ models.load_account_payment_term_line(lnk_dbgen)
#~ models.load_tcv_bank_list(lnk_dbgen)
#~ models.load_l10n_ut(lnk_dbgen)
#~ models.load_account_tax(lnk_dbgen)
#~ models.load_account_journal(lnk_dbgen)
models.load_product_category(lnk_dbgen)
#~ models.load_product_product_tile_format(lnk_dbgen)
