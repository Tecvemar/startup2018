# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_product_category(lnk):

    c2o = csv_2_openerp(
        '../data/common/product_category.csv', 'product.category', lnk)
    c2o.set_search_fields(['code'])
    #~ c2o.set_integer_fields(['property_stock_variation'])
    c2o.set_relational_fields([
        ('property_stock_account_output_categ', 'account.account', ['code']),
        ('property_stock_account_input_categ', 'account.account', ['code']),
        ('property_stock_variation', 'account.account', ['code']),
        ('property_account_income_categ', 'account.account', ['code']),
        ('property_account_expense_categ', 'account.account', ['code']),
        ('property_stock_journal', 'account.journal', ['code']),
        ('parent_id', 'product.category', ['code']),
        ])
    c2o.process_csv()
