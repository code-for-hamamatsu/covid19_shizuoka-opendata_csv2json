# contacts
# 新型コロナに関する相談件数

import re
import covid19_util
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def convert2json(csvData, dtUpdated):
    try:
        listDate = csvData["受付_年月日"]
        listCnt = csvData["相談件数"]
        list = []
        
        length = len(listDate)
        for n in range(length):

            Date = re.split('[年月日:;.,-/]',  listDate[n])
            for i in (1,2): Date[i] = Date[i].zfill(2)
            day = Date[0]+"-"+Date[1]+"-"+ Date[2]

            cnt = listCnt[n]
            if not covid19_util.is_nan(cnt):
                list.append({'日付': "{0}T08:00:00.000Z".format(day), "小計": int(cnt)})

        return {"date": dtUpdated.strftime('%Y/%m/%d %H:%M'), "data": list}

    except Exception as e:
        logger.exception(e)
        return "raise exception..."
