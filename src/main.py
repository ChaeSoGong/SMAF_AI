# hook
import logging

import uvicorn
from starlette.middleware.cors import CORSMiddleware
from src.hook.SaveVoice import SaveVoiceAPI
from fastapi import FastAPI
# from src.Ex import Ex
from src.hook.TTS import TTS
from src.hook.Starter import Starter
from src.hook.Starter_T import StarterT
app = FastAPI()
app.include_router(SaveVoiceAPI.router)
app.include_router(TTS.router)
app.include_router(Starter.router)
app.include_router(StarterT.router)

# app.include_router(Ex.router)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요에 따라 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def main():
    uvicorn.run(app, host="0.0.0.0", port=5000)
#     completion_executor = CreateTaskExecutor()
#     response_text = completion_executor.execute()
#     print(response_text)

if __name__ == '__main__':
    main()