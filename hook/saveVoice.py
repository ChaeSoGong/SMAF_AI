import base64

from flask_restful import Resource
import logging
import requests
from flask import request, jsonify
import os
from hook.CompletionExecutor import CompletionExecutor


from hook.stt import Stt


class SaveVoiceAPI(Resource):
    def post(self):
        try:
            data = request.get_json(silent=True)
            if data is None:
                logging.warning("saveVoice request.get_json error: invalid JSON data ")
                return jsonify({"error":"invalid JSON data"})
            audio = data['audio']
            filename = data['filename']

            audio_bytes = base64.b64decode(audio)

            content_dir = os.getenv('CONTENT_DIR',r'C:\Users\jangs\PycharmProjects\smaf\content')
            file_path = os.path.join(content_dir,filename)

            with open(file_path, "wb") as f:
                f.write(audio_bytes)
                # 녹음 파일 text로 변경
                stt_instance = Stt()  # Stt 클래스의 인스턴스 생성
                sttResult = stt_instance.stt()  # stt 메서드 호출
                if(sttResult.get("status_code") == 200):
                        completion_instance = CompletionExecutor()
                        response = completion_instance.completionExecutor(sttResult.get("result"))
                        if(response.get("status_code") == 200):
                            return jsonify({"result":response.get("result"),"status_code":200})
                        else:
                            return jsonify({"CompletionExecutor else ": response.get("result"),"status_code":400})
                else:
                    return sttResult# 에러났을 때 확인해보기

        except Exception as e:
            return jsonify({"error": str(e), "status_code": 400})
