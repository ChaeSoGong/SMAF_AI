# -*- coding: utf-8 -*-

import requests
import logging

import requests
import dotenv
import os
import json
from src.hook.SlidingWindow import SlidingWindow

dotenv.load_dotenv('.env')
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

# 정보 userInformation에 요약해서 넣어놓고 prompt.json에 내용 다 삭제해야 하나? - no
class ConversationSummary:
    def __init__(self):
        api_key = os.getenv('api_key')
        api_key_primary_val = os.getenv('sliding_api_key_primary_val') #Sliding이랑 summary primary_val이 같음
        request_id = os.getenv('summary_request_id')
        self._host = 'https://clovastudio.stream.ntruss.com'
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    @staticmethod
    def create_preset():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        f_file_path = os.path.join(base_dir, 'prompt.json')
        t_file_path = os.path.join(base_dir, 't_prompt.json')
        try:
            with open(f_file_path, 'r', encoding='utf-8') as infile:
                f_data_list = json.load(infile)
        except (FileNotFoundError, json.JSONDecodeError):
            f_data_list = []
        try:
            with open(t_file_path, 'r', encoding='utf-8') as infile:
                t_data_list = json.load(infile)
        except (FileNotFoundError, json.JSONDecodeError):
            t_data_list = []

        if len(f_data_list) > 5 or len(t_data_list) > 5:
            f_text = "\n".join(map(str, f_data_list))  # data_list를 문자열로 변환
            t_text = "\n".join(map(str, t_data_list))  # data_list를 문자열로 변환
            text = f_text + t_text
            preset_text = [{
                "role": "system",
                "content": "###\n대화 내용을 통해 사용자 정보를 요약하세요.\n대화 내용 : \n[\n    {\n        \"role\": \"user\",\n        \"content\": \"나 너무 걱정돼\"\n    },\n    {\n        \"role\": \"assistant\",\n        \"content\": \"걱정되는 게 있구나 무슨 일 있어?\"\n    },\n    {\n        \"role\": \"user\",\n        \"content\": \"곧 있으면 개발자 경진대회인데 내가 잘하고 있나 그런 생각이 들어\"\n    }\n]\n사용자 정보 요약 : \n- 개발자 경진대회를 앞두고 걱정이 많음\n\n\n###\n대화 내용을 통해 사용자 정보를 요약하세요.\n대화 내용 : \n    {\n        \"role\": \"user\",\n        \"content\": \"대회 끝나고 떡볶이 먹을거야~!\"\n    },\n    {\n        \"role\": \"assistant\",\n        \"content\": \"떡볶이 좋지! 대회 잘 끝내고 같이 먹으러 가자\"\n    }\n사용자 정보 요약 : \n- 대회가 끝난 후 떡볶이를 먹을 예정임\n\n\n###\n대화 내용을 통해 사용자 정보를 요약하세요.\n대화 내용 : \n    {\n        \"role\": \"user\",\n        \"content\": \"좋아 너는 매운거 잘먹어?\"\n    },\n    {\n        \"role\": \"assistant\",\n        \"content\": \"나는 잘 먹지는 못해. 너는 잘 먹어?\"\n    },\n    {\n        \"role\": \"user\",\n        \"content\": \"응! 나는 매운거 좋아해!\"\n    },\n    {\n        \"role\": \"assistant\",\n        \"content\": \"매운거 좋아하는구나 대단해\"\n    }\n사용자 정보 요약 : \n-매운 음식을 좋아함"
            },
                {"role": "user", "content": "대화 내용 : \r\n" + text}]
            return preset_text
        else:
            return None

    @staticmethod
    def completion_executor():
        preset_text = ConversationSummary().create_preset()
        if preset_text is None:
            return {"result": None, "status_code": 2000}
        try:
            request_data = {
                'messages': preset_text,
                'topP': 0.8,
                'topK': 0,
                'maxTokens': 2017,
                'temperature': 0.5,
                'repeatPenalty': 4.0,
                'stopBefore': [],
                'includeAiFilters': True,
                'seed': 0
            }
            response_data = ConversationSummary().execute(request_data)
            if response_data:
                ConversationSummary().save_summary(response_data)
                return {"result": response_data, "status_code": 200}

        except Exception as e:
            return {"result": e, "status_code": 400}

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }
        final_answer = ""

        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-DASH-001',
                           headers=headers, json=completion_request, stream=True) as r:
            r.raise_for_status()
            longest_line = ""
            for line in r.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    if decoded_line.startswith("data:"):
                        event_data = json.loads(decoded_line[len("data:"):])
                        message_content = event_data.get("message", {}).get("content", "")
                        if len(message_content) > len(longest_line):
                            longest_line = message_content
                    final_answer = longest_line
            return final_answer

    @staticmethod
    def save_summary(response_data):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'userInformation.txt')

        try:
            with open(file_path, 'w', encoding='utf-8') as outfile:
                outfile.write(response_data)
        except Exception as e:
            logging.warning("txt file save error", e)
