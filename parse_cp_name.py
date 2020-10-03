#scrape names of OTC companies
#http://lxml.de/lxmlhtml.html
from lxml import html

import requests
import time
from pymongo import MongoClient
import calendar
import sys
import const

#######################
def getCurrentTimestamp():
    return calendar.timegm(time.gmtime())
#######################
#upsert movie detail
def upsert_detail(db_client, list):
    #find if stock is existed (soft deleted or not)
    for stock in list:
        record = db_client[const.DB_COLLECTION_VN_STOCKS].find_one({'raw_code':stock['code'].lower()})
        if record is None:
            #not existed
            detail = {
                'code': stock['code'],
                'raw_code': stock['code'].lower(),
                'name': stock['name'].strip()
            }
            db_client[const.DB_COLLECTION_VN_STOCKS].insert_one(detail)
        else:
            #update name
            record['name'] = stock['name'].strip();
            db_client[const.DB_COLLECTION_VN_STOCKS].update({'raw_code':stock['code'].lower()}, record)
    return
#######################
#parse detail page
def parse_page(char):
    url = 'http://sanotc.com/?sub=ajax&act=getjsonCP&loaihh=0&q='+char
    r = requests.get(url)
    return r.json()
#######################
client = MongoClient('localhost:27017')
db_client = client['otcmarket_vn']
start_time = getCurrentTimestamp()

index = 0
alpha_len = len(const.DB_COLLECTION_VN_STOCKS)
while index < alpha_len:
    list = parse_page(const.DB_COLLECTION_VN_STOCKS[index])
    index = index + 1
    upsert_detail(db_client, list)
#
end_time = getCurrentTimestamp()
total_time = end_time - start_time
print 'Total time: ' + str(total_time)