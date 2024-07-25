import base64
import logging
import os
from src.hook.CompletionExecutor import CompletionExecutor
from src.hook.stt import Stt
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import APIRouter

class Model(BaseModel):
    audio: str
    filename: str


class SaveVoiceAPI:
    router = APIRouter()

    @router.post("/saveVoice")
    def save(data: Model):
        try:
            audio = data.audio
            filename = data.filename

            audio_bytes = base64.b64decode(audio)

            content_dir = os.getenv('CONTENT_DIR', r'/content')
            file_path = os.path.join(content_dir,filename)

            with open(file_path, "wb") as f:
                f.write(audio_bytes)
                # 녹음 파일 text로 변경
                stt_instance = Stt()  # Stt 클래스의 인스턴스 생성
                stt_result = stt_instance.stt()  # stt 메서드 호출
                if stt_result.get("status_code") == 200:
                    completion_instance = CompletionExecutor()
                    response = completion_instance.completionExecutor(stt_result.get("result"))
                    if response.get("status_code") == 200:
                        return JSONResponse(content={"result":response.get("result"),"status_code":200})
                    else:
                        return JSONResponse(content={"CompletionExecutorError": response.get("result"),"status_code":400})
                else:
                    return JSONResponse(content =stt_result)

        except Exception as e:
            logging.error(str(e))  # 에러 로그 추가
            raise HTTPException(status_code=400, detail=str(e))