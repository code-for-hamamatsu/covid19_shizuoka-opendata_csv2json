# patients
# 検査陽性患者の属性

import re
import covid19_util
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def convert2json(csvData, dtUpdated):
    try:
        logger.info(dtUpdated)
        logger.info(csvData)

        listDate = csvData["公表_年月日"]
        listCity = csvData["市区町村名"]
        listResidence = csvData["患者_居住地"]
        listAge = csvData["患者_年代"]
        listSex = csvData["患者_性別"]
        listDischarge = csvData["退院済フラグ"]

        dataList = []

        for n in range(len(listDate)):

            Date = re.split('[年月日:;.,-/]',  listDate[n])
            for i in (1,2): Date[i] = Date[i].zfill(2)
            day = Date[0]+"-"+Date[1]+"-"+ Date[2]

            releaseday = "{0}T08:00:00.000Z".format(day)
            
            Residence = listResidence[n]
            if covid19_util.is_nan(Residence):
                Residence = "--"
            residence = listCity[n] + ' ' + Residence
            
            age = listAge[n]
            if covid19_util.is_nan(age):
                age = "不明"
                
            sex = listSex[n]
            if covid19_util.is_nan(sex):
                sex = "不明"
                
            discharge = int(listDischarge[n])
            if covid19_util.is_nan(discharge):
                discharge = "不明"

            dataList.append({"リリース日": releaseday, "居住地": residence, "年代": age, "性別": sex, "退院": discharge, "date": day})

        return {"date": dtUpdated.strftime('%Y/%m/%d %H:%M'), "data": dataList}

    except Exception as e:
        logger.exception(e)
        return None
