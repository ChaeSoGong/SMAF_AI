# hook
from starlette.middleware.cors import CORSMiddleware

from hook.saveVoice import SaveVoiceAPI

from fastapi import FastAPI
app = FastAPI()

# api.add_resource(SaveVoiceAPI,'/saveVoice')
# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요에 따라 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/saveVoice")
async def save_voice(data: SaveVoiceAPI):  # SaveVoiceAPI는 FastAPI에서 사용할 수 있는 형태로 변환해야 합니다.
    # SaveVoiceAPI의 처리 로직을 여기에 추가
    return {"message": "Voice saved"}


def main():
   import uvicorn
   uvicorn.run(app, host="0.0.0.0", port=2000)


if __name__ == '__main__':
   main()




