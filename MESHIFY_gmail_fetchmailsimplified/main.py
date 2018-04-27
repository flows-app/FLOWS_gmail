import os
import boto3
import json
import urllib.request
import base64
import email
import datetime

gmail_url = "https://www.googleapis.com/gmail/v1/users/me/messages/"

def handler(event, context):
    print("event")
    print(event)
    accesstoken = event['accesstoken']
    mailid = event['mailid']

    request = urllib.request.Request(gmail_url+mailid)
    request.add_header('Authorization','Bearer '+event['accesstoken'])
    result = []
    try:
        with urllib.request.urlopen(request) as response:
            content = response.read()
            print(content)
            # {
            #   "id": "15f7250d08fbed4b",
            #   "threadId": "15ef189a104985b5",
            #   "labelIds": [ "IMPORTANT","SENT"],
            #   "snippet": "Hallo, ...",
            #   "historyId": "3779670",
            #   "internalDate": "1509451399000",
            #   "payload": {
            #     "partId": "",
            #     "mimeType": "multipart/alternative",
            #     "filename": "",
            #     "headers": [{
            #         "name": "Return-Path",
            #         "value": "\u003c****@gmail.com\u003e"
            #        },{
            #         "name": "Received",
            #         "value": "from [10.38.152.152] (pd95c76c2.dip0.t-ipconnect.de. [217.92.118.194])        by smtp.gmail.com with ESMTPSA id p28sm11082184wmf.2.2017.10.31.05.03.30"
            #        },{
            #         "name": "From",
            #         "value": "jens walter \u003c***@gmail.com\u003e"
            #        },{
            #         "name": "Content-Type",
            #         "value": "multipart/alternative; boundary=\"Apple-Mail=_7E3278BE-7361-47EC-A175-357E2D043B0D\""
            #        },{
            #         "name": "Mime-Version",
            #         "value": "1.0 (Mac OS X Mail 11.0 \\(3445.1.7\\))"
            #        },{
            #         "name": "Subject",
            #         "value": "Re: SEPA Überweisung"
            #        },{
            #         "name": "Date",
            #         "value": "Tue, 31 Oct 2017 13:03:19 +0100"
            #        },{
            #         "name": "References",
            #         "value": "\u003c6e6f766f.894836.00.303.1002010300.100132071709218.nmmail@***.de\u003e"
            #        },{
            #         "name": "To",
            #         "value": "***@***.de"
            #        },{
            #         "name": "In-Reply-To",
            #         "value": "\u003c6e6f766f.894836.00.303.1002010300.100132071709218.nmmail@***.de\u003e"
            #        },{
            #         "name": "Message-Id",
            #         "value": "\u003c774601A1-974F-49E3-AB92-41E963E44226@gmail.com\u003e"
            #        },{
            #         "name": "X-Mailer",
            #         "value": "Apple Mail (2.3445.1.7)"
            #        }
            #       ],
            #       "body": {"size": 0},
            #       "parts": [
            #        {
            #         "partId": "0",
            #         "mimeType": "text/plain",
            #         "filename": "",
            #         "headers": [
            #          {
            #           "name": "Content-Transfer-Encoding",
            #           "value": "quoted-printable"
            #          },
            #          {
            #           "name": "Content-Type",
            #           "value": "text/plain; charset=utf-8"
            #          }
            #         ],
            #         "body": {
            #          "size": 6691,
            #          "data": "SGFsbG..."
            #         }
            #        },
            #        {
            #         "partId": "1",
            #         "mimeType": "text/html",
            #         "filename": "",
            #         "headers": [
            #          {
            #           "name": "Content-Transfer-Encoding",
            #           "value": "quoted-printable"
            #          },
            #          {
            #           "name": "Content-Type",
            #           "value": "text/html; charset=utf-8"
            #          }
            #         ],
            #         "body": {
            #          "size": 25012,
            #          "data": "PGh0bWw-P..."
            #         }
            #        }
            #       ]
            #      },
            #      "sizeEstimate": 36334
            #     }

            mail = json.loads(content)
            msg = {
                "id": mailid,
                "messageId": "",
                "from": "",
                "to": [],
                "cc": [],
                "subject": "",
                "date": "",
                "body":{
                    "text": "",
                    "html": ""
                }
            }
            headers = mail['payload']['headers']
            tos=[]
            ccs=[]
            for header in headers:
                if header["name"]=="From":
                    x = email.utils.parseaddr(header["value"])
                    msg["from"]={"name":x[0],"address":x[1]}
                    if len(x[0])==0:
                        del msg["from"]["name"]
                if header["name"]=="Subject":
                    msg["subject"] = header["value"]
                if header["name"]=="Date":
                    #sample: Sun, 22 Apr 2018 17:23:57 +0900
                    #sample2: Sat, 21 Apr 2018 18:47:40 +0000 (UTC)
                    #sample3: 23 Apr 2018 17:25:02 +0200
                    dateVal = header["value"]
                    #preset with default value
                    dx=datetime.datetime.now()
                    for date_format in [
                        '%a, %d %b %Y %H:%M:%S %z',
                        '%d %b %Y %H:%M:%S %z',
                        '%a, %d %b %Y %H:%M:%S %z (%Z)']:
                        try:
                            dx=datetime.datetime.strptime(dateVal, date_format)
                        except ValueError:
                            pass

                    msg["date"] = dx.isoformat()
                if header["name"]=="To":
                    tos.append(header["value"])
                if header["name"]=="Cc":
                    ccs.append(header["value"])
                if header["name"]=="Message-Id" or header["name"]=="Message-ID":
                    msg["messageId"] = header["value"]
            addresses = email.utils.getaddresses(tos)
            for address in addresses:
                obj = {"name":address[0],"address":address[1]}
                if len(obj["name"])==0:
                    del obj["name"]
                msg["to"].append(obj)
            addresses = email.utils.getaddresses(ccs)
            for address in addresses:
                obj = {"name":address[0],"address":address[1]}
                if len(obj["name"])==0:
                    del obj["name"]
                msg["cc"].append(obj)
            if len(msg["cc"])==0:
                del msg["cc"]
            if len(msg["messageId"])==0:
                del msg["messageId"]
            #look for inline body
            if "body" in mail["payload"] and "size" in mail['payload']['body'] and mail['payload']['body']["size"]>0:
                data = mail['payload']['body']["data"]
                b = base64.urlsafe_b64decode(data)
                body_text = b.decode("utf-8")
                msg["body"]["text"] = body_text
                msg["body"]["html"] = body_text
            else:
                #look for multi mime
                parts = mail["payload"]["parts"]
                for part in parts:
                    if part["mimeType"]=="text/plain":
                        body_text = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                    if part["mimeType"]=="text/html":
                        body_html = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")

            result.append(msg)
    except urllib.error.HTTPError as e:
        if e.code in ( 403,404,405 ):
            print(e)
            error_message = e.read()
            print(error_message)
            raise e

    print(result)
    return result
