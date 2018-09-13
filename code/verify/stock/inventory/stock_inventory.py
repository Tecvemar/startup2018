# -*- encoding: utf-8 -*-
import csv

#~ def data_profit(data):
data = []
with open('2018/marzo.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print row
            data.append(row)
print data

    #~ data_profit(data)



