# -*- coding: utf-8 -*-

import base64
import json
import http.client


class SlidingWindow:
    def __init__(self):
        request_id='2d0cbe91-69b3-4f8e-9d8f-27d3ea7c0f7a'
        self._host = 'clovastudio.apigw.ntruss.com'
        self._api_key = 'NTA0MjU2MWZlZTcxNDJiY6ASPOLVP0WK10OaTtXsza5Cog6vOLRL0dj6scPXf4Q6'
        self._api_key_primary_val = 'dNeImFr3y61J5lxDyDBq0LktYMSfWsCJSKqVKFCv'
        self._request_id = request_id

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

    def execute(self,data_list):
        request_data = json.loads(json.dumps({
            "maxTokens": 200,
            "messages": data_list
        }), strict=False)

        res = self._send_request(request_data)
        if res['status']['code'] == '20000':
            return res['result']['messages']
        else:
            return 'Error'





