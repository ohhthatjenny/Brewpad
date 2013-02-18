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

def get_full_upc(upc):
    upc_str=str(upc)
    upc=[int(s) for s in upc_str]
    check_digit = 10-((upc[0]+upc[2]+upc[4]+upc[6]+upc[8]+upc[10])*3+upc[1]+upc[3]+upc[5]+upc[7]+upc[9]) % 10
    check_digit = (0 if check_digit==10 else check_digit)
    return upc_str+str(check_digit)
    
def main():
    api_key='94771e483e06142b0b8a7e1b8326bbc7'
    path='http://api.brewerydb.com/v2/'
    #BreweryDb.configure(api_key)
    
    fieldnames=('id','name','description', 'style_id','glass_id','glass_name','label', 'availability_id', 'availability_name', 'is_organic')
    f=open('../data/beers_inventory_brewerydb.csv', 'wt')
    writer=csv.DictWriter(f, fieldnames)
    headers = dict((n,n) for n in fieldnames)
    writer.writerow(headers)
    beer_db=[]
    with open('../data/wegmans_inventory.csv', 'rbU') as inventory:
        reader = csv.reader(inventory, delimiter=' ', quotechar='|')
        for row in reader:
            upc = [s for s in row[0] if s.isdigit()]
            upc=''.join(upc)
            upc= get_full_upc(upc)
            beer=get_beer(path, api_key, upc)
            
            if beer is not None and 'id' in beer and 'name' in beer and 'description' in beer and 'style' in beer:
                double = False
                
                #Make sure we don't add a beer twice
                for b in beer_db:
                    if b['id']==beer['id']:
                        double=True
            
                if not double:
                    entry={}
                    entry['id']=beer['id']
                    entry['name']=unicodedata.normalize('NFKD', beer['name']).encode('ascii','ignore')
                    entry['description']=unicodedata.normalize('NFKD', beer['description']).encode('ascii','ignore')
                    entry['style_id']=beer['style']['id']
                    if 'glass' in beer:
                        entry['glass_id']=beer['glass']['name']
                        entry['glass_name']=unicodedata.normalize('NFKD', beer['glass']['name']).encode('ascii','ignore')
                    if 'labels' in beer:
                        entry['label']=beer['labels']['large']
                    if 'available' in beer:
                        entry['availability_id']=beer['available']['id']
                        entry['availability_name']=unicodedata.normalize('NFKD', beer['available']['name']).encode('ascii','ignore')
                    if 'isOrganic' in beer:
                        entry['is_organic']=beer['isOrganic']
                    beer_db.append(entry)
    writer.writerows(beer_db)

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