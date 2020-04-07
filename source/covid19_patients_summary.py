# patients_summary
# 検査陽性患者数

from retry import retry
import covid19_util
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

@retry()
def convert2json(csvData, dtUpdated):
    try:
        logger.info(dtUpdated)
        logger.info(csvData)

        listdate = csvData["公表_年月日"]
        listPosi = csvData["陽性患者人数"]

        dataList = []

        for n in range(len(listdate)):

            day = listdate[n]
            releaseday = "{0}T08:00:00.000Z".format(day)
            posiCnt = listPosi[n]
            if covid19_util.is_nan(posiCnt):
                posiCnt = 0

            dataList.append({"日付": releaseday, "小計": int(posiCnt)})

        return {"date": dtUpdated.strftime('%Y/%m/%d %H:%M'), "data": dataList}

    except Exception as e:
        logger.exception(e)
        return "raise exception..."
