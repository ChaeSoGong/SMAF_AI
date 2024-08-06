# -*- coding: utf-8 -*-

import base64
import json
import http.client
import logging

import dotenv
import os

dotenv.load_dotenv('.env')
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
class SlidingWindow:
    def __init__(self):
        sliding_api_key = os.getenv('sliding_api_key')
        sliding_api_key_primary_val = os.getenv('sliding_api_key_primary_val')
        sliding_request_id = os.getenv('sliding_request_id')
        self._host = 'clovastudio.apigw.ntruss.com'
        self._api_key = sliding_api_key
        self._api_key_primary_val = sliding_api_key_primary_val
        self._request_id = sliding_request_id

    def _send_request(self, completion_request):
        try:

            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
                'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
                'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
            }

            conn = http.client.HTTPSConnection(self._host)
            conn.request('POST', '/v1/api-tools/sliding/chat-messages/HCX-DASH-001', json.dumps(completion_request),
                         headers)
            response = conn.getresponse()
            result = json.loads(response.read().decode(encoding='utf-8'))
            logging.warning(result)
            conn.close()
            return result
        except Exception as e:
            logging.error("er occurred: %s", e)


    def execute(self, data_list):
        try:
            request_data = json.loads("""{
              "maxTokens" : 200,
              "messages" : [ {
                "role" : "user",
                "content" : "hello"
              } ]
            }""", strict=False)
            # messages_json = json.dumps(data_list)
            # request_data = json.loads("""{
            #     "maxTokens" : 200,
            #     "messages" : %s
            # }""" % messages_json, strict=False)
            res = self._send_request(request_data)
            print(request_data)
            print(res)
            if res['status']['code'] == '20000':
                return res['result']['messages']
            else:
                return 'Error'

        except Exception as e:
            logging.error("An error occurred: %s", e)








