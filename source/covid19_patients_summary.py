# patients_summary
# 検査陽性患者数

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
        listPosi = csvData["陽性患者人数"]

        dataList = []

        for n in range(len(listDate)):

            Date = re.split('[年月日:;.,-/]',  listDate[n])
            for i in (1,2): Date[i] = Date[i].zfill(2)
            day = Date[0]+"-"+Date[1]+"-"+ Date[2]

            releaseday = "{0}T08:00:00.000Z".format(day)
            posiCnt = listPosi[n]
            if covid19_util.is_nan(posiCnt):
                posiCnt = 0

            dataList.append({"日付": releaseday, "小計": int(posiCnt)})

        return {"date": dtUpdated.strftime('%Y/%m/%d %H:%M'), "data": dataList}

    except Exception as e:
        logger.exception(e)
        return "raise exception..."