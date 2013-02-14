import sys
import json
import csv
from math import sqrt
from brewerydb import *
import unicodedata

def avg_var(style, var_max, var_min):
    return (float(style[var_max])+float(style[var_min]))/2.0

def meanstdv(styles, var_max, var_min):
    mean, count, std, max, min = 0, 0, 0, 0, sys.maxint
    for style in styles:
        if var_max in style and var_min in style:
            avg=avg_var(style, var_max, var_min)
            if avg < min:
                min=avg
            elif avg > max:
                max=avg
            mean+=(avg)
            count+=1
    mean = mean/count
    for style in styles:
        if var_max in style and var_min in style:
            avg=avg_var(style, var_max, var_min)
            std=std+(avg-mean)**2
    std=sqrt(std/(count-1))
    #max is how many std. devs. the max value is from the mean
    max=(max-mean)/std
    min=(mean-min)/std
    return mean,std,max,min

def get_scale(style, var_max, var_min, var, scale):
    style_var=(avg_var(style, var_max, var_min)-var[0])/var[1]
    if style_var < 0:
        style_var=style_var/var[3]*(scale/2.0)+(scale/2.0)
    else:
        style_var=style_var/var[2]*(scale/2.0)+(scale/2.0)
    return style_var


def make_csv(beer_styles, srm, ibu, abv, scale):
    style_db=[]
    fieldnames=('id','name','srm_min','srm_max','srm_avg','srm','ibu','abv')
    f=open('../data/styles_brewerydb.csv', 'wt')
    writer=csv.DictWriter(f, fieldnames)
    headers = dict( (n,n) for n in fieldnames )
    writer.writerow(headers)
    for style in beer_styles:
        entry={}
        entry['id']=style['id']
        entry['name']=unicodedata.normalize('NFKD', style['name']).encode('ascii','ignore')
        if 'srmMax' in style and 'srmMin' in style:
            entry['srm_min']=style['srmMin']
            entry['srm_max']=style['srmMax']
            entry['srm_avg']=avg_var(style, 'srmMax', 'srmMin')
        if 'srmMax' in style and 'srmMin' in style:
            entry['srm']=get_scale(style, 'srmMax', 'srmMin', srm, scale)
        if 'ibuMax' in style and 'ibuMin' in style:
            entry['ibu']=get_scale(style, 'ibuMax', 'ibuMax', ibu, scale)
        if 'abvMax' in style and 'abvMin' in style:
            entry['abv']=get_scale(style, 'abvMax', 'abvMin', abv, scale)
        style_db.append(entry)
    writer.writerows(style_db)
        

def main():
    apikey="94771e483e06142b0b8a7e1b8326bbc7"
    scale=10
    BreweryDb.configure(apikey)
    jsondata = BreweryDb.styles()
    beer_styles= jsondata['data']
    srm=meanstdv(beer_styles, 'srmMax', 'srmMin')
    ibu=meanstdv(beer_styles, 'ibuMax', 'ibuMin')
    abv=meanstdv(beer_styles, 'abvMax', 'abvMin')
    #fgMin, fgMax
    make_csv(beer_styles, srm, ibu, abv, scale)


if __name__ == "__main__":
    main()