# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp
import datetime
import decimal


class profit_2_openerp(csv_2_openerp):

    def __init__(self, model, lnk, profit_lnk):
        super(profit_2_openerp, self).__init__('', model, lnk)
        self.dbprofit = profit_lnk
        self.aux02_field = 'aux02'

    def set_sql(self, sql_string):
        self.dbprofit.set_sql_string(sql_string)

    def set_args(self, *args):
        self.dbprofit.set_sql_args(args)

    def format_data_row(self, item):
        res = super(profit_2_openerp, self).format_data_row(item)
        aux02 = {}
        for key in res.keys():
            if isinstance(item[key], datetime.datetime):
                item[key] = item[key].strftime('%Y-%m-%d')
            if isinstance(item[key], decimal.Decimal):
                item[key] = float(item[key])
            if key == self.aux02_field and self.aux02_fields:
                values = self.decode_aux02(item[key])
                for fld in self.aux02_fields:
                    aux02.update({fld: values[fld]})
            if type(item[key]) == unicode:
                item[key] = item[key].strip()
        res.update(aux02)
        if self.aux02_field in res and self.aux02_fields:
            res.pop(self.aux02_field)
        return res

    def load_data(self):
        if self.dbprofit.sql:
            self.data = self.format_csv_data(self.dbprofit.execute_sql())

    def close(self):
        self.dbprofit.close()
