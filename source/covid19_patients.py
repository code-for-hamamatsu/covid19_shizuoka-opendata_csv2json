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

        listDate = csvData["公表_年月日"]
        listresidence = csvData["患者_居住地"]
        listage = csvData["患者_年代"]
        listsex = csvData["患者_性別"]
        listdischarge = csvData["退院済フラグ"]

        dataList = []

        for n in range(len(listDate)):

            if '/' in listDate[n]:
                Date= listDate[n].split("/")
                Date[1] = Date[1].zfill(2)
                Date[2] = Date[2].zfill(2)
                day = Date[0]+"-"+Date[1]+"-"+ Date[2]
            elif '-' in listDate[n]:
                Date= listDate[n].split("-")
                Date[1] = Date[1].zfill(2)
                Date[2] = Date[2].zfill(2)
                day = Date[0]+"-"+Date[1]+"-"+ Date[2]

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

        return {"date": dtUpdated.strftime('%Y/%m/%d %H:%M'), "data": dataList}

    except Exception as e:
        logger.exception(e)
        return "raise exception..."
