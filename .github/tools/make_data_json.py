import requests
import json

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

API_QUERY_PRM = "main_summary:a3122ca8-a30b-4f64-ab17-a6fe95d46fba,patients:5ab47071-3651-457c-ae2b-bfb8fdbe1af1,patients_summary:92f9ebcd-a3f1-4d5d-899b-d69214294a45,inspection_persons:d4827176-d887-412a-9344-f84f161786a2,contacts:1b57f2c0-081e-4664-ba28-9cce56d0b314"

def process(apiAddress, apiKey):
    try:
        apiResponse = requests.get("{0}?type={1}".format(apiAddress, API_QUERY_PRM), headers={"x-api-key": apiKey})
        
        di = json.loads(apiResponse.text)
        if(di["hasError"]):
            raise Exception("has error")

        return apiResponse.text
    except Exception as e:
        logger.exception(e)
        raise e
