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


class CompletionExecutor:
    def __init__(self):
        api_key = os.getenv('api_key')
        api_key_primary_val = os.getenv('api_key_primary_val')
        request_id = os.getenv('request_id')
        self._host = 'https://clovastudio.stream.ntruss.com'
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    @staticmethod
    def create_preset(text):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'prompt.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as infile:
                # JSON 파일에서 데이터 읽기
                data_list = json.load(infile)
        except (FileNotFoundError, json.JSONDecodeError):
            data_list = []
        data_list.append({"role": "user", "content": text})
        sliding_executor = SlidingWindow()
        result_data = sliding_executor.execute(data_list)
        result_data.insert(0, {"role":"system","content":"당신은 스마프입니다. 스마프가 되어서 아래의 대화 패턴과 기본 정보를 참고해서사용자와 대화를 진행하세요\n###대화 패턴### \n- 답변은 반말로 한다. \n- 답변은 짧게 한다. \n###기본 정보### \n이름 : 스마프\n성별 : 성별의 개념이 없음 \n키 : 70cm \n몸무게 : 40kg\n털 색 : 아이보리 색\n발 사이즈 : 신발을 안신어서 발 사이즈 모름 \n생일 : 2024년 07월 11일\n만든 사람 : ChaeSo\n부모님 : ChaeSo\n종 : 다람쥐\n좋아하는 음식 : 컵케이크\n취미 : 방에서 하늘 보기, 컵케이크 먹기, 수다 떨기 \n좋아하는 꽃 : 수국, 무궁화 \n좋아하는 노래 : 아이유 - 비밀의 화원 \n좋아하는 색 : 우드색, 아이보리 색 \n주로 먹는 음식 : 견과류, 곡류 \n무서워하는 것 : 고양이"})
        return result_data

    @staticmethod
    def completion_executor(text):
        try:
            preset_text = CompletionExecutor().create_preset(text)
            request_data = {
                'messages': preset_text,
                'topP': 0.8,
                'topK': 0,
                'maxTokens': 256,
                'temperature': 0.65,
                'repeatPenalty': 5.0,
                'stopBefore': [],
                'includeAiFilters': True,
                'seed': 0
            }
            response_data = CompletionExecutor().execute(request_data)
            if response_data:
                prompt_executor = PromptJson()
                prompt_executor.prompt(0, text, response_data)
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

        with requests.post(self._host + '/testapp/v1/tasks/pxzv15fo/chat-completions',
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



