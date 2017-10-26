# -*- encoding: utf-8 -*-
import csv
import sys
import gc
from rif import calcular_rif


__animation__ = "|/-\\"


class csv_2_openerp(object):

    def __init__(self, csv_file, model, lnk):
        '''
        '''
        self.msg = '  Cargando: %s' % (model)
        print self.msg,
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
        self.set_vat_field = ''
        self.m2m_fields = []
        self.wait_idx = 0

    def load_data(self):
        if self.csv_file:
            self.data = self.format_csv_data(
                csv.DictReader(open(self.csv_file)))

    def find_related_field_value(self, item, f):
        value = self.find_duplicated(
            item[f], self.relations[f]['model'],
            self.relations[f]['search_fields'])
        if not value and item[f]:
            print '\tNo encontrado! -> %s: "%s" ' % (f, item[f])
        return value and len(value) == 1 and value[0] or 0

    def format_data_row(self, item):
        for f in self.integer_fields:
            item[f] = int(item[f])
        for f in self.boolean_fields:
            item[f] = item[f] == 't' or item[f] == 'True'
        for f in self.float_fields:
            item[f] = float(item[f])
        for f in self.relational_fields:
            if not self.relations[f]['self_search']:
                item[f] = self.find_related_field_value(item, f)
        if self.set_vat_field in item:
            item[self.set_vat_field] = self.validate_vat_field(
                item[self.set_vat_field])
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

    def format_m2m_data(self, item):
        for m2m in self.m2m_fields:
            field = m2m[0]
            operation = m2m[1]
            rel_model = m2m[2]
            if operation == 'link':
                search_fields = m2m[3]
                value = self.find_duplicated(
                    item[field], rel_model, search_fields)
                if value and len(value) == 1:
                    item[field] = [(4, value[0])]

    def format_csv_data(self, csv_reader):
        res = []
        for item in csv_reader:
            self.show_wait()
            row = self.format_data_row(item)
            self.format_chield_data(row)
            self.format_m2m_data(row)
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

    def set_m2m_fields(self, fields_list):
        '''
        fields_list: A list of file names to be procesed as many2many ref
        '''
        self.m2m_fields = []
        self.m2m_fields.extend(fields_list)

    def set_relational_fields(self, fields_rel):
        '''
        fields_rel: A list of tuples used to search data in related model,
                    use format: (field, model, search_fields)
        Sample:
            csv_2_openerp.set_relational_fields(
                [('partner_id', 'res.partner', 'vat'), ])
        Updated data values:
            self.relations a Dict with relations data for each field
            self.relational_fields List with user's relations
        '''
        self.relational_fields = []
        self.relational_fields.extend(
            [x[0] for x in fields_rel])
        self.relations = {}
        for item in fields_rel:
            self.relations.update({
                item[0]: {'model': item[1],
                          'search_fields': item[2],
                          'self_search': item[1] == self.model,
                          }})

    def set_child_model_fields(self, child_models):
        '''
        List of child fields: ['field_name1','field_name2']
        '''
        self.child_model_fields = []
        self.child_model_fields.extend(child_models)

    def validate_vat_field(self, vat):
        vat = vat.replace('-', '').replace('.', '').replace(' ', '').strip().upper()
        if 'J' not in vat:
            if 'V' not in vat and vat.isdigit():
                vat = 'V%08d' % int(vat)
        if len(vat) == 8 and 'V' in vat:
            vat = vat[0] + '0' + vat[1:]
        if len(vat) == 9:
            vat = calcular_rif(vat)
        if len(vat) != 10:
            print '\nError en el RIF: %s\n' % vat
            return ''
        return 'VE' + vat

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
        cache_key = '%s%s%s' % (
            self.lnk.database[:5], model.replace('.',''),
            str(search_args).strip('[]').replace("'", '').replace(', ', ''))
        if cache_key in self.search_cache:
            return self.search_cache[cache_key]
        if search_args:
            item_ids = self.lnk.execute(
                model, 'search', search_args)
            if item_ids:
                self.search_cache[cache_key] = item_ids
            return item_ids
        return []

    def process_csv(self):
        self.load_data()
        for item in self.data:
            self.show_wait()
            for f in self.relational_fields:
                if self.relations[f]['self_search']:
                    item[f] = self.find_related_field_value(item, f)
            item_ids = self.find_duplicated(item)
            if not item_ids:
                self.lnk.execute(self.model, 'create', item)
            elif self.update_records and len(item_ids) == 1:
                self.lnk.execute(self.model, 'write', item_ids, item)
        gc.collect()
        print "\r" + self.msg + ', Listo.'

    def test_data_file(self):
        self.load_data()
        for item in self.data:
            print item

    def execute(self, model, action, *args):
        self.lnk.execute(model, action, *args)

    def show_wait(self):
        print "\r" + self.msg, __animation__[
            self.wait_idx % len(__animation__)],
        self.wait_idx += 1
        sys.stdout.flush()
