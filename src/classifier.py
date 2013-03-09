#!/usr/local/bin/python

import sys
import csv
import math

def get_style_scores(prefs, groups):
    beer_scores=[]
    with open('../data/styles_brewerydb.csv', 'rbU') as csvfile, open ('../data/styles_flavors.csv', 'rbU') as flavfile:
        db = csv.DictReader(csvfile, quoting=csv.QUOTE_ALL)
        db_flavors = csv.DictReader(flavfile)
    
        for beer,flavors in zip(db, db_flavors):
            distance=0
            for category in prefs:
                if category in groups:
                    if prefs[category] == 1:
                        sum=0
                        for flavor in groups[category]:
                            sum+=int(flavors[flavor])
                        distance+=math.pow(len(groups[category])-sum,2)
                else:
                    if beer[category] is not '':
                        distance+=math.pow(abs(prefs[category]-float(beer[category])),2)
          
            distance=math.sqrt(distance)
            beer_scores.append((distance, beer['id']))

    beer_scores.sort()
    return beer_scores

def flavor_groupings():
    with open('../data/flavor_groups.csv', 'rbU') as csvfile:
        reader = csv.reader(csvfile, quotechar='|')
        groups={}
        for row in reader:
            flavors=row[1:]
            groups[row[0]]=flavors
    return groups

def get_inventory():
    with open ('../data/beers_inventory_brewerydb.csv', 'rbU') as csvfile:
        reader=csv.DictReader(csvfile, quoting=csv.QUOTE_ALL)
        beers={}
        for row in reader:
            if row['style_id'] in beers:
                beers[row['style_id']].append(row['id'])
            else:
                beers[row['style_id']]=[row['id']]
    return beers

def get_rec(beer_scores, inventory):
    recs=[]
    for beer in beer_scores:
        if beer[1] in inventory:
            recs.extend(inventory[beer[1]])
    return recs

# input = {'bitterness': int, 'flavor': int, 'color': int, 'Vanilla': int,
#          'Fruity': int, 'Earthy': int, 'Mineral': int, 'Toasty': int,
#          'Spices': int, 'Florals': int, 'Grainy': int, 'Creamy': int}
# output = list of beer IDs, where beer is in order of best matches
def main():

    groups = flavor_groupings()
    beer_scores = get_style_scores(sys.argv[0], groups)
    inventory=get_inventory()
    recommendations=get_rec(beer_scores, inventory)
    return recommendations

    """prefs = {'bitterness': 8, 'flavor': 9, 'color': 9, 'Vanilla': 1, 'Fruity': 1, 'Earthy': 1, 'Mineral': 0, 'Toasty': 0, 'Spices': 0, 'Florals': 0, 'Grainy': 0, 'Creamy': 0}
    groups = flavor_groupings()
    beer_scores = get_style_scores(prefs, groups)
    inventory=get_inventory()
    recommendations=get_rec(beer_scores, inventory)
    for rec in recommendations:
        print rec"""

if __name__ == "__main__":
    main()