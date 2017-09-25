# -*- encoding: utf-8 -*-
from csv2open import csv_2_openerp


class openerp_2_openerp(csv_2_openerp):

    def __init__(self, model, lnk, open_lnk):
        super(openerp_2_openerp, self).('', model, lnk)
        self.dbopen = open_lnk
        self.model_ids = []

    def get_model_ids(self):

    def load_csv(self):
        if self.dbopen:

    def process_open_data(self):
        self.load_open_data()
