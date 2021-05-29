# patients
# 検査陽性者の状況(陽性患者の属性より)

import re
import covid19_util
import time
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def convert2json(csvData, dtUpdated):
    try:
        timeStart = time.perf_counter()
        #main_summary.pyの変数を流用
        listStatus = csvData["患者_状態"] #症状別入院数カウントに利用
        listDischa = None #入院数/退院数カウントに利用
        try:
            listDischa = csvData["患者_退院済フラグ"]
        except Exception as e:
            # 浜松市
            listDischa = csvData["退院済フラグ"]

        sumPosi = 0 #陽性患者数
        sumHosp = 0 #入院中
        sumMild = 0 #軽症・中軽症 + 無症状
        sumServ = 0 #重症
        sumDischa = 0 #退院
        sumDeath = 0 #死亡

            
        #陽性患者＝リストの要素数
        sumPosi = len(csvData)

        for n in range(len(csvData)):
            #入院中患者のカウント
            if covid19_util.is_nan(listDischa[n]): sumHosp = sumHosp
            elif listDischa[n] == 0: sumHosp += 1

            #軽症・中等症者のカウント
            if covid19_util.is_nan(listStatus[n]): sumMild = sumMild
            elif (listStatus[n] == "軽症" or listStatus[n] == "中等症" or listStatus[n] == "無症状") and listDischa[n] == 0 : sumMild += 1

            #重症者のカウント
            if covid19_util.is_nan(listStatus[n]): sumServ = sumServ
            elif (listStatus[n] == "重症") and listDischa[n] == 0 : sumServ += 1

            #退院者カウント
            if covid19_util.is_nan(listDischa[n]): sumDischa = sumDischa
            elif listDischa[n] == 1: sumDischa += 1

            #死亡
            if covid19_util.is_nan(listStatus[n]): sumDeath = sumDeath
            elif listStatus[n] == "死亡": sumDeath += 1
            
        timeCurr = time.perf_counter()
        logger.info("covid19_main_summary TIME = {0} sec".format((timeCurr - timeStart)))
        return{
            "date": dtUpdated.strftime('%Y/%m/%d %H:%M'), 
            "children": [
                {
                    "attr": "陽性患者数", 
                    "value": int(sumPosi), 
                    "children": [
                        {
                            "attr": "入院中", "value": int(sumHosp), 
                            "children": [
                                {"attr": "軽症・中等症", "value": int(sumMild)}, 
                                {"attr": "重症", "value": int(sumServ)}
                            ]
                        }, 
                        {"attr": "退院","value": int(sumDischa)}, 
                        {"attr": "死亡","value": int(sumDeath)}
                    ]
                }
            ]
        }

    except Exception as e:
        logger.exception(e)
        return None

def try2merge4xx(data, csvData):
    try:
        title = "死亡者人数"
        if title in csvData:
            cols = list(csvData[title])
            num = 0
            for i in range(len(cols)):
                tmp = cols[i]
                num = num + int(tmp)
            data["children"][0]["children"][2]["value"] = num
            # 退院から減算
            data["children"][0]["children"][1]["value"] = data["children"][0]["children"][1]["value"] - num
    except Exception as e:
        logger.exception(e)
