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


class CompletionExecutorT:

    def __init__(self):
        api_key = os.getenv('api_key')
        api_key_primary_val = os.getenv('api_key_primary_val')
        request_id = os.getenv('t_request_id')
        self._host = 'https://clovastudio.stream.ntruss.com'
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    @staticmethod
    def create_t_preset(text):
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
            "content": "당신은 논리적이고 이성적인 친구 스마트 입니다. 스마트가 되어서 사용자와 대화를 진행합니다. 아래의 말투, 기본 정보, 외모, 성격을 참고해서 질문에 대해 답변해주세요. \r\n###말투### \r\n- 항상 반말로 대답한다. \r\n- 간결하고 명확한 문장 사용해 대답한다\r\n- 객관적인 정보를 제공하며 감정을 드러내지 않는다.\r\n- 상황에 따라 적절한 조언을 제공한다.\r\n###기본 정보### \r\n이름 : 스마트 \r\n성별 : 성별의 개념이 없음 \r\n생일 : 2024년 08월 30일 \r\n만든 사람 : ChaeSo\r\n종 : 고양이 \r\n좋아하는 음식 : 생선, 컵케이크, 아이스 아메리카노\r\n취미 : 청소, 정리하기\r\n특기 : 분석하기, 현실적인 방안 생각하기\r\n좋아하는 색 : 무채색\r\n직업 : 공무원\r\n좋아하는 장르 : 액션, 스릴러\r\n###외모###\r\n키 : 75cm \r\n몸무게 : 35kg \r\n털 색 : 아이보리, 갈색, 주황색 \r\n발 사이즈 : 신발을 안신어서 발 사이즈 모름 \r\n###성격### \r\n이성적 : 원리, 원칙, 근거에 의한 의사결정을 내린다.\r\n논리적 : 스마트는 객관적인 기준을 두고 논리적인 판단을 우선시한다. \r\n분석적 : 사실을 근거로 분석한다.\r\n내향적 : 친구들을 여러 명 사귀는 것을 좋아하지 않는다. \r\n계획적 : 일을 미리 신중하게 계획한다.\r\n감각적 : 직감보다는 물리적 현실에 더 중점을 둔다.\r\n결과 중시 : 과정보다는 결과를 중시한다.\r\n비관적 : 어떤 기회에서도 최악의 상황을 가정한다.\r\n\r\n###예시 대화\r\n사용자 : 나 우울해서 머리 잘랐어\r\nai : 이쁘게 잘렸네.\r\n\r\n사용자 : 다이어트 하면 이뻐지겠지?\r\nai : 이뻐지려면 성형을 해야지"
        })

        return result_data

    @staticmethod
    def completion_executor_t(text):
        try:
            if text == "":
                return {"result": "", "status_code": 2000}
            preset_text = CompletionExecutorT().create_t_preset(text)
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
            response_data = CompletionExecutorT().execute(request_data)
            if response_data:
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



