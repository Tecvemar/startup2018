# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_account_period(lnk):
    c2o = csv_2_openerp(
        '../data/common/account_period.csv', 'account.period', lnk)
    c2o.set_search_fields(['code'])
    c2o.set_boolean_fields(['special'])
    c2o.set_relational_fields([
        ('fiscalyear_id', 'account.fiscalyear', ['code'])])
    c2o.process_csv()
