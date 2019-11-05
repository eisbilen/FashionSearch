import json
import logging
from pprint import pprint
import csv
from elasticsearch import Elasticsearch
import re
import ast
import os, base64, re, logging
import locale
from locale import LC_ALL, setlocale


### Site Map Generapor #######
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import datetime
from xml.etree import ElementTree
from xml.dom import minidom
from io import BytesIO
### Site Map Generapor #######

# Set to users preferred locale:
locale.setlocale(locale.LC_ALL, 'tr_TR')

print(locale.localeconv())

loc = locale.getlocale()
print(loc)
print (locale.atof("3,14"))

point = locale.localeconv()['decimal_point']
sep = locale.localeconv()['thousands_sep']

print("decimal point")
print(point)

### Site Map Generapor #######
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, encoding='utf8', method='xml')  
    ##reparsed = minidom.parseString(rough_string)   
    ##return reparsed.toprettyxml(indent="  ")
    return rough_string
### Site Map Generapor #######


def search(es_object, index_name, search):
    res = es_object.search(index=index_name, body=search)
    pprint(res)


def create_index(es_object, index_name):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "products": {
                "dynamic": "strict",
                "properties": {

                    "productId": {
                        "type": "text"
                    },
                    "gender": {
                        "type": "text",
                                    "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                }
                    },
                    "company": {
                        "type": "text",
                                    "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                }
                    },
                    "imageLink": {
                        "type": "text"
                    },

                    "priceOriginal": {
                        "type": "text",
                    },
                    "price": {
                        "type": "float",
                                    "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                }                        
                    },

                    "sale": {
                        "type": "float",
                                    "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                }                        
                    },

                     "priceSale": {
                        "type": "text" 
                    },
                    "productLink": {
                        "type": "text"
                    },
                    "productName": {
                        "type": "text",
                                    "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                }
                    }
                    }
                }
            }
        }

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_record(elastic_object, index_name, record):
    is_stored = True
    try:
        outcome = elastic_object.index(index=index_name, doc_type='products', body=record)
        print(outcome)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
        is_stored = False
    finally:
        return is_stored


def connect_elasticsearch():

    bonsai = "https://cwlc5wrbyr:97eb1ljnak@fashionsearch-test-2782075929.eu-central-1.bonsaisearch.net"
    auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
    host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

    #_es = None
    #_es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    
    es_header = [{
    'host': host,
    'port': 443,
    'use_ssl': True,

    'http_auth': (auth[0],auth[1])
     }]
    _es = Elasticsearch(es_header,use_ssl=True, verify_certs=True)


    if _es.ping():
        print('Yay Connected')
    else:
        print('Awww it could not connect!')
    return _es

if __name__ == '__main__':
    
    es = connect_elasticsearch()

    es.indices.delete(index="recipes", ignore=[400,404])

    i=0

    ### Site Map Generapor #######
    root = Element('urlset')
    root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    ### Site Map Generapor #######

    with open("/Users/erdemisbilen/Angular/fashionWebScraping/csvFiles/jsonFiles.csv", newline=None) as f:
            reader=csv.DictReader(f)
        
            for row in reader:

                jsonFile="/Users/erdemisbilen/Angular/fashionWebScraping/jsonFiles/"+row['file_name_final']


                with open(jsonFile) as json_file:  
                    data = json.load(json_file)
       
                    for p in data:

                        i=i+1
                        if i==9900:
                            i=i-1
                            break

                        if p['priceSale']==None:
                            p['priceSale']="0 TL"
                            p['sale']=0

                
                        p['priceOriginal'] = ''.join((ch if ch in '0123456789,.' else '') for ch in p['priceOriginal'])
                        p['priceSale'] = ''.join((ch if ch in '0123456789,.' else '') for ch in p['priceSale'])

                        if p['company']=="HM":
                            p['priceOriginal'] = ''.join((ch if ch in '0123456789,' else '') for ch in p['priceOriginal'])
                            p['priceSale'] = ''.join((ch if ch in '0123456789,' else '') for ch in p['priceSale'])                            

                        if p['priceSale']!="0":

                            p['priceSale']=p['priceSale'].replace(',','.')
                            p['priceSale']=p['priceSale'].replace(".", "", p['priceSale'].count(".") -1)

                            p['priceOriginal']=p['priceOriginal'].replace(',','.')
                            p['priceOriginal']=p['priceOriginal'].replace(".", "", p['priceOriginal'].count(".") -1)


                            p['price']=float(p['priceSale'])
                            p['sale']=(float(p['priceOriginal'])/p['price'])-1
                        else:
                            p['price']=float(p['priceOriginal'])
                            
                        # if p['priceSale']!="0":
                            
                        #     p['price']=p['priceSale'].replace("\x00", "")
                        #     print(p['price'])
                        #     p['price']=float(p['price'])
                        #     p['sale']=(float(p['priceOriginal'])/float(p['price']))-1
                        # else:
                        #     p['price']=float(p['priceOriginal'])
                        


                        #print repr(p['sale'])

                        rec = {'productId': p['productId'],'gender': p['gender'],'imageLink': p['imageLink'], 'priceOriginal': p['priceOriginal'], 'priceSale': p['priceSale'],'price': p['price'], 'sale': p['sale'],'productName': p['productName'], 'productLink':p['productLink'], 'company':p['company']}


                        url = SubElement(root, 'url')

                        loc = SubElement(url, 'loc')
                        loc.text="https://www.trendvar.com/product-search/" + p['productName']

                        #lastmod = SubElement(url, 'lastmod')
                        #lastmod.text="latmod1"

                        #changefreq = SubElement(url, 'changefreq')
                        #changefreq.text="changfred1"

                        #priority = SubElement(url, 'priority')
                        #priority.text="priority1"


                        #print('company: ' + p['company'])
                        
                        #print('gender: ' + p['gender'])
                        #print('adulthood: ' + p['adulthood'])

                        #print('productId: ' + p['productId'])
                        #print('imageLink: ' + p['imageLink'])
                        print('priceOriginal: ' + p['priceOriginal'])
                        print('priceSale: ' + p['priceSale'])
                        print(p['price'])
                        print(p['sale'])
                        print('productName: ' + p['productName'])
                        #print('productLink: ' + p['productLink'])
            
                        result= json.dumps(rec)

                        if es is not None:
                            if create_index(es, 'recipes'):
                                out = store_record(es, 'recipes', result)
                                #print('Data indexed successfully')
                                #print('---------------------------------------')
    
    sitemap = open("sitemap.xml", "wb")
    sitemap.write(prettify(root))

    if es is not None:
        # search_object = {'query': {'match': {'calories': '102'}}}
        # search_object = {'_source': ['title'], 'query': {'match': {'calories': '102'}}}
        search_object = {'_source': ['productName'], 'query': {'match': {'productName': 'siyah'}}}
        search(es, 'recipes', json.dumps(search_object))