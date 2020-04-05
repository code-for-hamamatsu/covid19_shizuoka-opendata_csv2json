# patients
# 検査陽性患者の属性

import covid19_util
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def convert2json(csvData, dtUpdated):
    try:
        logger.info(dtUpdated)
        logger.info(csvData)

        print(dtUpdated)

        listdate = csvData["公表_年月日"]
        listresidence = csvData["患者_居住地"]
        listage = csvData["患者_年代"]
        listsex = csvData["患者_性別"]
        listdischarge = csvData["退院済フラグ"]

        dataList = []

        for n in range(len(listdate)):

            day = listdate[n]
            releaseday = "{0}T08:00:00.000Z".format(day)
            residence = listresidence[n]
            age = listage[n]
            if covid19_util.is_nan(age):
                age = "不明"
            sex = listsex[n]
            if covid19_util.is_nan(sex):
                sex = "不明"
            discharge = int(listdischarge[n])
            if covid19_util.is_nan(discharge):
                discharge = "不明"

            dataList.append({"リリース日": releaseday, "居住地": residence, "年代": age, "性別": sex, "退院": discharge, "date": day})

        print(dataList)

        return {"date": dtUpdated.strftime('%Y/%m/%d %H:%M'), "data": dataList}

    except Exception as e:
        logger.exception(e)
        return "raise exception..."
