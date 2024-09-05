import logging
import requests
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.hook.Summary import ConversationSummary
import dotenv
import os
import json

dotenv.load_dotenv('.env')
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


class StarterT:
    router = APIRouter()

    @staticmethod
    @router.post("/conversation/start/t")
    def conversation_starter_t():
        ConversationSummary().completion_executor()
        return JSONResponse({"result": StarterT().execute_t(), "response_code": 200})

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
                preset_text = [{"role": "system",
                                "content": "당신은 이성적인 스마트입니다. 질문 패턴과 성격을 참고해서 사용자에게 질문을 던집니다.\n사용자의 정보를 토대로 질문을 던져줘\r\n###질문 패턴### \r\n- 질문은 반말로 한다. \r\n- 질문은 짧게 한다. \r\n- 사용자의 정보 중 무작위로 하나에 대해 질문한다.\n###성격### \n이성적 : 원리, 원칙, 근거에 의한 의사결정을 내린다.\n논리적 : 스마트는 객관적인 기준을 두고 논리적인 판단을 우선시한다. \n분석적 : 사실을 근거로 분석한다.\n내향적 : 친구들을 여러 명 사귀는 것을 좋아하지 않는다. \n계획적 : 일을 미리 신중하게 계획한다.\n감각적 : 직감보다는 물리적 현실에 더 중점을 둔다.\n결과 중시 : 과정보다는 결과를 중시한다.\n비관적 : 어떤 기회에서도 최악의 상황을 가정한다.\r\n\n"},
                               {"role": "user",
                                "content": line}]
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
