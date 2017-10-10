# -*- encoding: utf-8 -*-
import csv


class csv_2_openerp(object):

    def __init__(self, csv_file, model, lnk):
        '''
        '''
        print 'Cargando: %s...' % (model)
        self.csv_file = csv_file
        self.model = model
        self.lnk = lnk
        self.data = []
        self.update_records = False
        self.search_fields = []
        self.integer_fields = []
        self.boolean_fields = []
        self.float_fields = []
        self.relational_fields = []
        self.child_model_fields = []
        self.relations = {}
        self.search_cache = {}

    def load_data(self):
        if self.csv_file:
            self.data = self.format_csv_data(
                csv.DictReader(open(self.csv_file)))

    def format_data_row(self, item):
        for f in self.integer_fields:
            item[f] = int(item[f])
        for f in self.boolean_fields:
            item[f] = item[f] == 't' or item[f] == 'True'
        for f in self.float_fields:
            item[f] = float(item[f])
        for f in self.relational_fields:
            value = self.find_duplicated(
                item[f], self.relations[f]['model'],
                self.relations[f]['search_fields'])
            if not value:
                print '\tNo encontrado! -> %s: %s ' % (f, item[f])
            item[f] = value and len(value) == 1 and value[0] or 0
        return item

    def format_chield_data(self, item):
        '''
        Process child_models_fields list and separate in new child_dict, then
        delete original keys and replace with
        Child_field: (0, 0, {child_dict})
        '''
        for field in self.child_model_fields:
            field_dot = field + '.'
            child_keys = filter(
                None, [x if field_dot in x else None for x in item.keys()])
            chks = [x.replace(field_dot, '') for x in child_keys]
            child_dict = {
                chks[x]: item[child_keys[x]] for x in range(len(chks))}
            [item.pop(f) for f in child_keys]
            item.update({field: [(0, 0, child_dict)]})

    def format_csv_data(self, csv_reader):
        res = []
        for item in csv_reader:
            row = self.format_data_row(item)
            self.format_chield_data(row)
            res.append(row)
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
        fields_list: A list of file names o be converted to int value
        Sample:
            csv_2_openerp.set_integer_fields(['pieces'])
        '''
        self.integer_fields = []
        self.integer_fields.extend(fields_list)

    def set_boolean_fields(self, fields_list):
        '''
        fields_list: A list of file names to be converted to bool value
        Sample:
            csv_2_openerp.set_integer_fields(['pieces'])
        '''
        self.boolean_fields = []
        self.boolean_fields.extend(fields_list)

    def set_float_fields(self, fields_list):
        '''
        fields_list: A list of file names to be converted to float value
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

    def set_child_model_fields(self, child_models):
        '''
        List of child fields: ['field_name1','field_name2']
        '''
        self.child_model_fields = []
        self.child_model_fields.extend(child_models)

    def find_duplicated(self, item, model=False, search_fields=[]):
        if not model:
            model = self.model
        if not search_fields:
            search_fields = self.search_fields
        search_args = []
        for field in search_fields:
            if type(item) in (dict, list):
                if item[field]:
                    search_args.append((field, '=', item[field]))
            else:
                if item:
                    search_args.append((field, '=', item))
        cache_key = '%s%s' % (
            model,
            str(search_args).strip('[]').replace("'", '').replace(', ', ''))
        if cache_key in self.search_cache:
            return self.search_cache[cache_key]
        item_ids = self.lnk.execute(
            model, 'search', search_args)
        if item_ids:
            self.search_cache[cache_key] = item_ids
        return item_ids

    def process_csv(self):
        self.load_data()
        for item in self.data:
            item_ids = self.find_duplicated(item)
            if not item_ids:
                self.lnk.execute(self.model, 'create', item)
            elif self.update_records and len(item_ids) == 1:
                self.lnk.execute(self.model, 'write', item_ids, item)

    def test_data_file(self):
        self.load_data()
        for item in self.data:
            print item

    def execute(self, model, action, *args):
        self.lnk.execute(model, action, *args)
