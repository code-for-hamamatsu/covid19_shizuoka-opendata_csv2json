import os
import os.path
import pandas as pd
import requests
import io
import json
import pytz
from datetime import date, datetime

import covid19_main_summary
import covid19_patients
import covid19_patients_summary
import covid19_inspection_persons
import covid19_contacts

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

SUPPORTED_TYPE = "main_summary:a3122ca8-a30b-4f64-ab17-a6fe95d46fba,patients_summary:92f9ebcd-a3f1-4d5d-899b-d69214294a45,inspection_persons:d4827176-d887-412a-9344-f84f161786a2,contacts:1b57f2c0-081e-4664-ba28-9cce56d0b314,patients:5ab47071-3651-457c-ae2b-bfb8fdbe1af1"
SUPPORTED_TYPE_ARY = SUPPORTED_TYPE.split(",")

def lambda_handler(event, context):
    try:  
        logger.info("-----")
        logger.info(json.dumps(event))
        result = {}

        types = SUPPORTED_TYPE
        if event is not None:
            qsp = event["queryStringParameters"]
            if qsp is not None and qsp["type"] is not None:
                types = event["queryStringParameters"]["type"]
            
        logger.info(types)
        dataList = types.split(",")
        for data in dataList:
            logger.info(data)
            tmp = data.split(":")
            type = tmp[0]
            apiID = tmp[1]
            
            csvData, dtUpdated = getCSVData("https://opendata.pref.shizuoka.jp/api/package_show?id=" + apiID)
            if type == "main_summary":
                # 検査陽性者の状況
                result[type] = covid19_main_summary.convert2json(csvData, dtUpdated)

            elif type == "patients":
                # 検査陽性患者の属性
                result[type] = covid19_patients.convert2json(csvData, dtUpdated)

            elif type == "patients_summary":
                # 検査陽性患者数
                result[type] = covid19_patients_summary.convert2json(csvData, dtUpdated)
                
            elif type == "inspection_persons":
                # PCR検査実施人数
                result[type] = covid19_inspection_persons.convert2json(csvData, dtUpdated)
                
            elif type == "contacts":
                # 新型コロナに関する相談件数
                result[type] = covid19_contacts.convert2json(csvData, dtUpdated)

            else:
                result[type] = "not supported..."
                
        logger.info(result)
        return {
            "statusCode": 200,
            "body": json.dumps(result, ensure_ascii=False, indent=2)
        }
    except Exception as e:
        logger.exception(e)
        return {
            "statusCode": 500,
            "body": "error"
        }

def getCSVData(apiAddress):
    try:
        apiResponse = requests.get(apiAddress).json()
        resources = apiResponse["result"]["resources"]
        
        apiResources = None
        csvAddress = None
        for i in range(len(resources)):
            apiResources = resources[i]
            csvAddress = apiResources["download_url"]
            root, ext = os.path.splitext(csvAddress)
            if ext.lower() == ".csv":
                logger.info(csvAddress)
                break
        
        # タイムゾーン +09:00 -> +0900 for strptime %f
        dateStr = apiResources["updated"][:-3] + apiResources["updated"][-2:]
        dtUpdated = datetime.strptime(dateStr, "%Y-%m-%dT%H:%M:%S.%f%z")
        logger.info(dtUpdated)

        res = requests.get(csvAddress).content
        csvData = pd.read_csv(io.StringIO(res.decode("shift-jis")), sep=",", engine="python")
        return csvData, dtUpdated

    except Exception as e:
        logger.exception(e)
        return None, None