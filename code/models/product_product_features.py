# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


def load_product_product_features(lnk):
    c2o = csv_2_openerp(
        '../data/common/product_product_features.csv',
        'product.product.features', lnk)
    c2o.set_search_fields(['name', 'type'])
    c2o.process_csv()

#~ def common_product_product_features(lnk):
    #~ product_product_features = csv.DictReader(
        #~ open('../data/common/product_product_features.csv'))
    #~ for feature in product_product_features:
        #~ feature_id = lnk.execute(
            #~ 'product.product.features', 'search', [
                #~ ('name', '=', feature['name']),
                #~ ('type', '=', feature['type'])])
        #~ if not feature_id:
            #~ lnk.execute('product.product.features', 'create', feature)
