# patients_summary
# 検査陽性患者数(陽性患者の属性より)

import json
import re
import covid19_util
import logging
import datetime
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import collections

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def convert2json(csvData, dtUpdated, increment=0):
    try:
        listDate = csvData["公表_年月日"]

        dataList = []
        
        today = datetime.date.today()
        dateStart = datetime.datetime(2020, 1, 29, 8, 0, 0) + datetime.timedelta(days=int(increment))
        dateEnd = today + relativedelta(hours=8, minutes=0, microseconds=0)
        days = (dateEnd - dateStart).days + 1
        
        for i in range(days):
            date = dateStart + datetime.timedelta(days=i)
            releaseday = date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
            dataList.append({"日付": releaseday, "小計": int(0)})
            
        counter = collections.Counter(listDate)
        
        for day in counter:
            num = counter[day]
            date = dt.strptime(day, "%Y-%m-%d")
            index = (date - dateStart).days
            dataList[index + 1]["小計"] = num
            
        return {"date": dtUpdated.strftime('%Y/%m/%d %H:%M'), "data": dataList}

    except Exception as e:
        logger.exception(e)
        return None
