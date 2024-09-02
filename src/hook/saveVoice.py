import base64
import logging
import os
from src.hook.CompletionExecutor import CompletionExecutor
from src.hook.CompletionExecutorForT import CompletionExecutor_t
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
    def save_f(data: Model):
        try:
            logging.warning("1")
            audio = data.audio
            filename = data.filename

            audio_bytes = base64.b64decode(audio)

            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, 'content', filename)
            with open(file_path, "wb") as f:
                logging.warning("2")

                f.write(audio_bytes)
                # 녹음 파일 text로 변경
                stt_instance = Stt()  # Stt 클래스의 인스턴스 생성
                stt_result = stt_instance.stt(file_path)  # stt 메서드 호출
                logging.warning("3")
                if stt_result.get("status_code") == 200:
                    logging.warning("4")
                    completion_instance = CompletionExecutor()
                    response = completion_instance.completionExecutor(stt_result.get("result"))
                    logging.warning(stt_result.get("result"))
                    logging.warning("5")
                    if response.get("status_code") == 200:
                        logging.warning("6")
                        #여기에 TTS
                        return JSONResponse(content={"result": response.get("result"), "status_code": 200})
                    else:
                        return JSONResponse(content={"CompletionExecutorError": response.get("result"), "status_code": 400})
                else:
                    return JSONResponse(content={"result": stt_result, "status_code": 400})

        except Exception as e:
            logging.error(str(e))  # 에러 로그 추가
            raise HTTPException(status_code=400, detail=str(e))

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
                # 녹음 파일 text로 변경
                stt_instance = Stt()  # Stt 클래스의 인스턴스 생성
                stt_result = stt_instance.stt(file_path)  # stt 메서드 호출
                if stt_result.get("status_code") == 200:
                    completion_instance = CompletionExecutor_t()
                    response = completion_instance.completionExecutor_t(stt_result.get("result"))
                    if response.get("status_code") == 200:
                        # 여기에 TTS
                        return JSONResponse(content={"result": response.get("result"), "status_code": 200})
                    else:
                        return JSONResponse(
                            content={"CompletionExecutorError_t": response.get("result"), "status_code": 400})
                else:
                    return JSONResponse(content={"result": stt_result, "status_code": 400})
        except Exception as e:
            logging.error(str(e))  # 에러 로그 추가
            raise HTTPException(status_code=400, detail=str(e))