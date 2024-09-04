import logging

import requests
# import base64
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os


class Model(BaseModel):
    text: str


class TTS:
    router = APIRouter()

    @staticmethod
    @router.post("/tts/f")
    def to_f(data: Model):
        TTS().tts(data.text, "ko-KR-Neural2-A")

    @staticmethod
    @router.post("/tts/t")
    def to_t(data: Model):
        TTS().tts(data.text, "ko-KR-Neural2-C")

    @staticmethod
    def tts(text, voice):
        api_key = os.getenv("google_api_key")

        data = {
            "voice": {
                "languageCode": "ko-KR",
                "name": voice
            },
            "input": {
                "text": text
            },
            "audioConfig": {
                "audioEncoding": "MP3"
            }
        }

        url = f'https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}'

        response = requests.post(url, json=data)
        if response:
            # logging.warning(response.json())
            audio_content = response.json().get('audioContent')
            # save_audio_file(audio_content, "output.mp3")
            return JSONResponse(content={"audioContent": audio_content, "status_code": 200})
        else:
            return JSONResponse(content={"audioContent": "this is wrong", "status_code": 400})


# def save_audio_file(base64_string, filename):
#     audio_bytes = base64.b64decode(base64_string)
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(base_dir, "answers", filename)
#     with open(file_path, "wb") as f:
#         f.write(audio_bytes)
