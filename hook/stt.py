import sys
import requests
import dotenv
import os
from flask import request, jsonify
from flask_restful import Resource

dotenv.load_dotenv('.env')
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

class SttApi(Resource):
    def post(self):
        client_id = os.getenv('client_id')
        client_secret = os.getenv('client_secret')
        lang = "Kor"  # 언어 코드 ( Kor, Jpn, Eng, Chn )
        url="https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
        data = open(r'C:\Users\jangs\PycharmProjects\smaf\content\_posts_assets_2020-01-13-stt-step-by-step_original.mp3', 'rb')
        headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret,
            "Content-Type": "application/octet-stream"
        }
        try:
            response = requests.post(url, data=data, headers=headers)
            rescode = response.status_code
            result = response.json()
            if rescode == 200:
                result = result["text"]
            else:
                result = "STT response is not 200 : " + result["text"]
        except requests.exceptions.RequestException as e:
            return jsonify({"STT except : " + str(e)}), 400
        return jsonify(result)
