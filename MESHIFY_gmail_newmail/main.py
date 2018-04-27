import os
import boto3
import json
import urllib.request
import datetime
import time

gmail_url = "https://www.googleapis.com/gmail/v1/users/me/messages"

def handler(event, context):
    #remove credentials from event structure
    accesstoken = event['accesstoken']
    event['accesstoken']='***'

    print("event")
    print(event)

    yesterday = datetime.date.today() - datetime.timedelta(1)
    yesterday_tuple = yesterday.timetuple()
    yesterday_ts = str(int(time.mktime(yesterday_tuple)))
    params = urllib.parse.urlencode({'q': 'after:'+yesterday_ts})
    print(params)
    request = urllib.request.Request(gmail_url+'?'+params)
    request.add_header('Authorization','Bearer '+accesstoken)
    result = []
    try:
        with urllib.request.urlopen(request) as response:
            content = response.read()
            print(content)
            # {
            #  "messages": [
            #   {
            #    "id": "15f7250d08fbed4b",
            #    "threadId": "15ef189a104985b5"
            #   },
            #   {
            #    "id": "15ee7a3a9733ff3a",
            #    "threadId": "15ee7a3a9733ff3a"
            #   },
            maillist = json.loads(content)
            if "messages" in maillist:
                for mailentry in maillist['messages']:
                    result.append(mailentry)
    except urllib.error.HTTPError as e:
        if e.code in ( 403,404,405 ):
            print(e)
            error_message = e.read()
            print(error_message)
            raise e

    print(result)
    return result
