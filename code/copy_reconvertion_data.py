# -*- encoding: utf-8 -*-
from open_lnk import openerp_link
from definitions import dbdata

# login with migration's user
dbsource = openerp_link(
    'localhost',
    8069,
    'desarrollo',
    dbdata['openerp_login'],
    dbdata['openerp_password'],
    )

dbdest = openerp_link(
    'localhost',
    8069,
    'reconversionbarcelona',
    dbdata['openerp_login'],
    dbdata['openerp_password'],
    )

__fix_mode__ = True


def update_tcv_reconvertion(item):
    data = {
        'name': 'ACROPOLIS 2018',
        'date': '2018-08-20',
        'sql_command': item['sql_command'],
        'sql_reverse': item['sql_reverse'],
        }
    dbdest.execute('tcv.reconvertion', 'write', [1], data)
    # ~ dbdest.execute('tcv.reconvertion', 'button_load', [1])


def copy_fields_data(source_model, dest_model):
    source_fields = dbsource.execute(
        'tcv.reconvertion.fields', 'read', source_model['fields_ids'], [])
    dest_fields = dbdest.execute(
        'tcv.reconvertion.fields', 'read', dest_model['fields_ids'], [])
    # ~ print source_fields
    for source in source_fields:
        for dest in dest_fields:
            if source['name'] == dest['name']:
                data = {
                    'rounding': source['rounding'],
                    'method': source['method'],
                    'fld_type': source['fld_type'],
                    'store': source['store']
                    }
                dbdest.execute(
                    'tcv.reconvertion.fields', 'write', dest['id'], data)


def copy_models_data(model):
    source_model = dbsource.execute(
        'ir.model', 'read', model['model_id'][0], ['model'])
    dest_model_id = dbdest.execute(
        'ir.model', 'search', [('model', '=', source_model['model'])])
    if dest_model_id:
        line_id = dbdest.execute(
            'tcv.reconvertion.models', 'search',
            [('model_id', '=', dest_model_id[0])])
        if line_id:
            data = {
                'status': model['status'],
                'use_company_rule': model['use_company_rule'],
                'check_currecy': model['check_currecy'],
                'where': model['where']
                }
            dbdest.execute('tcv.reconvertion.models', 'write', line_id, data)
            dest_model = dbdest.execute(
                'tcv.reconvertion.models', 'read', line_id[0], [])
            copy_fields_data(model, dest_model)


def process_fix():
    data_ids = dbsource.execute(
        'tcv.reconvertion', 'search', [])
    data = dbsource.execute(
        'tcv.reconvertion', 'read', data_ids, [])
    for item in data:
        update_tcv_reconvertion(item)
        for model in dbsource.execute(
                'tcv.reconvertion.models', 'read', item['models_ids'], []):
            print model['model_id'][1]
            copy_models_data(model)


process_fix()
