# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_tcv_bank_config(dbcomp):

    work_dir = '../data/companies/%s/' % dbcomp.database
    c2o = csv_2_openerp(
        work_dir + 'tcv_bank_config.csv', 'tcv.bank.config', dbcomp)
    c2o.update_records = True
    c2o.set_search_fields(['company_id'])
    c2o.set_integer_fields(['company_id'])
    c2o.set_relational_fields([
        ('detail_ids.journal_id', 'account.journal', ['code']),
        ('detail_ids.bank_journal_id', 'account.journal', ['code']),
        ('acc_bank_comis', 'account.account', ['code']),
        ('acc_prepaid_tax', 'account.account', ['code']),
        ])
    c2o.set_child_model_fields(['detail_ids'])
    c2o.process_csv()
