#!/usr/local/bin/python

import sys
import csv
from optparse import OptionParser

def create_database(prefs, groups):
    with open('../data/beermap.csv', 'rbU') as csvfile:
        db = csv.DictReader(csvfile, quotechar='|')
        shortest=sys.maxint
        match=""
        for beer in db:
            distance=0
            for category in prefs:
                if category in groups:
                    sum=0
                    for flavor in groups[category]:
                        sum+=int(beer[category])
                    distance+=abs(len(groups[category])-sum)
                else:
                    distance+=abs(prefs[category]-int(beer[category]))
        
            if distance<shortest:
                shortest=distance
                match=beer['STYLE']
    return match 

def flavor_groupings():
    with open('../data/flavorgrouping.csv', 'rbU') as csvfile:
        reader = csv.reader(csvfile, quotechar='|')
        groups={}
        for row in reader:
            flavors=row[1:]
            print flavors
            groups[row[0]]=flavors
    return groups

def main():
    
    questions=['bitterness', 'flavor', 'color', 'Vanilla', 'Fruity', 'Earthy', 'Mineral', 'Toasty', 'Spices', 'Florals', 'Grainy', 'Creamy']
    
    prefs = {'bitterness': 3, 'flavor': 3, 'color': 3, 'Vanilla': 1, 'Fruity': 1, 'Earthy': 1, 'Mineral': 1, 'Toasty': 1, 'Spices': 1, 'Florals': 1, 'Grainy': 1, 'Creamy': 1}
    
    groups = flavor_groupings()
    
    suggestion = create_database(prefs)

    print suggestion

if __name__ == "__main__":
    main()