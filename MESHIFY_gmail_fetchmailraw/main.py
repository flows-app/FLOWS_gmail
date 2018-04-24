import os
import boto3
import json
import urllib.request
import base64

gmail_url = "https://www.googleapis.com/gmail/v1/users/me/messages/"

def handler(event, context):
    print("event")
    print(event)
    accesstoken = event['accesstoken']
    mailid = event['mailid']

    request = urllib.request.Request(gmail_url+mailid+'?format=raw')
    request.add_header('Authorization','Bearer '+event['accesstoken'])
    result = []
    try:
        with urllib.request.urlopen(request) as response:
            content = response.read()
            print(content)
            # {
            #  "id": "15f7250d08fbed4b",
            #  "threadId": "15ef189a104985b5",
            #  "labelIds": [
            #   "IMPORTANT",
            #   "SENT"
            #  ],
            #  "snippet": "Hallo,...",
            #  "historyId": "3779670",
            #  "internalDate": "1509451399000",
            #  "sizeEstimate": 36334,
            #  "raw": "UmV0dXJuLVBhdGg..."
            # }
            mail = json.loads(content)
            msg = {
                "id": mailid,
                "content": base64.urlsafe_b64decode(content["raw"]).decode("utf-8")
            }
            result.append(msg)
    except urllib.error.HTTPError as e:
        if e.code in ( 403,404,405 ):
            print(e)
            error_message = e.read()
            print(error_message)
            raise e

    print(result)
    return result
