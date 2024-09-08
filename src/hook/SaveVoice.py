import base64
import logging
import os
from src.hook.CompletionExecutor import CompletionExecutor
from src.hook.CompletionExecutorForT import CompletionExecutorT
from src.hook.STT import STT
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import APIRouter
import random


class Model(BaseModel):
    audio: str
    filename: str

class SaveVoiceAPI:
    router = APIRouter()

    @staticmethod
    @router.post("/saveVoice")
    def save_f(data: Model):
        try:
            audio = data.audio
            filename = data.filename

            audio_bytes = base64.b64decode(audio)

            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, 'content', filename)
            with open(file_path, "wb") as f:
                f.write(audio_bytes)
                # 녹음 파일 text로 변경
                stt_result = STT.stt(file_path)  # stt 메서드 호출
                if stt_result.get("status_code") == 200:
                    response = CompletionExecutor().completion_executor(stt_result.get("result"))
                    logging.warning(stt_result.get("result"))
                    if response.get("status_code") == 200:
                        return JSONResponse(content={"result": response.get("result"), "status_code": 200})
                    elif response.get("status_code") == 2000:
                        questions = ["왜 불러", "왜 말을 안해", "응? 뭐라고?", "뭐라고 했어?"]
                        random_number = random.randint(0, 3)
                        return JSONResponse(content={"result": questions[random_number], "status_code": 200})
                    else:
                        return JSONResponse(content={"CompletionExecutorError": response.get("result"), "status_code": 400})
                else:
                    return JSONResponse(content={"result": stt_result, "status_code": 400})

        except Exception as e:
            logging.error(str(e))  # 에러 로그 추가
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    @router.post("/saveVoice/t")
    def save_t(data: Model):
        try:
            audio = data.audio
            filename = data.filename
            audio_bytes = base64.b64decode(audio)
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, 'content', filename)
            with open(file_path, "wb") as f:
                f.write(audio_bytes)
                stt_result = STT.stt(file_path)  # stt 메서드 호출
                if stt_result.get("status_code") == 200:
                    response = CompletionExecutorT().completion_executor_t(stt_result.get("result"))
                    if response.get("status_code") == 200:
                        return JSONResponse(content={"result": response.get("result"), "status_code": 200})
                    elif response.get("status_code") == 2000:
                        questions = ["왜 불러", "왜 말을 안해", "응? 뭐라고?", "뭐라고 했어?"]
                        random_number = random.randint(0, 3)
                        return JSONResponse(content={"result": questions[random_number], "status_code": 200})
                    else:
                        return JSONResponse(
                            content={"CompletionExecutorError_t": response.get("result"), "status_code": 400})
                else:
                    return JSONResponse(content={"result": stt_result, "status_code": 400})
        except Exception as e:
            logging.error(str(e))  # 에러 로그 추가
            raise HTTPException(status_code=400, detail=str(e))