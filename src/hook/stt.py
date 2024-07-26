import sys
import requests
import dotenv
import os
from fastapi.responses import JSONResponse

dotenv.load_dotenv('.env')
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

class Stt():
    def stt(self):
        client_id = os.getenv('client_id')
        client_secret = os.getenv('client_secret')
        lang = "Kor"  # 언어 코드 ( Kor, Jpn, Eng, Chn )
        url="https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
        data = open(r'./content/audioData.wav', 'rb')
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
                return {"result":result["text"], "status_code": 200}
                # return jsonify({"result": result["text"], "status": 200})
            else:
                return {"result": "STT response is not 200", "status_code": 400}

        except requests.exceptions.RequestException as e:
            return {"result": str(e), "status_code": 400}
