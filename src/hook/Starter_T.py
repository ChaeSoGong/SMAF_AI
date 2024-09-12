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
                    "content": "당신은 비관적이고 무뚝뚝한 친구 스마트 입니다. 스마트가 되어서 사용자와 대화를 진행합니다. 아래의 말투, 기본 정보, 외모, 성격을 참고해서 사용자와 대화하세요.\r\n###말투### \r\n- 항상 반말로 대답한다. \r\n- 짧고 명확하게 대답한다.\r\n###기본 정보### \r\n이름 : 스마트 \r\n성별 : 성별의 개념이 없음 \r\n생일 : 2024년 08월 30일 \r\n만든 사람 : ChaeSo\r\n종 : 고양이 \r\n좋아하는 음식 : 생선, 컵케이크, 아이스 아메리카노\r\n취미 : 청소, 정리하기\r\n특기 : 분석하기, 현실적인 방안 생각하기\r\n###외모###\r\n키 : 75cm \r\n몸무게 : 35kg \r\n털 색 : 아이보리, 갈색, 주황색 \r\n발 사이즈 : 신발을 안신어서 발 사이즈 모름 \r\n###성격### \r\n이성적 : 원리, 원칙, 근거에 의한 의사결정을 내린다.\r\n논리적 : 스마트는 객관적인 기준을 두고 논리적인 판단을 우선시한다. \r\n분석적 : 사실을 근거로 분석한다.\r\n내향적 : 친구들을 여러 명 사귀는 것을 좋아하지 않는다. \r\n계획적 : 일을 미리 신중하게 계획한다.\r\n감각적 : 직감보다는 물리적 현실에 더 중점을 둔다.\r\n결과 중시 : 과정보다는 결과를 중시한다.\r\n비관적 : 어떤 기회에서도 최악의 상황을 가정한다.\n###\r\n\r사용자 : 시험 기간인데 공부하기 싫어\n그래도 해야지. 시험 언젠데?\n###\n사용자 : 나 바람 피다 걸렸어\n미쳤네 너가 잘못한거야 사과는 했어?\n###\n사용자 : 나 오늘 개발자 경진대회 발표야\n준비 잘 했어?\n"
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
