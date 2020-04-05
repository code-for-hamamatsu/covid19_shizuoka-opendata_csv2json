import requests
import json

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

API_ADDRESS = "https://r4v2wcv8c2.execute-api.ap-northeast-1.amazonaws.com/work/process?type=patients:5ab47071-3651-457c-ae2b-bfb8fdbe1af1,inspection_persons:d4827176-d887-412a-9344-f84f161786a2,contacts:1b57f2c0-081e-4664-ba28-9cce56d0b314"

def process():
    try:  
        apiResponse = requests.get(API_ADDRESS)
        return apiResponse.text
    except Exception as e:
        logger.exception(e)
        return "error"
