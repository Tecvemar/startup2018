# -*- encoding: utf-8 -*-
import csv


def common_res_country_state(lnk):
    res_country_state = csv.DictReader(
        open('../data/common/res_country_state.csv'))
    for state in res_country_state:
        state_id = lnk.execute(
            'res.country.state', 'search', [('name', '=', state['name']),
                                            ('country_id', '=', 229)])
        if not state_id:
            lnk.execute('res.country.state', 'create', state)
