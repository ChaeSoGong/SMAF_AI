import json
import sys
import requests
import dotenv
import os
# from flask_cors import CORS
from flask import request, jsonify
from flask_restful import Resource

dotenv.load_dotenv('.env')
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

class SentimentApi(Resource):
    def post(self):

        data = request.get_json()
        content = data.get('content')
        print(content)
        result = content

        # CLOVA Studio sentiment
        client_id = os.getenv('client_id')
        client_secret = os.getenv('client_secret')
        url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
        data = {
            "content": content,
            "config.negativeClassification": True
        }
        json_data = json.dumps(data)
        headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret,
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url, data=json_data, headers=headers)
            rescode = response.status_code

            if rescode == 200:
                result = response.json()
                # return result
            else:
                result = "Sentiment response is not 200 : " + response.json()
                # return result
        except requests.exceptions.RequestException as e:
            return jsonify({"Sentiment except : " + str(e)})
        return result
