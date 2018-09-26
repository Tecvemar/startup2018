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

__fix_mode__ = False


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


def get_groups_to_fix():
    '''
    list of task manually created

    '''
    return [[(2660, 'tcv.mrp.polish'),
             (1182, 'tcv.mrp.resin'),
             ]
            ]


def read_task(dbopen, task_id, res_model):
    task = dbopen.execute(res_model, 'read', task_id)
    inputs_model = res_model + '.inputs'
    output_model = res_model + '.output'
    costs_model = res_model + '.costs'
    parent = dbopen.execute(
        'tcv.mrp.subprocess', 'read', task['parent_id'][0])
    io_slabs_ids = dbopen.execute(
        'tcv.mrp.io.slab', 'search', [('task_ref', '=', task['id']),
                                      ('subprocess_ref', '=', parent['id'])])
    io_slabs = dbopen.execute(
        'tcv.mrp.io.slab', 'read', io_slabs_ids)
    inputs = dbopen.execute(
        inputs_model, 'read', task['input_ids'])
    output = dbopen.execute(
        output_model, 'read', task['output_ids'])
    costs = dbopen.execute(
        costs_model, 'read', task['costs_ids'])
    move = dbopen.execute(
        'account.move', 'read', task['move_id'][0])
    move.update({
        'move_lines': dbopen.execute(
            'account.move.line', 'read', move['line_id'])})
    task.update({
        'tcv.mrp.subprocess': parent,
        'io_slabs': io_slabs,
        'inputs': inputs,
        'output': output,
        'costs': costs,
        'io_slabs': io_slabs,
        'move': move,
        'res_model': res_model,
        })

    return task


def write_model_fix(dbopen, res_model, id, data):
    if __fix_mode__:
        dbopen.execute(res_model, 'write', id, data)
    else:  # test_mode
        print res_model, id, data

def execute_fix_wkf(dbopen, res_model, method, id):
    if __fix_mode__:
        dbopen.execute(res_model, method, id)
    else:  # test_mode
        print res_model, id, method


def fix_base_model(dbopen, task):
    data = {
        'operator_cost': task['operator_cost'] / 100,
        'factory_overhead': task['factory_overhead'] / 100,
        'valid_cost': True,
        }
    write_model_fix(
        dbopen, task['res_model'], task['id'], data)
    task.update(data)
    return True


def fix_costs_model(dbopen, task):
    for cost in task['costs']:
        print
        data = {
            'operator_cost': cost['operator_cost'] / 100,
            'factory_overhead': cost['factory_overhead'] / 100,
            }
        total_cost = data['operator_cost'] + data['operator_cost']
        total_cost += cost['supplies_cost'] + cost['cumulative_cost']
        data.update({
            'total_cost': total_cost,
            'real_unit_cost': total_cost / cost['total_area']
            })
        write_model_fix(
            dbopen, task['res_model'] + '.costs', cost['id'], data)
        cost.update(data)

    return True


def fix_io_slabs_model(dbopen, task):
    for io_slab in task['io_slabs']:
        for cost in task['costs']:
            if io_slab['cost_line'] == cost['id']:
                data = {
                    'total_cost': cost['total_cost'],
                    'real_unit_cost': cost['real_unit_cost'],
                    }
                write_model_fix(
                    dbopen, 'tcv.mrp.io.slab', io_slab['id'], data)
                io_slab.update(data)
    return True


def fix_acc_move_resin(dbopen, task):
    return

def fix_acc_move_model(dbopen, task):
    execute_fix_wkf(
        dbopen, 'account.move', 'button_cancel', task['move_id'][0])
    if task['res_model'] == 'tcv.mrp.polish':
        print
    elif task['res_model'] == 'tcv.mrp.resin':
         fix_acc_move_resin(dbopen, task)
    else:
        print 'Unknow model %s' % task['res_model']
    execute_fix_wkf(
        dbopen, 'account.move', 'post', task['move_id'][0])

def process_fix():
    for group in get_groups_to_fix():
        for task_id, res_model in group:
            task = read_task(dbopen, task_id, res_model)
            fix_base_model(dbopen, task)
            fix_costs_model(dbopen, task)
            fix_io_slabs_model(dbopen, task)
            fix_acc_move_model(dbopen, task)


process_fix()
