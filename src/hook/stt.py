import logging
import sys
import requests
import dotenv
import os
from fastapi.responses import JSONResponse

dotenv.load_dotenv('.env')
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

class Stt():
    def stt(self, file_path):
        client_id = os.getenv('client_id')
        client_secret = os.getenv('client_secret')
        lang = "Kor"  # 언어 코드 ( Kor, Jpn, Eng, Chn )
        url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang

        # base_dir = os.path.dirname(os.path.abspath(__file__))
        # file_path = os.path.join(base_dir, 'content', filename)


        data = open(file_path, 'rb')
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
                logging.warning(result["text"])
                return {"result": result["text"], "status_code": 200}
            else:
                return {"result": "STT response is not 200", "status_code": 400}

        except requests.exceptions.RequestException as e:
            return {"result": str(e), "status_code": 400}
