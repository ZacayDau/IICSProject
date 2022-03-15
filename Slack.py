import requests
import json

from OrientDB import OrientQuery

def SendMessage(txt):
    url = "https://hooks.slack.com/services/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"

    payload = json.dumps({
      "text":  txt
    })
    headers = {
      'Content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)


query="select * from COLUMN"
df=OrientQuery(query,"CustomerE2E")
SendMessage(df)



