import requests
import json

url = "https://usw5.dm-us.informaticacloud.com/saas/public/core/v3/export"

payload = json.dumps({
  "name": "5ZjDKSfkhf1bigbY4m1JUi_Add-On Bundles_Project_15/03/2022 07:32:46",
  "objects": [
    {
      "id": "fPySJsvQe0KfKDpaeycuyx",
      "includeDependencies": False
    }
  ]
})
headers = {
  'INFA-SESSION-ID': '9T34VHv2bKvlg3ZimUQqMj',
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
