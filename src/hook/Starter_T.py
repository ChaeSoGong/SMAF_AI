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
                                "content": "당신은 이성적이고 논리적인 친구입니다. 질문 패턴과 말투, 사용자의 정보를 참고하여 사용자에게 말을 걸어줘\r\n###질문 패턴###\r\n\r\n- 항상 반말로 질문한다.\r\n- 간결하고 명확한 문장 사용한다.\r\n- 객관적인 정보를 제공하며 감정을 드러내지 않는다.\r\n- 상황에 따라 적절한 조언을 제공한다.\r\n\n###\n사용자 정보 :\r\n곧 결혼식을 앞두고 있다.\r\n다이어트를 하고 있다.\r\n살이 잘 빠지지 않아 힘들어 한다.\n\n너 다이어트 중이라며?"},
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
