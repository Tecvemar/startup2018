# -*- encoding: utf-8 -*-
from open_lnk import openerp_link
from definitions import dbdata

# login with migration's user
dbpen = openerp_link(
    'localhost',
    8069,
    'barcelona',
    dbdata['openerp_login'],
    dbdata['openerp_password'],
    )

__fix_mode__ = True


def process_fix():
    names = [
        ('IVA 12% Compras', 'IVA 16% Compras'),
        ('IVA 12% Ventas', 'IVA 16% Ventas'),
        ]

    for iva_name in names:
        iva12_id = dbpen.execute(
            'account.tax', 'search', [('name', '=', iva_name[0])])[0]
        iva16_id = dbpen.execute(
            'account.tax', 'search', [('name', '=', iva_name[1])])[0]
        print '%s -> %s:' % iva_name, iva12_id, '->', iva16_id
        sql = "UPDATE product_taxes_rel SET tax_id = %(iva16_id)s " + \
            "WHERE tax_id = %(iva12_id)s"
        params = {'iva12_id': iva12_id, 'iva16_id': iva16_id}
        print sql % params
        # ~ dbpen.execute_sql(sql, params)  # Comment this line to test


process_fix()
