# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp
import datetime
import decimal


class profit_2_openerp(csv_2_openerp):

    def __init__(self, model, lnk, profit_lnk):
        super(profit_2_openerp, self).__init__('', model, lnk)
        self.dbprofit = profit_lnk
        self.aux02_fields = []

    def set_sql(self, sql_string):
        self.dbprofit.set_sql_string(sql_string)

    def set_args(self, *args):
        self.dbprofit.set_sql_args(args)

    def set_aux02_fields(self, field_names):
        '''
        Create a list of fields to be extracted from aux02 profit's field
        all fields:
        p20.set_aux02_fields([
            'pieces', 'length', 'heigth', 'width', 'location_id'])
        '''
        self.aux02_fields = field_names

    def decode_aux02(self, a2):
        '''
        This code splits the data in aux02 (from profit db)
        '''
        if a2:
            data = a2.split(';')
            pc = le = he = wi = 0
            ub = ''
            if len(data) == 4:
                if data[0]:
                    pc = int(float(data[0]))
                    wi = float(data[0])
                if data[1]:
                    le = float(data[1].replace(',', '.'))
                if data[2]:
                    he = float(data[2])
                if data[3]:
                    ub = data[3]
            res = {'pieces': pc,
                   'length': le,
                   'heigth': he,
                   'width': wi,
                   'location': ub}
        else:
            res = {'pieces': 0,
                   'length': 0,
                   'heigth': 0,
                   'width': 0,
                   'location': 0}
        return res

    def format_data_row(self, item):
        res = super(profit_2_openerp, self).format_data_row(item)
        aux02 = {}
        for k in res.keys():
            if isinstance(item[k], datetime.datetime):
                item[k] = item[k].strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(item[k], decimal.Decimal):
                item[k] = float(item[k])
            if k == 'aux02' and self.aux02_fields:
                values = self.decode_aux02(item[k])
                for f in self.aux02_fields:
                    aux02.update({f: values[f]})
        res.update(aux02)
        if 'aux02' in res and self.aux02_fields:
            res.pop('aux02')
        return res

    def load_data(self):
        if self.dbprofit.sql:
            self.data = self.format_csv_data(self.dbprofit.execute_sql())
