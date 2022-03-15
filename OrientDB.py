import requests
import json
import pandas as pd


def OrientQuery(query,database):


    url = "http://localhost:2480/command/CustomerE2E/sql"

    payload = json.dumps({
        "command": "select * from COLUMN"
    })
    headers = {
        'Authorization': 'Basic cm9vdDpyb290',
        'Content-Type': 'application/json',
        'Cookie': 'OSESSIONID=OS1647213389295-1231421075967031879'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    #data = json.loads(response.text)
    #df = pd.json_normalize(data['result'])

    return (response.text)







