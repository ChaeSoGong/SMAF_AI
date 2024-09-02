import logging

import requests
import dotenv
import os
import json
from src.hook.SlidingWindow import SlidingWindow

from src.hook.PromptJson import PromptJson

dotenv.load_dotenv('.env')
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

class CompletionExecutor_t:

    def __init__(self):
        api_key = os.getenv('api_key')
        api_key_primary_val = os.getenv('api_key_primary_val')
        request_id = os.getenv('request_id')
        self._host = 'https://clovastudio.stream.ntruss.com'
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def create_t_preset(self, text):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 't_prompt.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as infile:
                # JSON 파일에서 데이터 읽기
                data_list = json.load(infile)
        except (FileNotFoundError, json.JSONDecodeError):
            data_list = []
        data_list.append({"role": "user", "content": text})
        sliding_executor = SlidingWindow()
        result_data = sliding_executor.execute(data_list)
        result_data.insert(0, {
            "role": "system",
            "content": "당신은 이성적이고 현실적이며 츤데레 성격의 스마트 입니다. 스마트가 되어서 사용자와 대화를 진행합니다. 아래의 대화 패턴과 기본 정보, 성격을 참고해서 질문에 대해 답변해주세요.\n###대화 패턴###\r\n- 답변은 반말로 한다.\r\n- 답변은 짧게 한다.\r\n###기본 정보###\r\n이름 : 스마트\r\n성별 : 성별의 개념이 없음\r\n키 : 75cm\r\n몸무게 : 35kg\r\n털 색 : 아이보리, 갈색, 주황색\r\n눈들 : \r\n발 사이즈 : 신발을 안신어서 발 사이즈 모름\r\n생일 : 2024년 08월 30일\r\n만든 사람 : ChaeSo\r\n종 : 고양이\r\n좋아하는 음식 : 아이스 아메리카노\r\n###성격###\r\n이성적 : 스마트는 감성보다는 이성을 중시한다.\r\n논리적 : 스마트는 무슨 일이든 논리적인 판단을 우선시한다.\r\n분석적 : 스마트는 모든 상황을 현실적으로 분석한다.\r\n내향적 : 친구들을 여러 명 사귀는 것을 좋아하지 않는다.\r\n계획적\r\n직관적 : 상상을 잘 하지 못한다.\r\n"
        })

        return result_data

    def completionExecutor_t(self, text):
        try:
            completion_executor = CompletionExecutor_t()
            preset_text = completion_executor.create_t_preset(text)
            request_data = {
                'messages': preset_text,
                'topP': 0.8,
                'topK': 0,
                'maxTokens': 256,
                'temperature': 0.25,
                'repeatPenalty': 5.0,
                'stopBefore': [],
                'includeAiFilters': True,
                'seed': 0
            }
            response_data = completion_executor.execute(request_data)
            if (response_data):
                prompt_executor = PromptJson()
                prompt_executor.prompt(1,text, response_data)
                return {"result": response_data, "status_code": 200}

        except Exception as e:
            return {"result": e, "status_code": 400}

    def execute(self, completion_request):

        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8'
            ,'Accept': 'text/event-stream'
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



