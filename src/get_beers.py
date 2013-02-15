# Gets inventory beers from BreweryDB using UPC. Output is a DB.

import sys
import csv
from brewerydb import *
import unicodedata


def main():
    apikey="94771e483e06142b0b8a7e1b8326bbc7"
    BreweryDb.configure(apikey)
    BreweryDb.search({'type':'beer','q':'unibroue'})

if __name__ == "__main__":
    main()