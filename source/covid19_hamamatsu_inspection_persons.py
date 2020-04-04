# inspection_persons
# PCR検査実施人数

import covid19_hamamatsu_util
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def convert2json(csvData, dtUpdated):
    try:
        logger.info(dtUpdated)
        logger.info(csvData)

        listDate = csvData["受付_年月日"]
        listCnt = csvData["人数"]
        labels = []
        dataList = []

        length = len(listDate)
        for n in range(length):
            day = listDate[n]
            cnt = listCnt[n]
            if covid19_hamamatsu_util.is_nan(cnt):
                cnt = int(0)
            labels.append("{0}T08:00:00.000Z".format(day))
            dataList.append(int(cnt))

        datasets = []
        datasets.append({"label": "PCR検査実施人数", "data": dataList})

        return {"date": dtUpdated.strftime('%Y/%m/%d %H:%M'), "labels": labels, "datasets": datasets}

    except Exception as e:
        logger.exception(e)
        return "raise exception..."
