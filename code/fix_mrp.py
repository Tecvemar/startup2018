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

__fix_mode__ = True


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
    return res


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
        # ~ print model, len(task_ids)
        for item in dbopen.execute(model, 'read', task_ids):
            sbprcs = dbopen.execute(
                'tcv.mrp.subprocess', 'read', item['parent_id'][0])
            lotes.append(item['task_info'].split()[1])
            prior_ids.append(sbprcs['id'])
            # ~ print item['id'], item['task_info'], \
                # ~ item['parent_id'], item['operator_cost']
        # ~ prior_sbprcss_ids = prior_ids and dbopen.execute(
            # ~ 'tcv.mrp.subprocess', 'search',
            # ~ [('prior_id', 'in', prior_ids)])
        # ~ for item in dbopen.execute('tcv.mrp.subprocess', 'read',
                                   # ~ prior_sbprcss_ids):
            # ~ print item['id'], item['template_id'], \
                # ~ item['ref'], item['name'], item['task_name']
    # ~ print list(set(lotes))


def get_groups_to_fix():
    '''
    list of task manually created

    '''
    return [
        [(1181, 'tcv.mrp.resin'),
         (2675, 'tcv.mrp.polish'),
         (1399, 'tcv.mrp.finished.slab'),
         ],
        [(2660, 'tcv.mrp.polish'),
         (1182, 'tcv.mrp.resin'),
         (2676, 'tcv.mrp.polish'),
         (1407, 'tcv.mrp.finished.slab'),
         ],
        ]


def read_task(dbopen, task_id, res_model):
    task = dbopen.execute(res_model, 'read', task_id)
    # ~ print res_model, task_id, task
    inputs_model = res_model + '.inputs'
    output_model = res_model + '.output'
    costs_model = res_model + '.costs'
    subprocess = dbopen.execute(
        'tcv.mrp.subprocess', 'read', task['parent_id'][0])
    io_slabs_ids = dbopen.execute(
        'tcv.mrp.io.slab', 'search', [
            ('task_ref', '=', task['id']),
            ('subprocess_ref', '=', subprocess['id'])])
    io_slabs = dbopen.execute(
        'tcv.mrp.io.slab', 'read', io_slabs_ids)
    inputs = dbopen.execute(
        inputs_model, 'read', task['input_ids'])
    output = dbopen.execute(
        output_model, 'read', task['output_ids'])
    costs = []
    if res_model not in ('tcv.mrp.finished.slab',):
        costs = dbopen.execute(
            costs_model, 'read', task['costs_ids'])
        # Read associated input and output
        for item in costs:
            item['output'] = dbopen.execute(
                output_model, 'read', item['output_id'][0])
            item['input'] = dbopen.execute(
                inputs_model, 'read', item['output']['input_id'][0])
    move = dbopen.execute(
        'account.move', 'read', task['move_id'][0])
    move.update({
        'move_lines': dbopen.execute(
            'account.move.line', 'read', move['line_id'])})
    task.update({
        'subprocess': subprocess,
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
        dbopen.execute(res_model, method, [id])
    else:  # test_mode
        print res_model, id, method


def fix_base_model(dbopen, task):
    template_cost = get_operator_and_factory_cost_by_m2(dbopen)
    if task['subprocess']['template_id'][0] in template_cost:
        mrp_cost = template_cost[task['subprocess']['template_id'][0]]
        data = {
            'operator_cost': mrp_cost['operator_cost_m2'],
            'factory_overhead': mrp_cost['factory_overhead_m2'],
            'valid_cost': True,
            }
        write_model_fix(
            dbopen, task['res_model'], task['id'], data)
        task.update(data)
    return True


def fix_costs_model(dbopen, task):
    for cost in task['costs']:
        template_cost = get_operator_and_factory_cost_by_m2(dbopen)
        mrp_cost = template_cost[task['subprocess']['template_id'][0]]
        area = cost['total_area']
        output = cost['output']
        inputs = cost['input']
        cumulative_cost = (
            (inputs['total_cost'] * output['pieces']) / inputs['pieces'])
        data = {
            'operator_cost': mrp_cost['operator_cost_m2'] * area,
            'factory_overhead': mrp_cost['factory_overhead_m2'] * area,
            'cumulative_cost': cumulative_cost,
            }
        fo_oc_cost = data['operator_cost'] + data['factory_overhead']
        total_cost = cost['supplies_cost'] + cumulative_cost + fo_oc_cost
        # fix cumulative_cost  // original code
        #cumulative_cost = ((output.input_id.total_cost * output.pieces) /
        #                   output.input_id.pieces)
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


def fix_finished_model(dbopen, task):
    dbopen.execute(
        task['res_model'], 'call_compute_average_cost', task['id'])
    lot_ids = []
    outputs = dbopen.execute(
        'tcv.mrp.finished.slab.output', 'read', task['output_ids'])
    for item in outputs:
        dbopen.execute(
            'stock.production.lot', 'write', item['prod_lot_id'][0],
            {'property_cost_price': item['real_unit_cost']})
        lot_ids.append([item['prod_lot_id'][0]])
    return lot_ids


def fix_acc_move_model(dbopen, task):
    move_id = task['move_id'][0]
    execute_fix_wkf(
        dbopen, 'account.move', 'button_cancel', move_id)
    #  Unlink actual lines
    for line in task['move']['line_id']:
        dbopen.execute(
            'account.move.line', 'unlink', task['move']['line_id'])
        task['move']['line_id'] = []
    #  Create new fixed lines
    lines = dbopen.execute(
        task['res_model'], 'call_create_account_move_lines', task['id'])
    dbopen.execute(
        'account.move', 'write', [move_id], {'line_id': lines})
    execute_fix_wkf(
        dbopen, 'account.move', 'post', move_id)


def process_fix():
    lot_ids = []
    for group in get_groups_to_fix():
        for task_id, res_model in group:
            task = read_task(dbopen, task_id, res_model)
            fix_base_model(dbopen, task)
            fix_costs_model(dbopen, task)
            fix_io_slabs_model(dbopen, task)
            if res_model == 'tcv.mrp.finished.slab':
                lot_ids.extend(fix_finished_model(dbopen, task))
            fix_acc_move_model(dbopen, task)


process_fix()
