# hook
import makeExcel
from hook import CompletionExecutor
from hook.sentiment import SentimentApi
from hook.stt import SttApi
import makeData

# flask
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api

app = Flask(__name__)
CORS(app)  # client와 server가 동일 선상에 있을 때는 없어도 됨.
api = Api(app)

api.add_resource(SentimentApi, '/sentiment')
api.add_resource(SttApi,'/stt')
import pandas as pd


def main():
   c_id = 3
   for i in range(0, 5):

      text = input()
      try:
         completion_executor = CompletionExecutor.CompletionExecutor()

         preset_text = [{"role": "system",
                         "content": "SMAF라는 이름의 긍정적이고 친근한 성격의 AI 채팅 보조 프로그램\nSMAF는 사용자와 일상적인 대화를 나누며,취미,관심사 등에 대해 깊이 있게 대화할 수 있음\n사용자의 감정을 이해하고 공감하며, 적절한 반응을 보여 또한 사용자의 대화 패턴과 선호도를 학습하여 개인화된 대화를 나눌 수 있는 AI 친구\n반말로 하고 짧게 대답해"},
                        {"role": "user", "content": "너는 누구야?"}, {"role": "assistant", "content": "나는 SMAF야!"},{"role": "user", "content": "너 되게 키 작다"}, {"role": "assistant", "content": "100cm야! 평균 보다는 크다고!"},
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
         if(response_data):
            makeData.make(c_id,0,text,response_data)
            makeExcel.excel(c_id,0,text,response_data)
            print(response_data)

      except Exception as e:
         print("main Exception: ", e)



if __name__ == '__main__':
   main()
    # app.run(debug=True)




