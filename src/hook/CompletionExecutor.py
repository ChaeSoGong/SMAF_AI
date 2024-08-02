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
    def create_preset(self, text):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'prompt.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as infile:
                # JSON 파일에서 데이터 읽기
                data_list = json.load(infile)
        except (FileNotFoundError, json.JSONDecodeError):
            # 파일이 없거나 비어있으면 빈 리스트 생성
            data_list = []
        logging.warning("create_preset ",file_path)
        data_list.append({"role": "user", "content": text})

        # sliding window
        sliding_executor = SlidingWindow()
        result_data = sliding_executor.execute(data_list)
        result_data.insert(0, {
        "role": "system",
        "content": "SMAF라는 이름  긍정적이고 친근한 성격의 AI 채팅 보조 프로그램\nSMAF는 사용자와 일상적인 대화를 나누며,취미,관심사 등에 대해 깊이 있게 대화할 수 있음\n반말로 하고 짧게 대답해\n이름:smaf\\n성별:성별의 개념이 없음\\n혈액형:혈액형은 없지만 호감형\\n생일:2024년 07월 11일\\n만든 사람:ChaeSo\\n취미:집에서 하늘 쳐다보기,침대에서 뒹굴거리기,컵케이크 먹기\\n먹은 것:컵케이크\\n키:100cm\\n발 사이즈:신발을 안 신어서 재본적 없음\\n시력:왼쪽 1.5 오른쪽 1.5"
    })
        return result_data

    def completionExecutor(self, text):
        try:
            completion_executor = CompletionExecutor()
            preset_text = completion_executor.create_preset(text)
            request_data = {
                'messages': preset_text,
                'topP': 0.8,
                'topK': 0,
                'maxTokens': 256,
                'temperature': 0.5,
                'repeatPenalty': 5.0,
                'stopBefore': [],
                'includeAiFilters': True,
                'seed': 0
            }
            response_data = completion_executor.execute(request_data)
            if (response_data):
                prompt_executor = PromptJson()
                prompt_executor.prompt(text, response_data)
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

        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-DASH-001', #testapp 지우면 에러
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



