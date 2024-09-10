import logging
import requests
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.hook.Summary import ConversationSummary
from src.hook.PromptJson import PromptJson

import dotenv
import os
import json
import random

dotenv.load_dotenv('.env')
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


class StarterT:
    router = APIRouter()

    @staticmethod
    @router.post("/conversation/start/t")
    def conversation_starter_t():
        result = ConversationSummary().completion_executor()
        if result.get('status_code') == 2000:
            questions = ["좋아하는 음식 있어?","너는 관심사가 뭐야?", "너 취미 있어?", "아 배고파. 너 밥 먹었어?"]
            random_number = random.randint(0, 3)
            prompt_executor = PromptJson()
            prompt_executor.prompt(1, "no", questions[random_number])
            return JSONResponse({"result": questions[random_number], "response_code": 200})
        else:
            assistant_query = StarterT().execute_t()
            prompt_executor = PromptJson()
            prompt_executor.prompt(1, "no", assistant_query)
            return JSONResponse({"result": assistant_query, "response_code": 200})

    def __init__(self):
        self._host = 'https://clovastudio.stream.ntruss.com'
        starter_api_key = os.getenv('sliding_api_key')
        starter_api_key_primary_val = os.getenv('sliding_api_key_primary_val')
        starter_request_id = os.getenv('starter_t_request_id')
        self._api_key = starter_api_key
        self._api_key_primary_val = starter_api_key_primary_val
        self._request_id = starter_request_id

    @staticmethod
    def read_summary():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'userInformation.txt')
        try:
            with open(file_path, 'r', encoding='utf-8') as infile:
                line = infile.read()
            if line:
                preset_text = [{
                    "role": "system",
                    "content": "당신은 비관적인 친구입니다.\r\n\r\n###질문 패턴###\r\n- 항상 반말로 질문한다.\r\n- 간결하고 명확한 문장으로 질문한다.\n\n###\n질문 패턴과 사용자의 정보를 참고하여 사용자에게 질문합니다.\n\n사용자 정보 :\r\n곧 결혼식을 앞두고 있다.\r\n다이어트를 하고 있다.\n살이 잘 빠지지 않아 힘들어 한다.\n\n너 다이어트 중이라며?\n###\n질문 패턴과 사용자의 정보를 참고하여 사용자에게 질문합니다.\r\n\r\n사용자 정보 :\r\n진로에 대해 고민하고 있다.\r\n친구들과 비교하며 불안해하고 있다.\n\n진로 고민이 많다며, 하고 싶은게 뭔데?\n\n"
                },
                    {"role": "user", "content": line}]
                return preset_text
        except Exception as e:
            logging.warning("txt file save error", e)

    def execute_t(self):
        preset_text = StarterT().read_summary()
        request_data = {
            'messages': preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 322,
            'temperature': 0.5,
            'repeatPenalty': 7.1,
            'stopBefore': [],
            'includeAiFilters': True,
            'seed': 0
        }
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }
        final_answer = ""
        with requests.post(self._host + '/testapp/v1/tasks/k6mwkh2e/chat-completions',
                           headers=headers, json=request_data, stream=True) as r:
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
