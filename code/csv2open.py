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
        self.relational_fields = []
        self.relations = []

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
            for f in self.relational_fields:
                value = self.find_duplicated(
                    item[f], self.relations[f]['model'],
                    self.relations[f]['search_fields'])
                item[f] = value and len(value) == 1 and value[0] or None
            res.append(item)
        return res

    def set_search_fields(self, fields_list):
        '''
        fields_list: A list of file names, used to search for duplicateds
                     records (key fields)
        Sample:
            csv_2_openerp.set_search_fields(['name', 'country_id'])
        '''
        self.search_fields = []
        self.search_fields.extend(fields_list)

    def set_integer_fields(self, fields_list):
        '''
        fields_list: A list of file namesto be converted to int value
        Sample:
            csv_2_openerp.set_integer_fields(['pieces'])
        '''
        self.integer_fields = []
        self.integer_fields.extend(fields_list)

    def set_float_fields(self, fields_list):
        '''
        fields_list: A list of file namesto be converted to float value
        Sample:
            csv_2_openerp.set_float_fields(['amount'])
        '''
        self.float_fields = []
        self.float_fields.extend(fields_list)

    def set_relational_fields(self, fields_rel):
        '''
        fields_rel: A list of tuples used to search data in related model,
                    use format: (field, model, search_fields)
        Sample:
            csv_2_openerp.set_relational_fields(
                [('partner_id', 'res.partner', 'vat'), ])
        '''
        self.relational_fields = []
        self.relational_fields.extend(
            [x[0] for x in fields_rel])
        self.relations = {}
        for item in fields_rel:
            self.relations.update({
                item[0]: {'model': item[1],
                          'search_fields': item[2],
                          }})

    def find_duplicated(self, item, model=False, search_fields=[]):
        if not model:
            model = self.model
        if not search_fields:
            search_fields = self.search_fields
        search_args = []
        for field in search_fields:
            if type(item) in (dict, list):
                search_args.append((field, '=', item[field]))
            else:
                search_args.append((field, '=', item))
        item_ids = self.lnk.execute(
            model, 'search', search_args)
        return item_ids

    def process_csv(self):
        self.load_csv()
        for item in self.csv_data:
            if not self.find_duplicated(item):
                self.lnk.execute(self.model, 'create', item)
