import os
import boto3
import json
import urllib.request
import base64

gmail_url = "https://www.googleapis.com/gmail/v1/users/me/messages/"

def handler(event, context):
    #remove credentials from event structure
    accesstoken = event['accesstoken']
    event['accesstoken']='***'

    print("event")
    print(event)
    mailid = event['mailid']

    request = urllib.request.Request(gmail_url+mailid)
    request.add_header('Authorization','Bearer '+accesstoken)
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
            #         "value": "***@gmail.com"
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
            result.append(mail)
    except urllib.error.HTTPError as e:
        if e.code in ( 403,404,405 ):
            print(e)
            error_message = e.read()
            print(error_message)
            raise e

    print(result)
    return result
