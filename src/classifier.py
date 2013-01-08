#!/usr/local/bin/python

import sys
import csv
import math

def create_database(prefs, groups):
    with open('../data/beermap.csv', 'rbU') as csvfile:
        db = csv.DictReader(csvfile, quotechar='|')
        shortest=sys.maxint
        beer_scores=[]
        for beer in db:
            distance=0
            for category in prefs:
                if category in groups:
                    sum=0
                    for flavor in groups[category]:
                        sum+=int(beer[category])
                    distance+=math.pow(abs(len(groups[category])-sum),2)
                else:
                    distance+=math.pow(abs(prefs[category]-float(beer[category])),2)
        
            distance=math.sqrt(distance)
        
            beer_scores.append((distance, beer['STYLE']))
            beer_scores.sort()
    return beer_scores

def flavor_groupings():
    with open('../data/flavorgrouping.csv', 'rbU') as csvfile:
        reader = csv.reader(csvfile, quotechar='|')
        groups={}
        for row in reader:
            flavors=row[1:]
            groups[row[0]]=flavors
    return groups

def main():
    
    questions=['bitterness', 'flavor', 'color', 'Vanilla', 'Fruity', 'Earthy', 'Mineral', 'Toasty', 'Spices', 'Florals', 'Grainy', 'Creamy']
    
    prefs = {'bitterness':2, 'flavor': 5, 'color': 5, 'Vanilla': 1, 'Fruity': 0, 'Earthy': 1, 'Mineral': 1, 'Toasty': 1, 'Spices': 0, 'Florals': 0, 'Grainy': 0, 'Creamy': 0}
    
    groups = flavor_groupings()
    
    suggestion = create_database(prefs, groups)
    for beer in suggestion:
        print beer

if __name__ == "__main__":
    main()