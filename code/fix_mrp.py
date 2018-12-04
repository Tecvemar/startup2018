# -*- encoding: utf-8 -*-
from open_lnk import openerp_link
from definitions import dbdata

# login with migration's user
dbopen = openerp_link(
    '192.168.0.9',
    8069,
    'operaciones',
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
        [#  Bl-3175 LEONA
         (1181, 'tcv.mrp.resin'),
         (2675, 'tcv.mrp.polish'),
         (1399, 'tcv.mrp.finished.slab'),
         ],
        [#  BL-3210 LEONA
         (1177, 'tcv.mrp.resin'),
         (2671, 'tcv.mrp.polish'),
         (1395, 'tcv.mrp.finished.slab'),
         ],
        [#  BL-3224 LEONA
         (1186, 'tcv.mrp.resin'),
         (2680, 'tcv.mrp.polish'),
         (1404, 'tcv.mrp.finished.slab'),
         ],
        [#  BL-3226 LEONA
         (2681, 'tcv.mrp.polish'),
         (1405, 'tcv.mrp.finished.slab'),
         ],
        [#  BL-3231 LEONA
         (1178, 'tcv.mrp.resin'),
         (2672, 'tcv.mrp.polish'),
         (1396, 'tcv.mrp.finished.slab'),
         ],
        [#  BL-3241 LEONA
         (2660, 'tcv.mrp.polish'),
         (1182, 'tcv.mrp.resin'),
         (2676, 'tcv.mrp.polish'),
         (1407, 'tcv.mrp.finished.slab'),
         ],
        [#  BL-3248 LEONA
         (1183, 'tcv.mrp.resin'),
         (2677, 'tcv.mrp.polish'),
         (1401, 'tcv.mrp.finished.slab'),
         ],
        [#  BL-3255 LEONA
         (1185, 'tcv.mrp.resin'),
         (2679, 'tcv.mrp.polish'),
         (1403, 'tcv.mrp.finished.slab'),
         ],
        [#  BL-1500 AMARA
         (1179, 'tcv.mrp.resin'),
         (2673, 'tcv.mrp.polish'),
         (1397, 'tcv.mrp.finished.slab'),
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


def fix_account_invoice_move(dbopen, task, lot):
        invoice_lines = dbopen.execute(
            'account.invoice.line', 'read', lot['invoice_lines_ids'], [])
        for line in invoice_lines:
            invoice = dbopen.execute(
                'account.invoice', 'read', line['invoice_id'][0], [])
            if invoice['move_id']:
                reconcile_ids = []
                move_id = invoice['move_id'][0]
                execute_fix_wkf(
                    dbopen, 'account.move', 'button_cancel', move_id)
                move = dbopen.execute(
                    'account.move', 'read', move_id, [])
                move_lines = dbopen.execute(
                    'account.move.line', 'read', move['line_id'], [])
                for mline in move_lines:
                    if mline['reconcile_id'] or mline['reconcile_partial_id']:
                        reconcile_ids.append({
                            'id': mline['id'],
                            'reconcile_id': mline['reconcile_id'] and mline['reconcile_id'][0] or 0,
                            'reconcile_partial_id': mline['reconcile_partial_id'] and mline['reconcile_partial_id'][0] or 0,
                            })
                        dbopen.execute(
                            'account.move.line', 'write', [mline['id']],
                            {'reconcile_id': 0, 'reconcile_partial_id': 0})
                for mline in move_lines:
                    if lot['name'] in mline['name']:
                        data = {'debit': 0.0, 'credit': 0.0}
                        amount = round(
                            lot['property_cost_price'] * mline['quantity'], 2)
                        data['debit'] = amount if mline['debit'] else 0.0
                        data['credit'] = amount if mline['credit'] else 0.0
                        dbopen.execute(
                            'account.move.line', 'write', [mline['id']], data)
                        print [mline[x] for x in (
                            'name', 'debit', 'credit')], data
                for rline in reconcile_ids:
                    dbopen.execute(
                        'account.move.line', 'write', [rline['id']], rline)
                execute_fix_wkf(
                    dbopen, 'account.move', 'post', move_id)


def fix_finished_model(dbopen, task):
    dbopen.execute(
        task['res_model'], 'call_compute_average_cost', task['id'])
    outputs = dbopen.execute(
        'tcv.mrp.finished.slab.output', 'read', task['output_ids'])
    for item in outputs:
        # Fix lot cost
        prod_lot_id = item['prod_lot_id'][0]
        dbopen.execute(
            'stock.production.lot', 'write', prod_lot_id,
            {'property_cost_price': item['real_unit_cost']})
        # Check sale and fix costs (if needed)
        lot = dbopen.execute(
            'stock.production.lot', 'read', prod_lot_id, [])
        if lot['invoice_lines_ids']:
            fix_account_invoice_move(dbopen, task, lot)
    return True


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
    for group in get_groups_to_fix():
        for task_id, res_model in group:
            task = read_task(dbopen, task_id, res_model)
            fix_base_model(dbopen, task)
            fix_costs_model(dbopen, task)
            fix_io_slabs_model(dbopen, task)
            if res_model == 'tcv.mrp.finished.slab':
                fix_finished_model(dbopen, task)
            fix_acc_move_model(dbopen, task)


process_fix()
