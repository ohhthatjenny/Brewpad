# Gets inventory beers from BreweryDB using UPC. Output is a DB.

import sys
import csv
import requests
from brewerydb import *
import unicodedata


def get_beer(path, api_key, upc):
    full_path=path+'search/upc?code='+upc+'&key='+api_key
    response=requests.get(full_path)
    if 'data' in response.json():
        return response.json()['data'][0]

def main():
    api_key='94771e483e06142b0b8a7e1b8326bbc7'
    path='http://api.brewerydb.com/v2/'
    #BreweryDb.configure(api_key)
    
    fieldnames=('id','name','description', 'style_id','glass_id','glass_name','label', 'availability_id', 'availability_name', 'is_organic')
    f=open('../data/beers_inventory_brewerydb.csv', 'wt')
    writer=csv.DictWriter(f, fieldnames)
    headers = dict((n,n) for n in fieldnames)
    writer.writerow(headers)
    
    with open('../data/wegmans_inventory.csv', 'rbU') as inventory:
        reader = csv.reader(inventory, delimiter=' ', quotechar='|')
        for row in reader:
            print row

    beer=get_beer(path, api_key, '606905008303')
    entry={}
    entry['id']=beer['id']
    entry['name']=beer['name']
    entry['description']=beer['description']
    entry['style_id']=beer['style']['id']
    entry['glass_id']=beer['glass']['name']
    entry['glass_name']=beer['glass']['name']
    entry['label']=beer['labels']['large']
    entry['availability_id']=beer['available']['id']
    entry['availability_name']=beer['available']['name']
    entry['is_organic']=beer['isOrganic']
    print entry
    writer.writerow(entry)

#id
#name
#description
#glass:id
#glass:name
#style:id
#labels:large
#available:id
#available:name
#isOrganic


if __name__ == "__main__":
    main()