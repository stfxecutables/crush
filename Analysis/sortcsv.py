import sys
import csv


def csv_itemgetter(index, delimiter=','):
    composite = lambda row: row.split(delimiter)[index]
    return composite

with open(sys.argv[1]) as file:
    for eachline in sorted(file, key=csv_itemgetter(2),reverse=True):
        print(eachline)


#tail -2250000 c2.csv |head
#cat correlations.csv | awk '$2 != "nan"' FS=','> c5.csv