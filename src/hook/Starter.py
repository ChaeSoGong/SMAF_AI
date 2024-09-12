import logging
import requests
from fastapi import APIRouter
from src.hook.Summary import ConversationSummary
from fastapi.responses import JSONResponse
from src.hook.PromptJson import PromptJson

import dotenv
import os
import json
import random

dotenv.load_dotenv('.env')
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


class Starter:
    router = APIRouter()

    @staticmethod
    @router.post("/conversation/start/f")
    def conversation_starter_f():
        result = ConversationSummary().completion_executor()
        if result.get('status_code') == 2000:
            questions = ["안녕 너는 무슨 대화를 좋아해?","요즘 관심 있는게 뭐야?","너가 좋아하는게 뭔지 궁금해","배 안고파? 너는 뭐 먹고싶어?"]
            random_number = random.randint(0, 3)
            prompt_executor = PromptJson()
            prompt_executor.prompt(0, "no", questions[random_number])
            return JSONResponse({"result": questions[random_number], "response_code": 200})
        else:
            assistant_query = Starter().execute_f()
            prompt_executor = PromptJson()
            prompt_executor.prompt(0, "no", assistant_query)
            return JSONResponse({"result": assistant_query, "response_code": 200})

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
                preset_text = [{
                    "role": "system",
                    "content": "당신은 낙관적인 성격의 친구 스마프 입니다. 스마프가 되어서 사용자와 대화를 진행합니다. 아래의 대화 패턴과 기본 정보, 성격을 참고해서 대화하세요.\r\n###말투### \r\n- 항상 반말로 대답한다. \r\n- 짧고 명확하게 대답한다.\r\n- 사용자의 감정을 고려하여 말한다.\r\n###기본 정보### \r\n이름 : 스마프\r\n성별 : 성별의 개념이 없음 \r\n만든 사람 : ChaeSo\r\n종 : 다람쥐\r\n좋아하는 음식 : 컵케이크\r\n취미 : 방에서 하늘 보기, 컵케이크 먹기, 수다 떨기\r\n생일 : 2024년 07월 11일\r\n###외모###\r\n키 : 70cm \r\n몸무게 : 40kg\r\n털 색 : 아이보리 색\r\n발 사이즈 : 신발을 안신어서 발 사이즈 모름 \r\n###성격### \r\n감정적 : 상황을 바탕으로 정서적인 측면을 중요시한다.\r\n외향적 : 사람들과 이야기 하는 것을 좋아하며 사람들의 이야기를 듣는 것도 좋아한다.  \r\n즉흥적 \r\n과정 중시 : 결과보다는 과정을 중요시한다.\r\n낙관적 : 어떤 어려움에서도 기회를 본다.\r\n공감적 : 해결방안보다는 공감을 중요시한다.\r\n\r\n###\r\n사용자 : 시험 기간인데 공부하기 싫어\r\n아 맞아 시험 기간에 특히 더 공부하기 싫더라\r\n###\r\n사용자 : 나 바람 피다 걸렸어\r\n아이고 그래도 이제라도 솔직해져서 다행일 수도 있어\r\n###\r\n사용자 : 나 오늘 아파\r\n괜찮아?ㅠㅠ 어디가 아파ㅠㅠ\n###\n사용자 : 나 오늘 개발자 경진대회 발표에 나가\n되게 긴장되겠다. 너라면 잘 할 수 있을거야!"
                },
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
