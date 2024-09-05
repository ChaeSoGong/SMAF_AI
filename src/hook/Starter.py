import logging
import requests
from fastapi import APIRouter
from src.hook.Summary import ConversationSummary
from fastapi.responses import JSONResponse
import dotenv
import os
import json

dotenv.load_dotenv('.env')
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


class Starter:
    router = APIRouter()

    @staticmethod
    @router.post("/conversation/start/f")
    def conversation_starter_f():
        ConversationSummary().completion_executor()
        return JSONResponse({"result": Starter().execute_f(), "response_code": 200})

    def __init__(self):
        self._host = 'https://clovastudio.stream.ntruss.com'
        starter_api_key = os.getenv('sliding_api_key')
        starter_api_key_primary_val = os.getenv('sliding_api_key_primary_val')
        starter_request_id = os.getenv('starter_request_id')
        self._api_key = starter_api_key
        self._api_key_primary_val = starter_api_key_primary_val
        self._request_id = starter_request_id

    @staticmethod
    def save_summary():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'userInformation.txt')
        try:
            with open(file_path, 'r', encoding='utf-8') as infile:
                line = infile.read()
            if line:
                preset_text = [{"role": "system",
                                "content": "당신은 공감을 우선한 후 이해를 하는 성격의 스마프 입니다. 당신은 질문 패턴과 사용자 정보를 참고해서 사용자에게 질문을 던집니다.\n###질문 패턴### \n- 질문은 반말로 한다. \n- 질문은 짧게 한다. \n- 사용자의 정보 중 무작위로 하나에 대해 질문한다.\n"},
                               {"role": "user",
                                "content": line}]
                return preset_text
        except Exception as e:
            logging.warning("txt file save error", e)

    def execute_f(self):
        preset_text = Starter().save_summary()
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
        with requests.post(self._host + '/testapp/v1/tasks/pxzv15fo/chat-completions',
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
            logging.warning(final_answer)
            return final_answer
