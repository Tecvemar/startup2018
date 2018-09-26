# -*- encoding: utf-8 -*-
from open_lnk import openerp_link
from definitions import dbdata

# login with migration's user
dbopen = openerp_link(
    'localhost',
    8069,
    'prueba2',
    dbdata['openerp_login'],
    dbdata['openerp_password'],
    )


def get_operator_and_factory_cost_by_m2(dbopen):
    cost_ids = dbopen.execute(
        'tcv.mrp.template.param', 'search',
        [('name', 'in', ('operator_cost_m2', 'factory_overhead_m2'))])
    costs = dbopen.execute(
        'tcv.mrp.template.param', 'read', cost_ids, [])
    res = {x['param_id'][0]: {} for x in costs}

    for item in costs:
        template_id = item['param_id'][0]
        res[template_id][item['name']] = item['float_val']
    print res


def cost_distribution(dbopen, model, item):
    res = {}
    return res


def find_mrp_process(dbopen):
    '''
    Search for production process to be fixed
    '''
    lotes = []
    prior_ids = []
    for model in ('tcv.mrp.gangsaw', 'tcv.mrp.polish',
                  'tcv.mrp.resin', 'tcv.mrp.waste.slab',
                  'tcv.mrp.finished.slab'):
        task_ids = dbopen.execute(
            model, 'search', [('state', '=', 'done'),
                              ('operator_cost', '>', 1),
                              ('date_end', '>', '2018-01-01')])
        print model, len(task_ids)
        for item in dbopen.execute(model, 'read', task_ids):
            sbprcs = dbopen.execute(
                'tcv.mrp.subprocess', 'read', item['parent_id'][0])
            lotes.append(item['task_info'].split()[1])
            prior_ids.append(sbprcs['id'])
            print item['id'], item['task_info'], \
                item['parent_id'], item['operator_cost']
        prior_sbprcss_ids = prior_ids and dbopen.execute(
            'tcv.mrp.subprocess', 'search',
            [('prior_id', 'in', prior_ids)])
        for item in dbopen.execute('tcv.mrp.subprocess', 'read',
                                   prior_sbprcss_ids):
            print item['id'], item['template_id'], \
                item['ref'], item['name'], item['task_name']
    print list(set(lotes))


def get_tasks_to_fix():
    '''
    list of task manually created

    '''
    return [[(2660, 'tcv.mrp.polish'),
             ]
            ]
