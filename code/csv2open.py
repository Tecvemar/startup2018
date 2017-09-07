# -*- encoding: utf-8 -*-
import csv


class csv_2_openerp(object):

    def __init__(self, csv_file, model, lnk):
        print 'Cargando: %s...' % (model)
        self.csv_file = csv_file
        self.model = model
        self.lnk = lnk
        self.search_fields = []
        self.integer_fields = []
        self.float_fields = []

    def load_csv(self):
        self.csv_data = self.format_csv_data(
            csv.DictReader(open(self.csv_file)))

    def format_csv_data(self, csv_reader):
        res = []
        for item in csv_reader:
            for f in self.integer_fields:
                item[f] = int(item[f])
            for f in self.float_fields:
                item[f] = float(item[f])
            res.append(item)
        return res

    def set_search_fields(self, fields_list):
        '''
        fields: a list of file names, used to search for duplicateds records
        '''
        self.search_fields = []
        self.search_fields.extend(fields_list)

    def set_integer_fields(self, fields_list):
        self.integer_fields = []
        self.integer_fields.extend(fields_list)

    def set_float_fields(self, fields_list):
        self.float_fields = []
        self.float_fields.extend(fields_list)

    def find_duplicated(self, item):
        search_args = []
        for field in self.search_fields:
            search_args.append((field, '=', item[field]))
        print search_args
        item_ids = self.lnk.execute(
            self.model, 'search', search_args)
        return item_ids

    def process_csv(self):
        self.load_csv()
        for item in self.csv_data:
            if not self.find_duplicated(item):
                self.lnk.execute(self.model, 'create', item)
