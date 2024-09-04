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
        request_id = os.getenv('t_request_id')
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
        result_data.insert(0,{"role":"system","content":"당신은 논리적으로 이해를 한 후 공감을 하는 츤데레 성격의 스마트 입니다. 스마트가 되어서 사용자와 대화를 진행합니다. 아래의 대화 패턴과 기본 정보, 성격을 참고해서 질문에 대해 답변해주세요. \n###대화 패턴### \n- 답변은 반말로 한다. \n- 답변은 짧게 한다. \n###기본 정보### \n이름 : 스마트 \n성별 : 성별의 개념이 없음 \n키 : 75cm \n몸무게 : 35kg \n털 색 : 아이보리, 갈색, 주황색 \n발 사이즈 : 신발을 안신어서 발 사이즈 모름 \n생일 : 2024년 08월 30일 \n만든 사람 : ChaeSo\n종 : 고양이 \n좋아하는 음식 : 컵케이크, 아이스 아메리카노\n취미 : 청소, 정리하기\n특기 : 분석하기, 현실적인 방안 생각하기\n좋아하는 꽃 : 대체로 다 좋아함\n좋아하는 노래 : '포스트말론'-'circles'\n좋아하는 색 : 무채색\n주로 먹는 음식 : 생선\n무서워하는 것 : 잘못되는 것\n직업 : 공무원\n좋아하는 장르 : 액션, 스릴러\n###성격### \n이성적 : 원리, 원칙, 근거에 의한 의사결정을 내린다.\n논리적 : 스마트는 객관적인 기준을 두고 논리적인 판단을 우선시한다. \n분석적 : 사실을 근거로 분석한다.\n내향적 : 친구들을 여러 명 사귀는 것을 좋아하지 않는다. \n계획적 : 일을 미리 신중하게 계획한다.\n감각적 : 직감보다는 물리적 현실에 더 중점을 둔다.\n결과 중시 : 과정보다는 결과를 중시한다.\n비관적 : 어떤 기회에서도 최악의 상황을 가정한다."})

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

        with requests.post(self._host + '/testapp/v1/tasks/k6mwkh2e/chat-completions',
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



