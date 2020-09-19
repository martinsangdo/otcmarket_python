#https://otcmarket.herokuapp.com/
import requests
from pymongo import MongoClient
import const
import json
import calendar
import time
import os

#sync Contact from server to local db
#######################
def upsert_detail(db_client, detail):
    # detail['options'] = detail['options'].replace("\\", "")
    # detail['device_info'] = detail['device_info'].replace("\\", "")
    #find if document is existed (soft deleted or not)
    record = db_client[const.DB_COLLECTION_CONTACT].find_one({'_id':detail['_id']})
    if record is None:
        #not existed
        db_client[const.DB_COLLECTION_CONTACT].insert_one(detail)
        #send mail
        send_mail(detail)
    else:
        if 'sent_mail_time' in record:
            detail['sent_mail_time'] = record['sent_mail_time']
        db_client[const.DB_COLLECTION_CONTACT].update({'_id':detail['_id']}, detail)
    return
#######################
def send_mail(detail):
    user_email = detail['email'].replace('@', '#')
    #compose message
    body_content = ''
    body_content = body_content + 'From: '+detail['email']+'\n\n'
    options = json.loads(detail['options'])
    options_str = ''
    for key in options:
        options_str = options_str + key+': '+str(options[key])+'\n'
    body_content = body_content + options_str
    body_content = body_content + '\nCreate time: '+detail['create_time']+'\n'
    subject = const.SUBJECT_FREFIX+user_email
    # subject = subject + '\nContent-type:text/html;charset=utf-8'
    # print body_content
    os.system('echo "'+body_content+'" | mail -s '+subject+' '+const.RECEIVER_MAIL)
    #todo: log sent mail time

    return
#######################
def getCurrentTimestamp():
    return calendar.timegm(time.gmtime())
#######################

url = "https://otcmarket.herokuapp.com/contact/list"
r = requests.get(url)
raw_data = r.json()

if raw_data is not None:
    list = raw_data['list']
    if list is not None:
        client = MongoClient(const.HOSTNAME+':'+const.PORT)
        db_client = client[const.DATABASE]
        for contact in list:
            upsert_detail(db_client, contact)