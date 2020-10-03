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
def upsert_detail(db_client, id, name):
    #find if record is existed
    record = db_client[const.DB_COLLECTION_VN_INDUSTRY].find_one({'id':int(id)})
    if record is None:
        #not existed
        detail = {
            'id': int(id),
            'name': name
        }
        db_client[const.DB_COLLECTION_VN_INDUSTRY].insert_one(detail)
    else:
        #update name
        record['name'] = name;
        db_client[const.DB_COLLECTION_VN_INDUSTRY].update({'id':int(id)}, record)
    return
#######################
#parse detail page
def parse_page(db_client):
    page = ''
    page_url = 'http://sanotc.com'
    while page == '':
        try:
            page = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0'})
            break
        except:
            time.sleep(5)
            continue
    # print page.content
    tree = html.fromstring(page.content)
    tags = tree.xpath('//select[@id="s_cat_id"]/option')
    for tag in tags:
        upsert_detail(db_client, tag.attrib['value'], tag.text_content())

    return
#######################
client = MongoClient('localhost:27017')
db_client = client['otcmarket_vn']
start_time = getCurrentTimestamp()

parse_page(db_client)
#
end_time = getCurrentTimestamp()
total_time = end_time - start_time
print 'Total time: ' + str(total_time)