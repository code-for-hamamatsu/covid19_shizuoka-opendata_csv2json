# main_summary
# 検査陽性者の状況

import covid19_util
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def convert2json(csvData, dtUpdated):
    try:
        logger.info(dtUpdated)
        logger.info(csvData)

        listCnt = csvData["検査実施人数"]
        listPosi = csvData["陽性患者数"]
        listHosp = csvData["入院中"]
        listMild = csvData["軽症・中軽症"]
        listServ = csvData["重症"]
        listDischa = csvData["退院"]
        listDeath = csvData["死亡"]

        sumCnt = 0
        sumPosi = 0
        sumHosp = 0
        sumMild = 0
        sumServ = 0
        sumDischa = 0
        sumDeath = 0

        for n in range(len(listCnt)):
            if covid19_util.is_nan(listCnt[n]): sumCnt = sumCnt
            else: sumCnt = sumCnt + listCnt[n]
            
            if covid19_util.is_nan(listPosi[n]): sumPosi = sumPosi
            else: sumPosi = sumPosi + listPosi[n]

            if covid19_util.is_nan(listHosp[n]): sumHosp = sumHosp
            else: sumHosp = sumHosp + listHosp[n]

            if covid19_util.is_nan(listMild[n]): sumMild = sumMild
            else: sumMild = sumMild + listMild[n]

            if covid19_util.is_nan(listServ[n]): sumServ = sumServ
            else: sumServ = sumServ + listServ[n]

            if covid19_util.is_nan(listDischa[n]): sumDischa = sumDischa
            else: sumDischa = sumDischa + listDischa[n]

            if covid19_util.is_nan(listDeath[n]): sumDeath = sumDeath
            else: sumDeath = sumDeath + listDeath[n]

        return{"attr": "検査実施人数","value": int(sumCnt),"children": [{"attr": "陽性患者数","value": int(sumPosi),"children": [{"attr": "入院中","value": int(sumHosp),"children": [{"attr": "軽症・中等症","value": int(sumMild)},{"attr": "重症","value": int(sumServ)}]},{"attr": "退院","value": int(sumDischa)},{"attr": "死亡","value": int(sumDeath)}]}]}

    except Exception as e:
        logger.exception(e)
        return None
        