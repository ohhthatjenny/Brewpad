#!/usr/local/bin/python

import sys
import csv
from optparse import OptionParser

def create_database(prefs):
    with open('../beermap.csv', 'rb') as csvfile:
        db = csv.DictReader(csvfile, quotechar='|')
        shortest=99999
        match=""
        for beer in db:
            distance=0
            for category in prefs:
                distance+=abs(prefs[category]-beer[category])
            if distance<shortest:
                shortest=distance
                match=beer['STYLE']
    return db

def classify(prefs, db):
    n_neighbors = 1 #number of neighbors    
    print db.line_num
    print db
 

def main():
    
    prefs = {'Caramel': 1, 'Bitterness to Sweetness level (1 most sweet to 5 most bitter)': 3,
            '5 Full-bodied to 1 light': 3, 'Fruity':1}
    db = create_database(prefs)
    print prefs
    suggestion = classify(prefs, db)
    print db.fieldnames
    print db.line_num
    print suggestion

if __name__ == "__main__":
    main()