#parse latest posts
#http://lxml.de/lxmlhtml.html
from lxml import html

import requests
import time
from pymongo import MongoClient
import calendar
import const
import re
#extract vn phone number from text
def extract_phone_number_from_text(org_str):
    if org_str == "":
        return ""
    org_str = org_str.strip()
    raw_str = org_str.replace('.','').replace('-','')
    phones = re.findall(r'[\+\(]?[0-9][0-9 .\-\(\)]{8,}[0-9]', raw_str)
    new_phones = []
    for phone in phones:
        if phone is not None and phone is not '' and len(phone) < 15:
            new_phones.append(phone.replace(' ',''))
        else:
            new_phones.append(phone)
    return new_phones
#######################
def getCurrentTimestamp():
    return calendar.timegm(time.gmtime())
#######################
def extract_post_id(detail_url):
    if detail_url is None or detail_url is '':
        return ''
    item_index = detail_url.find('-item')
    html_index = detail_url.find('.html')
    return detail_url[item_index+len('-item'):html_index]
#######################
#upsert post detail
def upsert_detail(db_client, detail):
    #find if record is existed
    record = db_client[const.DB_COLLECTION_VN_POST].find_one({'post_id':detail['post_id']})
    detail['is_expired'] = 'false'
    detail['updated_time'] = getCurrentTimestamp()
    if record is None:
        #not existed
        detail['created_time'] = getCurrentTimestamp()
        detail['is_active'] = 'true'
        db_client[const.DB_COLLECTION_VN_POST].insert_one(detail)
    else:
        #update
        detail['type'] = record['type']
        detail['created_time'] = record['created_time']
        detail['is_active'] = record['is_active']
        if 'admin_node' in record:
            detail['admin_note'] = record['admin_note']
        if 'transaction_id' in record:
            detail['transaction_id'] = record['transaction_id']
        db_client[const.DB_COLLECTION_VN_POST].update({'post_id':detail['post_id']}, detail)
    return
####################### parse detail page of post
def parse_page_detail(page_url, detail):
    page = ''
    while page == '':
        try:
            page = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0'})
            break
        except:
            time.sleep(5)
            continue
    # print page.content
    tree = html.fromstring(page.content)
    detail_rows = tree.xpath('//div[@id="stockdetail"]/div/div[@class="row"]')
    row_index = 0
    for detail_row in detail_rows:
        if row_index == 4:
            #post date
            detail['post_date'] = detail_row.xpath('./div[@class="pull-left"]')[1].text_content().strip()
        if row_index == 5:
            #expire date
            detail['expire_date'] = detail_row.xpath('./div[@class="pull-left"]')[1].text_content().strip()
        row_index = row_index + 1
    #find description
    description = tree.xpath('//div[@id="stockdetail"]/div[@class="col-sm-12 marginBottom20"]/div[@class="row"]/p')
    detail['description'] = description[0].text_content().strip()
    detail['phones'] = extract_phone_number_from_text(detail['description'])
    return
####################### analyze each list of posts
def get_posts(type, posts, db_client, profile_urls):
    row_index = 0;
    for post in posts:
        if row_index == 0:
            row_index = row_index + 1
            continue;  #skip label row
        detail = {}
        cols = post.xpath('./td')
        col_index = 0
        for col in cols:
            if col_index == 0:
                #process first column only
                code_column = col.xpath('./a')
                profile_url = code_column[0].attrib['href']
                profile_urls.append(profile_url)
                #
                detail['url'] = code_column[1].attrib['href']   #original detail url
                parse_page_detail(detail['url'], detail)
                #
                detail['code'] = code_column[1].text_content().strip()
                detail['post_id'] = extract_post_id(detail['url'])
                detail['username'] = profile_url.replace('http://sanotc.com/profile/', '')
            if col_index == 1:
                detail['price'] = col.text_content().strip()
            if col_index == 2:
                detail['volume'] = col.text_content().strip()
            if col_index == 3:
                detail['display_time'] = col.text_content().strip()
            col_index = col_index + 1
        detail['type'] = type
        upsert_detail(db_client, detail)
    return
####################### parse homepage
def parse_page_list(db_client, profile_urls):
    page = ''
    page_url = 'http://sanotc.com/otc'
    while page == '':
        try:
            page = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0'})
            break
        except:
            time.sleep(5)
            continue
    # print page.content
    tree = html.fromstring(page.content)
    #sale posts
    sale_posts = tree.xpath('//div[@id="otclisting0"]/table/tr')
    get_posts('sale', sale_posts, db_client, profile_urls)
    #buy posts
    buy_posts = tree.xpath('//div[@id="otclisting1"]/table/tr')
    get_posts('buy', buy_posts, db_client, profile_urls)

    return
#######################
def parse_profile(db_client, profile_url):
    page = ''
    while page == '':
        try:
            page = requests.get(profile_url, headers={'User-Agent': 'Mozilla/5.0'})
            break
        except:
            time.sleep(5)
            continue
    # print page.content
    tree = html.fromstring(page.content)
    brokername = tree.xpath('//h2[@class="brokername"]')
    username = brokername[0].text_content().strip()
    #get phone & email
    broker_info = tree.xpath('//div[@class="row brokerinfo"]/div/b')
    phone = broker_info[0].text_content().strip()
    email = broker_info[1].text_content().strip()
    #upsert db
    if username is None or username is '':
        return
    #find if record is existed
    record = db_client[const.DB_COLLECTION_VN_USER].find_one({'username':username})
    if record is None:
        #not existed
        detail = {
            'username': username,
            'phone': phone,
            'email': email,
            'hide_phone': 'false',
            'hide_email': 'false',
            'name': username,   #default
            'created_time': getCurrentTimestamp(),
            'updated_time': getCurrentTimestamp(),
            'is_active': 'true',
            'source': 'sanotc'
        }
        db_client[const.DB_COLLECTION_VN_USER].insert_one(detail)
    else:
        #update
        record['updated_time'] = getCurrentTimestamp()
        if 'phone' in record:
            record['phone'] = phone
        if 'email' in record:
            record['email'] = email
        db_client[const.DB_COLLECTION_VN_USER].update({'username':username}, record)
    return
####################### main
client = MongoClient('localhost:27017')
db_client = client['otcmarket_vn']
start_time = getCurrentTimestamp()
profile_urls = []
parse_page_list(db_client, profile_urls)
if len(profile_urls) > 1:
    #remove duplicated urls
    profile_urls = list(dict.fromkeys(profile_urls))
    # print profile_urls
    for profile_url in profile_urls:
        parse_profile(db_client, profile_url)
#
end_time = getCurrentTimestamp()
total_time = end_time - start_time
print 'Total time: ' + str(total_time)