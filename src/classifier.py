#!/usr/local/bin/python

import sys
import csv
import math

def get_substyle_scores(prefs, groups):
    beer_scores=[]
    with open('../data/beermap.csv', 'rbU') as csvfile:
        db = csv.DictReader(csvfile, quotechar='|')
        for beer in db:
            distance=0
            for category in prefs:
                if category in groups:
                    if prefs[category] == 1:
                        sum=0
                        for flavor in groups[category]:
                            sum+=int(beer[flavor])
                        distance+=math.pow(len(groups[category])-sum,2)            
                else:
                    distance+=math.pow(abs(prefs[category]-float(beer[category])),2)
        
            distance=math.sqrt(distance)
            beer_scores.append((distance, beer['STYLE']))
        print beer_scores
    beer_scores=beer_scores.sort()
    print beer_scores
    return beer_scores

def flavor_groupings():
    with open('../data/flavorgrouping.csv', 'rbU') as csvfile:
        reader = csv.reader(csvfile, quotechar='|')
        groups={}
        for row in reader:
            flavors=row[1:]
            groups[row[0]]=flavors
    return groups

def get_inventory(beer_scores):
    with open ('../data/wegmansbeer.csv', 'rbU') as csvfile:
        reader=csv.reader(csvfile)
        beers={}
        for row in reader:
            if row[0] in beers:
                beers[row[0]].append(row[2])
            else:
                beers[row[0]]=[row[2]]
    return beers

def get_rec(beer_scores, inventory):
    recs=[]
    print beer_scores
    for beer in beer_scores:
        recs.extend(inventory[beer[1]])
    print recs
    return recs


def main():
    
    questions=['bitterness', 'flavor', 'color', 'Vanilla', 'Fruity', 'Earthy', 'Mineral', 'Toasty', 'Spices', 'Florals', 'Grainy', 'Creamy']
    
    prefs = {'bitterness': 3, 'flavor': 3, 'color': 4, 'Vanilla': 0, 'Fruity': 0, 'Earthy': 1, 'Mineral': 0, 'Toasty': 1, 'Spices': 0, 'Florals': 0, 'Grainy': 0, 'Creamy': 0}
    
    groups = flavor_groupings()
    
    beer_scores = get_substyle_scores(prefs, groups)

    inventory=get_inventory(beer_scores)
    
    recommendations=get_rec(beer_scores, inventory)

if __name__ == "__main__":
    main()