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
        conn.close()
        return result

    def execute(self, data_list):

        try:
            request_data = {
                "maxTokens": 200,
                "messages": data_list
            }
            logging.warning(data_list)
            json_data = json.dumps(request_data)
            res = self._send_request(json_data)
            if res['status']['code'] == '20000':
                return res['result']['messages']
            else:
                return 'Error'
        except TypeError as e:
            logging.error("JSON serialization error: %s", e)
            logging.error("Data that caused the error: %s", data_list)

        # request_data = json.loads(json.dumps({
        #     "maxTokens": 200,
        #     "messages": data_list
        # }))
        #
        # res = self._send_request(request_data)
        # if res['status']['code'] == '20000':
        #     return res['result']['messages']
        # else:
        #     return 'Error'





