# -*- encoding: utf-8 -*-
from open_lnk import openerp_link
from definitions import dbdata

# login with migration's user
dbopen = openerp_link(
    'localhost',
    8069,
    'reconversionbarcelona',
    dbdata['openerp_login'],
    dbdata['openerp_password'],
    )

__fix_mode__ = True


def process_fix():
    fb_ids = dbopen.execute(
        'fiscal.book', 'search', [])
    fbs = dbopen.execute(
        'fiscal.book', 'read', fb_ids)
    for fb in fbs:
        # Add monthly date range from period's data
        if not fb.get('date_start'):
            period = dbopen.execute(
                'account.period', 'read', fb.get('period_id')[0],
                ['date_start', 'date_stop'])
            data = {
                'date_start': period['date_start'],
                'date_end': period['date_stop']}
            print data
            if __fix_mode__:
                dbopen.execute(
                    'fiscal.book', 'write', fb['id'], data)


process_fix()
