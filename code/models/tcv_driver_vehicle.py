# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_tcv_driver_vehicle(lnk):

    c2o = csv_2_openerp(
        '../data/common/tcv_driver_vehicle.csv',
        'tcv.driver.vehicle', lnk)
    c2o.set_search_fields(['code', 'type'])
    c2o.set_boolean_fields(['active'])
    c2o.process_csv()
