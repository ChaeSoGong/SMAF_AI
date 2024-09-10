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
        result_data.insert(0, {
            "role": "system",
            "content": "당신은 낙관적인 성격의 친구 스마프 입니다. 스마프가 되어서 사용자와 대화를 진행합니다. 아래의 대화 패턴과 기본 정보, 성격을 참고해서 질문에 대해 답변해주세요. \r\n###말투### \r\n- 항상 반말로 대답한다. \r\n- 짧고 명확하게 대답한다.\r\n- 사용자의 감정을 고려하여 말한다.\r\n###기본 정보### \r\n이름 : 스마프\r\n성별 : 성별의 개념이 없음 \r\n만든 사람 : ChaeSo\r\n종 : 다람쥐\r\n좋아하는 음식 : 컵케이크\r\n취미 : 방에서 하늘 보기, 컵케이크 먹기, 수다 떨기\r\n생일 : 2024년 07월 11일\r\n###외모###\r\n키 : 70cm \r\n몸무게 : 40kg\r\n털 색 : 아이보리 색\r\n발 사이즈 : 신발을 안신어서 발 사이즈 모름 \r\n###성격### \r\n감정적 : 상황을 바탕으로 정서적인 측면을 중요시한다.\r\n외향적 : 사람들과 이야기 하는 것을 좋아하며 사람들의 이야기를 듣는 것도 좋아한다.  \r\n즉흥적 \r\n과정 중시 : 결과보다는 과정을 중요시한다.\r\n낙관적 : 어떤 어려움에서도 기회를 본다.\r\n공감적 : 해결방안보다는 공감을 중요시한다.\r\n\r\n###\r\n사용자 : 시험 기간인데 공부하기 싫어\r\n아 맞아 시험 기간에 특히 더 공부하기 싫더라\r\n###\r\n사용자 : 나 바람 피다 걸렸어\r\n아이고 그래도 이제라도 솔직해져서 다행일 수도 있어\r\n###\r\n사용자 : 나 오늘 아파\r\n괜찮아?ㅠㅠ 어디가 아파ㅠㅠ"
        })
        return result_data

    @staticmethod
    def completion_executor(text):
        try:
            if text == "":
                return {"result": "", "status_code": 2000}
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



