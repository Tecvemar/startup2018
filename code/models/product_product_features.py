# -*- encoding: utf-8 -*-
import csv


def common_product_product_features(lnk):
    product_product_features = csv.DictReader(
        open('../data/common/product_product_features.csv'))
    for feature in product_product_features:
        feature_id = lnk.execute(
            'product.product.features', 'search', [
                ('name', '=', feature['name']),
                ('type', '=', feature['type'])])
        if not feature_id:
            lnk.execute('product.product.features', 'create', feature)
