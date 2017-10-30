# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_tcv_sale_order_config(lnk):
    c2o = csv_2_openerp(
        '../data/common/tcv_sale_order_config.csv',
        'tcv.sale.order.config', lnk)
    c2o.update_records = True
    c2o.set_search_fields(['company_id'])
    c2o.set_integer_fields(['days_to_cancel', 'days_to_due'])
    c2o.process_csv()
