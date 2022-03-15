

import requests
import json
import os
from datetime import date, datetime



class IICSApi:

    def __init__(self, user,password,baseApiUrl,operationUrl):
        self.user = user
        self.password = password
        self.baseApiUrl = baseApiUrl
        self.sessionID=self.login(operationUrl)


    def login(self,operationUrl):
        print("login...")

        try:
            url=self.baseApiUrl+operationUrl
            print(url)
            payload = json.dumps({
                "username": self.user,
                "password": self.password
            })
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            response = requests.request("POST",url , headers=headers, data=payload)
            # print(response.text)
            session = json.loads(response.text)["userInfo"]["sessionId"]
            print("end login")
        except Exception as e:
            print(e.__traceback__)

        return session


    def postRequest(self,requestUrl,payload,methodType,responseType):

        try:

            print("Start: {}{}".format(requestUrl,'...'))

            headers = {
                'Accept': 'application/json',
                'INFA-SESSION-ID': self.sessionID,
                'Content-Type': 'application/json'

            }
            response = requests.request( methodType, requestUrl, headers=headers, data=payload)
            if response.status_code!=200:
                print(response.status_code)
                return {"status":response.status_code,"body":response.reason}
            else:
                if responseType=="dict":
                    dictresult = json.loads(response.text)

                    print("End: {}".format(requestUrl))
                    return {"status": response.status_code, "body": dictresult}
                else:
                    return  {"status": response.status_code, "body": response.text}

        except Exception as e:
            print(e.__traceback__)
            return   {"status": 401, "body": e.__traceback__}




    def getAssets(self, operationUrl, fromDate):
        try:
            print(f'GetAssets from:',{fromDate})
            url = self.baseApiUrl+ operationUrl+ "?" + "updateTime>=" + fromDate
            print(url)
            dictResult=self.postRequest(url,"","GET","dict")
            if(dictResult["status"]==200 ):
                print(f"Number of Assets:", {dictResult["body"]["count"]})
                return dictResult["body"]



        except Exception as e:
            print(e.__traceback__)
            return None



    def getExportId(self,assetId,asseType,assetPath,operationUrl,dt_string):

        url = self.baseApiUrl + operationUrl
        print(url)
        assetName = assetPath.split("/")[-1]
        try:
            payload = json.dumps({
                "name": assetId + '_' + assetName + '_' + asseType + '_' + dt_string,
                "objects": [
                    {
                        "id": assetId,
                        "includeDependencies": False
                    }
                ]
            })

            dict=self.postRequest(url,payload,"POST","dict")
            if(dict["status"]==200):
                print(dict["body"]["status"])
                print("end ExportAssetJson")
                return dict["body"]["id"]
            else:
                print(dict["body"])
                return 401
        except Exception as e:
            print(e.__traceback__)
            return None




    def exportAssetJson(self,operationUrl,assetId,asseType,assetPath):
        print("ExportAssetJson...")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        jobID= self.getExportId(assetId,asseType,assetPath, operationUrl,dt_string)
        assetname=assetPath.split("/")[-1]
        filename=assetId+'_'+asseType+'_'+assetname+'.zip'
        if jobID!=401:
            url="{}{}{}{}/package".format(self.baseApiUrl,operationUrl,"/",jobID)
            stream= self.postRequest(url,"","GET","stream")
            if (not os.path.isdir('rawData')):
                os.mkdir('rawData')
            filename='rawData/{}'.format(filename)
            with open(filename, 'w') as f:
                print("create file:",filename)
                if(stream["status"]==200):
                    f.write(stream["body"])









class Program:

    def main(self):
        baseApiUrl = "https://usw5.dm-us.informaticacloud.com/saas"
        loginUrl="/public/core/v3/login"
        userName='zacay.daushin@gmail.com'
        password="Nadav2009"
        session=IICSApi(userName,password,baseApiUrl,loginUrl)

        assetsDict=session.getAssets("/public/core/v3/objects","2018-11-21T12:00.00Z")
        assetDictObj= assetsDict["objects"]
        [session.exportAssetJson("/public/core/v3/export",obj["id"], obj["type"],obj["path"]) for obj in  assetDictObj ]




pg=Program()
pg.main()

