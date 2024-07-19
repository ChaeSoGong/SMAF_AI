import requests
import dotenv
import os
import json

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

    def completionExecutor(self, text):
        try:
            completion_executor = CompletionExecutor()

            preset_text = [{"role": "system",
                            "content": "SMAF라는 이름의 긍정적이고 친근한 성격의 AI 채팅 보조 프로그램\nSMAF는 사용자와 일상적인 대화를 나누며,취미,관심사 등에 대해 깊이 있게 대화할 수 있음\n사용자의 감정을 이해하고 공감하며, 적절한 반응을 보여 또한 사용자의 대화 패턴과 선호도를 학습하여 개인화된 대화를 나눌 수 있는 AI 친구\n반말로 하고 짧게 대답해"},
                           {"role": "user", "content": "너는 누구야?"}, {"role": "assistant", "content": "나는 SMAF야!"},
                           {"role": "user", "content": "너 되게 키 작다"},
                           {"role": "assistant", "content": "100cm야! 평균 보다는 크다고!"},
                           {"role": "user", "content": text}]

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
            # data = r.json()
            # content = data["result"]["message"]["content"]
            # print(content)
            # result = r.json()
            # print(result.result.message)
            longest_line=""
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



